#!/bin/bash
#
# Build the CSV files needed for SQL import.

set -e

cat schedule.csv | sed '

s/,0,/,20160530,/
s/,1,/,20160531,/
s/,2,/,20160601,/

s/,A,/,Session A,/
s/,B,/,Session B,/
s/,C,/,Session C,/
s/,D,/,Session D,/
s/,E,/,Session E,/

' > schedule2.csv

# When tutorials are ready:
# 20160528,2016-05-28,1
# 20160529,2016-05-29,1

cat > breaks.csv <<EOF
day_id,start,minutes,kind_label
20160530,12:40,60,Lunch
20160530,12:40,60,Lunch
20160530,12:55,60,Lunch
20160530,12:55,60,Lunch
20160530,12:55,60,Lunch
20160531,12:40,60,Lunch
20160531,12:40,60,Lunch
20160531,12:55,60,Lunch
20160531,12:55,60,Lunch
20160531,12:55,60,Lunch
20160530,15:45,30,Break
20160530,15:45,30,Break
20160530,16:00,30,Break
20160530,16:00,30,Break
20160530,16:00,30,Break
20160531,15:45,30,Break
20160531,15:45,30,Break
20160531,16:00,30,Break
20160531,16:00,30,Break
20160531,16:00,30,Break
EOF

cat > days.csv <<EOF
id,date,schedule_id
20160530,2016-05-30,1
20160531,2016-05-31,1
20160601,2016-06-01,1
EOF

cat > kinds.csv <<EOF
id,label,schedule_id
1,talk,1
8,Break,1
9,Lunch,1
EOF

cat > rooms.csv <<EOF
id,name,order,schedule_id
101,Session A,1,1
102,Session B,2,1
103,Session C,3,1
104,Session D,4,1
105,Session E,5,1
EOF

# 2014,20160530,C,16:30:00,30,"To mock, or not to mock, that is the question"

psql "${1:-pycon2016}" <<'EOF'

begin;

create temporary table b (
 day_id integer,
 start time,
 minutes integer,
 kind_label text
);

create temporary table d (
 id integer,
 date date,
 schedule_id integer
);

create temporary table k (
 id integer,
 label text,
 schedule_id integer
);

create temporary table r (
 id integer,
 name text,
 "order" integer,
 schedule_id integer
);

create temporary table s (
 proposal_id integer,
 day_id integer,
 room_name text,
 time time,
 minutes integer,
 title text
);

\copy b from 'breaks.csv' csv header;
\copy d from 'days.csv' csv header;
\copy k from 'kinds.csv' csv header;
\copy r from 'rooms.csv' csv header;
\copy s from 'schedule2.csv' csv header;

delete from symposion_schedule_slotkind;
delete from symposion_schedule_slotroom;
delete from symposion_schedule_room;
delete from symposion_schedule_slot;
delete from symposion_schedule_day;
delete from symposion_schedule_presentation_additional_speakers
delete from symposion_schedule_presentation;

insert into symposion_schedule_slotkind select * from k;
insert into symposion_schedule_day select * from d;
insert into symposion_schedule_room select * from r;

insert into symposion_schedule_slot
 select
  10 + row_number() over (order by start),
  start,
  start + cast(minutes || ' minutes' as interval),
  '',
  day_id,
  (select id from symposion_schedule_slotkind where label = kind_label)
 from b;

insert into symposion_schedule_slot
 select
  proposal_id,
  time,
  time + cast(minutes || ' minutes' as interval),
  '',
  day_id,
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
  s.title,
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

# When testing on my Vagrant box:
#
# alter table symposion_schedule_presentation drop constraint symposion_schedule_presentation_proposal_base_id_key
# alter table symposion_schedule_presentation drop constraint s_proposal_base_id_5335e1577995b5c_fk_proposals_proposalbase_id
