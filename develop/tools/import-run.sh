#!/bin/bash
#
# Given a talks schedule CSV, import the data into PostgreSQL import.

set -e

# When tutorials are ready:
# 20160528,2016-05-28,1
# 20160529,2016-05-29,1

cat > breaks.csv <<EOF
day,start,minutes,kind_label
2016-05-30,12:40,60,Lunch
2016-05-30,12:40,60,Lunch
2016-05-30,12:55,60,Lunch
2016-05-30,12:55,60,Lunch
2016-05-30,12:55,60,Lunch
2016-05-31,12:40,60,Lunch
2016-05-31,12:40,60,Lunch
2016-05-31,12:55,60,Lunch
2016-05-31,12:55,60,Lunch
2016-05-31,12:55,60,Lunch
2016-05-30,15:45,30,Break
2016-05-30,15:45,30,Break
2016-05-30,16:00,30,Break
2016-05-30,16:00,30,Break
2016-05-30,16:00,30,Break
2016-05-31,15:45,30,Break
2016-05-31,15:45,30,Break
2016-05-31,16:00,30,Break
2016-05-31,16:00,30,Break
2016-05-31,16:00,30,Break
EOF

cat > kinds.csv <<EOF
id,label
1,talk
8,Break
9,Lunch
EOF

cat > rooms.csv <<EOF
id,name,order
101,Session A,1
102,Session B,2
103,Session C,3
104,Session D,4
105,Session E,5
EOF

psql "${2:-pycon2016}" <<'EOF'

begin;

create temporary table b (
 day date,
 start time,
 minutes integer,
 kind_label text
);

create temporary table k (
 id integer,
 label text
);

create temporary table r (
 id integer,
 name text,
 "order" integer
);

create temporary table s (
 proposal_id integer,
 day date,
 time time,
 minutes integer,
 room_name text
);

\copy b from 'breaks.csv' csv header;
\copy k from 'kinds.csv' csv header;
\copy r from 'rooms.csv' csv header;
\copy s from 'talks2.csv' csv header;

delete from symposion_schedule_slotkind;
delete from symposion_schedule_slotroom;
delete from symposion_schedule_room;
delete from symposion_schedule_slot;
delete from symposion_schedule_day;
delete from symposion_schedule_presentation_additional_speakers;
delete from symposion_schedule_presentation;

insert into symposion_schedule_slotkind select *,
 (select id from symposion_schedule_schedule where section_id =
   (select id from conference_section where slug = 'talks'))
 from k;

insert into symposion_schedule_day (date, schedule_id) select d.day,
 (select id from symposion_schedule_schedule where section_id =
   (select id from conference_section where slug = 'talks'))
 from (select distinct day from s) d;

insert into symposion_schedule_room select *,
 (select id from symposion_schedule_schedule where section_id =
   (select id from conference_section where slug = 'talks'))
 from r;

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
  (select id from symposion_schedule_slotkind where label = 'talk')
 from s;

insert into symposion_schedule_slotroom
 select
  proposal_id,
  (select id from symposion_schedule_room where name = room_name),
  proposal_id
 from s;

insert into symposion_schedule_presentation
 select
  proposal_id,
  pp.title,
  pp.description,
  pp.abstract,
  false,
  proposal_id,
  (select id from conference_section where slug = 'talks'),
  proposal_id,
  pp.speaker_id,
  '',
  '',
  ''
 from s join proposals_proposalbase pp on (pp.id = proposal_id);

insert into symposion_schedule_presentation_additional_speakers
 select id, proposalbase_id, speaker_id
 from proposals_proposalbase_additional_speakers
 where proposalbase_id in (select id from symposion_schedule_presentation);

commit;

EOF
