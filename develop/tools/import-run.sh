#!/bin/bash
#
# Given a talks schedule CSV, import the data into PostgreSQL import.

set -e

# When tutorials are ready:
# 20160528,2016-05-28,1
# 20160529,2016-05-29,1

cat > breaks.csv <<EOF
day,start,minutes,kind_label
talk,2016-05-30,12:40,60,Lunch
talk,2016-05-30,12:40,60,Lunch
talk,2016-05-30,12:55,60,Lunch
talk,2016-05-30,12:55,60,Lunch
talk,2016-05-30,12:55,60,Lunch
talk,2016-05-31,12:40,60,Lunch
talk,2016-05-31,12:40,60,Lunch
talk,2016-05-31,12:55,60,Lunch
talk,2016-05-31,12:55,60,Lunch
talk,2016-05-31,12:55,60,Lunch
talk,2016-05-30,15:45,30,Break
talk,2016-05-30,15:45,30,Break
talk,2016-05-30,16:00,30,Break
talk,2016-05-30,16:00,30,Break
talk,2016-05-30,16:00,30,Break
talk,2016-05-31,15:45,30,Break
talk,2016-05-31,15:45,30,Break
talk,2016-05-31,16:00,30,Break
talk,2016-05-31,16:00,30,Break
talk,2016-05-31,16:00,30,Break
EOF

psql "${2:-pycon2016}" <<'EOF'

begin;

create temporary table b (
 kind_slug text,
 day date,
 start time,
 minutes integer,
 kind_label text
);

create temporary table s (
 kind_slug text,
 proposal_id integer,
 day date,
 time time,
 minutes integer,
 room_name text
);

\copy b from 'breaks.csv' csv header;
\copy s from 'talks2.csv' csv header;

delete from symposion_schedule_slotkind;
delete from symposion_schedule_slotroom;
delete from symposion_schedule_room;
delete from symposion_schedule_slot;
delete from symposion_schedule_day;
delete from symposion_schedule_presentation_additional_speakers;
delete from symposion_schedule_presentation;

insert into symposion_schedule_slotkind (label, schedule_id)
 select
   t.kind_label,
   (select sss.id
     from symposion_schedule_schedule sss
      join conference_section cs on (sss.section_id = cs.id)
     where cs.slug = t.kind_slug || 's'
   )
  from (
   select distinct kind_slug, kind_label from b
   union
   select distinct kind_slug, kind_slug from s
  ) t;

insert into symposion_schedule_day (date, schedule_id)
 select distinct day, ss.id
  from s
   join proposals_proposalbase pb on (s.proposal_id = pb.id)
   join proposals_proposalkind pk on (pb.kind_id = pk.id)
   join symposion_schedule_schedule ss on (pk.section_id = ss.section_id)
 ;

insert into symposion_schedule_room (name, "order", schedule_id)
 select distinct room_name, 1, ss.id
  from s
   join proposals_proposalbase pb on (s.proposal_id = pb.id)
   join proposals_proposalkind pk on (pb.kind_id = pk.id)
   join symposion_schedule_schedule ss on (pk.section_id = ss.section_id)
  order by room_name
 ;

update symposion_schedule_room set "order" = id;

insert into symposion_schedule_slot
 select
  10 + row_number() over (order by start),
  start,
  start + cast(minutes || ' minutes' as interval),
  '',
  (select id from symposion_schedule_day ssd where ssd.date = day),
  (select id from symposion_schedule_slotkind where label = kind_label)
 from b;

insert into symposion_schedule_slot
 select
  proposal_id,
  time,
  time + cast(minutes || ' minutes' as interval),
  '',
  (select id from symposion_schedule_day ssd where ssd.date = day),
  (select id from symposion_schedule_slotkind where label = kind_slug)
 from s;

insert into symposion_schedule_slotroom
 select
  proposal_id,
  (select id from symposion_schedule_room where name = room_name),
  proposal_id
 from s;

insert into symposion_schedule_presentation
 select
  s.proposal_id,
  pb.title,
  pb.description,
  pb.abstract,
  false,
  s.proposal_id,
  pk.section_id,
  s.proposal_id,
  pb.speaker_id,
  '',
  '',
  ''
 from s
  join proposals_proposalbase pb on (s.proposal_id = pb.id)
  join proposals_proposalkind pk on (pb.kind_id = pk.id)
 ;

insert into symposion_schedule_presentation_additional_speakers
 select id, proposalbase_id, speaker_id
 from proposals_proposalbase_additional_speakers
 where proposalbase_id in (select id from symposion_schedule_presentation);

commit;

EOF
