#!/bin/bash
#
# Given a list of talk IDs, link them to the talks schedule (but without
# rooms or times yet) so that they show up in the list of accepted talks
# at `/{YEAR}/schedule/talks/list/`.
#
# See:
#
# pycon/templates/schedule/schedule_list.html
# symposion/schedule/views.py

set -e

if ! [ -f accepted-talks.csv ]
then
    echo "Error: accepted-talks.csv not found"
    exit 1
fi

psql "${1:-pycon2017}" <<'EOF'

begin;

delete from symposion_schedule_presentation;
delete from symposion_schedule_schedule;

create temporary table s (
 x text,
 y text,
 proposal_id integer,
 z text
);

\copy s (x, y, proposal_id, z) from 'accepted-talks.csv' csv;

insert into symposion_schedule_schedule (published, section_id) values (
  true,
  (select id from conference_section where slug = 'talks')
);

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
  null,
  pb.speaker_id,

  '',
  '',
  ''
 from s
  join proposals_proposalbase pb on (s.proposal_id = pb.id)
  join proposals_proposalkind pk on (pb.kind_id = pk.id)
 ;

commit;

EOF
