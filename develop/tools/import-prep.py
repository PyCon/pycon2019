#!/usr/bin/env python2.7
#
# Take various CSV inputs and produce a read-to-import conference schedule.

import os
import pandas as pd
import sys
from datetime import date

def path_to(base, name):
    return os.path.join(os.path.expanduser(base), name)

def main():
    dfs = []
    base = sys.argv[1]

    path = path_to(base, 'talks.csv')
    if os.path.exists(path):
        dfs.append(read_talks(path))

    path = path_to(base, 'tutorials.csv')
    if os.path.exists(path):
        dfs.append(read_tutorials(path))

    c = pd.concat(dfs).rename(columns={'time': 'start'})
    c.to_csv('schedule.csv', index=False)


def read_talks(path):
    t = pd.read_csv(path)

    t['kind_slug'] = 'talk'
    t['proposal_id'] = t.pop('proposal')
    t['day'] = date(2017, 5, 19) + pd.to_timedelta(t['day'], 'd')
    t['room'] = 'Session ' + t['room']

    t = t[['kind_slug', 'proposal_id', 'day', 'time', 'duration', 'room']]

    return t

    # t = pd.read_csv(path_to(base, 'PyCon 2016 Tutorial Counts - Sheet1.csv'))
    # rooms = {str(title).strip().lower(): room_name
    #          for title, room_name in t[['Title', 'Room Name']].values}


def read_tutorials(path):
    t = pd.read_csv(path)

    t['kind_slug'] = 'tutorial'
    t['proposal_id'] = t.pop('id')
    t['day'] = pd.to_datetime(t['day'])
    t['time'] = t['time'].str.extract('([^ ]*)', expand=False)
    t['duration'] = 200
    t['room'] = ['Room {}'.format((n%9) + 1) for n in range(len(t))]
    #t['room'] = t['title'].str.strip().str.lower().map(rooms)

    t = t[['kind_slug', 'proposal_id', 'day', 'time', 'duration', 'room']]

    return t

    # t = pd.read_csv(path_to(base, 'sponsor-tutorials-edited.csv'))

    # t = t[t['ID'].notnull()].copy()
    # t['kind_slug'] = 'sponsor-tutorial'
    # #t['kind_slug'] = 'tutorial'
    # t['proposal_id'] = t.pop('ID').astype(int)
    # t['day'] = pd.to_datetime(t['Day Slot'])
    # t['time'] = t['Time Slot'].str.extract('([^ ]*)')
    # t['room'] = t['Room']
    # # t = t.sort_values(['Title'])
    # # t['room'] = t.groupby(['day', 'time'])['room'].cumsum()
    # # t['room'] = t['room'].apply(lambda n: 'Sponsor Room {}'.format(n))

    # t = t[['kind_slug', 'proposal_id', 'day', 'time', 'duration', 'room']]

    # dfs.append(t)

    #t.to_csv('schedule.csv', index=False)


if __name__ == '__main__':
    main()
