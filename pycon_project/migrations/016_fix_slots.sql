update schedule_slot set start = start + INTERVAL '3 hours' where kind_id is not null;
update schedule_slot set "end" = "end" + INTERVAL '3 hours' where kind_id is not null;