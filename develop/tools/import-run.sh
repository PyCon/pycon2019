#!/bin/bash
#
# Given a talks schedule CSV, import the data into PostgreSQL import.

set -e

# DAY1=2016-05-28
# DAY2=2016-05-29
# DAY3=2016-05-30
# DAY4=2016-05-31
# DAY5=2016-06-01

DAY1=2017-05-17
DAY2=2017-05-18
DAY3=2017-05-19
DAY4=2017-05-20
DAY5=2017-05-21

cat > breaks.csv <<EOF
kind_slug,kind_label,day,start,duration,room_name,content_override
sponsor-tutorial,Break,${DAY1},10:30,30,(B110-111|B118-119),
sponsor-tutorial,Lunch,${DAY1},12:30,60,(B110-111|B118-119),
sponsor-tutorial,Break,${DAY2},10:30,30,(B110-111|B118-119),
sponsor-tutorial,Lunch,${DAY2},12:30,60,(B110-111|B118-119),
sponsor-tutorial,Break,${DAY2},15:00,30,(B110-111|B118-119),
sponsor-tutorial, ,${DAY2},17:00,60,(B110-111|B118-119),
sponsor-tutorial,plenary,${DAY2},18:00,180,(B110-111|B118-119),Opening Reception
tutorial,Lunch,${DAY1},12:20,60,(B%|C%|Room%),
tutorial,Lunch,${DAY2},12:20,60,(B%|C%|Room%),
tutorial, ,${DAY2},16:40,80,(B%|C%|Room%),
tutorial,plenary,${DAY2},18:00,150,(B%|C%|Room%),Opening Reception (Expo Hall)
talk,Breakfast,${DAY2},8:00,600,Session %,Registration desk open
talk,plenary,${DAY2},18:00,150,Session %,Opening Reception (Expo Hall)
talk,Breakfast,${DAY3},8:00,60,Session %,
talk,plenary,${DAY3},9:00,30,Session %,Welcome to PyCon
talk,plenary,${DAY3},9:30,40,Session %,Keynote: Jake Vanderplas
talk,Break,${DAY3},10:10,40,Session %,
talk,Lunch,${DAY3},12:40,60,Session A,
talk,Lunch,${DAY3},12:40,60,Session B,
talk,Lunch,${DAY3},12:55,60,Session C,
talk,Lunch,${DAY3},12:55,60,Session D,
talk,Lunch,${DAY3},12:55,60,Session E,
talk,Break,${DAY3},15:45,30,Session A,
talk,Break,${DAY3},15:45,30,Session B,
talk,Break,${DAY3},16:00,30,Session C,
talk,Break,${DAY3},16:00,30,Session D,
talk,Break,${DAY3},16:00,30,Session E,
talk,plenary,${DAY3},17:40,60,Session %,Lightning Talks
talk,Breakfast,${DAY4},8:00,30,Session %,
talk,plenary,${DAY4},8:30,30,Session %,Lightning Talks
talk,plenary,${DAY4},9:00,40,Session %,Keynote: Lisa Guo & Hui Ding
talk,plenary,${DAY4},9:40,40,Session %,Keynote: Katy Huff
talk,Break,${DAY4},10:20,30,Session %,
talk,Lunch,${DAY4},12:40,60,Session A,
talk,Lunch,${DAY4},12:40,60,Session B,
talk,Lunch,${DAY4},12:55,60,Session C,
talk,Lunch,${DAY4},12:55,60,Session D,
talk,Lunch,${DAY4},12:55,60,Session E,
talk,Break,${DAY4},15:45,45,Session A,
talk,Break,${DAY4},15:45,45,Session B,
talk,Break,${DAY4},16:00,30,Session C,
talk,Break,${DAY4},16:00,30,Session D,
talk,Break,${DAY4},16:00,30,Session E,
talk,plenary,${DAY4},17:40,50,Session %,Lightning Talks
talk,Break,${DAY4},18:30,150,Session %,PyLadies Charity Auction
talk,Breakfast,${DAY5},8:00,30,Session %,
talk,plenary,${DAY5},8:30,30,Session %,Lightning Talks
talk,plenary,${DAY5},9:00,20,Session %,PSF Community Service Awards
talk,plenary,${DAY5},9:20,40,Session %,"Panel: Paul Everitt with Guido van Rossum and others"
talk,Break,${DAY5},10:00,190,Session %,Poster Session / Job Fair / Lunch (Expo Hall)
talk,plenary,${DAY5},15:10,40,Session %,Keynote: Kelsey Hightower
talk,plenary,${DAY5},15:50,10,Session %,Final Remarks and Conference Close
EOF

psql "${1:-pycon2017}" <<EOF

begin;

create temporary table b (
 slot_id serial,
 kind_slug text,
 kind_label text,
 day date,
 start time,
 duration integer,
 room_name text,
 content_override text
);

create temporary table s (
 kind_slug text,
 proposal_id integer,
 day date,
 start time,
 duration integer,
 room_name text
);

\copy b (kind_slug, kind_label, day, start, duration, room_name, content_override) from 'breaks.csv' csv header;
\copy s from 'schedule.csv' csv header;

-- Avoid conflict with slot id's from schedule.csv:
update b set slot_id = -slot_id;

delete from symposion_schedule_slotkind;
delete from symposion_schedule_slotroom;
delete from symposion_schedule_room;
delete from symposion_schedule_slot;
delete from symposion_schedule_day;
delete from symposion_schedule_presentation_additional_speakers;
delete from symposion_schedule_presentation;
delete from pycon_schedule_session;
delete from pycon_schedule_session_slots;
delete from symposion_schedule_schedule;

create or replace function raise_error(text) returns int as \$\$
begin
  raise exception '%', \$1;
  return -1;
end; \$\$ language plpgsql;

insert into symposion_schedule_schedule (published, section_id)
 select 't', id from conference_section;

alter table s add column schedule_id integer;

update s set schedule_id = coalesce(sss.id,
  raise_error(format('Error! No proposal exists with ID %s', sss.id)))
 from proposals_proposalbase ppb
   join proposals_proposalkind ppk on (ppb.kind_id = ppk.id)
   join symposion_schedule_schedule sss on (ppk.section_id = sss.section_id)
 where s.proposal_id = ppb.id;

select * from s;

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
   select distinct kind_slug, kind_slug from b
   union
   select distinct kind_slug, kind_slug from s
  ) t;

alter table b add column schedule_id integer;

update b set schedule_id = ssk.schedule_id
 from symposion_schedule_slotkind ssk
 where b.kind_slug = ssk.label;

insert into symposion_schedule_day (date, schedule_id)
 select distinct b.day, ss.id
  from b
   join proposals_proposalkind pk on (b.kind_slug = pk.slug)
   join symposion_schedule_schedule ss on (pk.section_id = ss.section_id)
 union
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
 (id, start, "end", content_override, day_id, kind_id)
 select
  b.slot_id,
  start,
  start + cast(duration || ' minutes' as interval),
  coalesce(b.content_override, ''),
  (select id from symposion_schedule_day ssd
    where ssd.date = b.day and ssd.schedule_id = b.schedule_id),
  (select id from symposion_schedule_slotkind ssk
    where label = kind_label and ssk.schedule_id = b.schedule_id)
 from b;

-- Broken:

select * from symposion_schedule_day order by 2, 3;
select * from s;
select s.day, s.schedule_id,
  (select id from symposion_schedule_day ssd
    where ssd.date = s.day and ssd.schedule_id = s.schedule_id)
 from s order by 1, 2;

insert into symposion_schedule_slot
 (id, start, "end", content_override, day_id, kind_id)
 select
  proposal_id,
  start,
  start + cast(duration || ' minutes' as interval),
  '',
  (select id from symposion_schedule_day ssd
    where ssd.date = s.day and ssd.schedule_id = s.schedule_id),
  (select id from symposion_schedule_slotkind where label = kind_slug)
 from s;

insert into symposion_schedule_slotroom (room_id, slot_id)
 select
  ssr.id,
  b.slot_id
 from b
  join symposion_schedule_room ssr on (ssr.name similar to b.room_name);

insert into symposion_schedule_slotroom (room_id, slot_id)
 select
  (select id from symposion_schedule_room where name = room_name),
  proposal_id
 from s;

insert into symposion_schedule_presentation
  (id, title, description, abstract, cancelled,
   proposal_base_id, section_id, slot_id, speaker_id,
   assets_url, slides_url, video_url)
 select
  pb.id,
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

insert into symposion_schedule_presentation
  (id, title, description, abstract, cancelled,
   proposal_base_id, section_id, slot_id, speaker_id,
   assets_url, slides_url, video_url)
 select
  pb.id,
  pb.title,
  pb.description,
  pb.abstract,
  false,

  pb.id,
  (select id from conference_section where slug = 'posters'),
  NULL,
  pb.speaker_id,

  '',
  '',
  ''
 from pycon_pyconposterproposal pp
  join proposals_proposalbase pb on (pp.proposalbase_ptr_id = pb.id)
 where overall_status = 4
  and not cancelled
 ;

insert into symposion_schedule_presentation_additional_speakers
  (presentation_id, speaker_id)
 select
  ssp.id, ppas.speaker_id
 from
  proposals_proposalbase_additional_speakers ppas
  join symposion_schedule_presentation ssp
   on (ppas.proposalbase_id = ssp.proposal_base_id);

-- Session IDs look like XYZ where:
--  X is the main conference day: 1, 2, or 3
--  Y is the room number: 1 through 5
--  Z is part of day: 1 before 1pm, 2 after 1pm, 3 after 4pm

insert into pycon_schedule_session
  (id, day_id)
 select
  (date - '${DAY2}') * 100 + room * 10 + daypart, ssd.id
 from
  symposion_schedule_day ssd
   join symposion_schedule_schedule sss on (ssd.schedule_id = sss.id)
   join conference_section cs on (sss.section_id = cs.id),
  (values (1), (2), (3), (4), (5)) t1 (room),
  (values (1), (2), (3)) t2 (daypart)
 where
  cs.slug = 'talks';

insert into pycon_schedule_session_slots
  (session_id, slot_id)
 select
  pss.id session_id,
  sss.id slot_id
 from
  pycon_schedule_session pss
  join symposion_schedule_day ssd on (pss.day_id = ssd.id)
  join symposion_schedule_slot sss on (ssd.id = sss.day_id)
  join symposion_schedule_slotkind sssk on (sss.kind_id = sssk.id)
  join symposion_schedule_slotroom sssr on (sss.id = sssr.slot_id)
  join symposion_schedule_room ssr on (sssr.room_id = ssr.id)
  join symposion_schedule_schedule sss2 on (sssk.schedule_id = sss2.id)
  join conference_section cs on (sss2.section_id = cs.id)
 where
  (pss.id % 10) = case when sss.start < '13:00:00' then 1
                       when sss.start < '16:00:00' then 2
                       else 3 end
  and
  (pss.id / 10 % 10) = case when ssr.name = 'Session A' then 1
                            when ssr.name = 'Session B' then 2
                            when ssr.name = 'Session C' then 3
                            when ssr.name = 'Session D' then 4
                            else 5 end
  and
  (pss.id / 100) = case when ssd.date = '${DAY3}' then 1
                        when ssd.date = '${DAY4}' then 2
                        else 3 end
  and sssk.label = 'talk'
  and cs.slug = 'talks'
 order by
  session_id;

update symposion_schedule_room
 set name = 'Oregon Ballroom 201–202'
 where name = 'Session A';

update symposion_schedule_room
 set name = 'Oregon Ballroom 203–204'
 where name = 'Session B';

update symposion_schedule_room
 set name = 'Portland Ballroom 251 & 258'
 where name = 'Session C';

update symposion_schedule_room
 set name = 'Portland Ballroom 252–253'
 where name = 'Session D';

update symposion_schedule_room
 set name = 'Portland Ballroom 254–255'
 where name = 'Session E';

commit;

EOF
