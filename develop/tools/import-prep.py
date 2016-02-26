#!/usr/bin/env python2.7
#
# Take various CSV inputs and produce a read-to-import conference schedule.

import pandas as pd
from datetime import date

def main():

    dfs = []

    t = pd.read_csv('talks.csv')

    t['kind_slug'] = 'talk'
    t['proposal_id'] = t.pop('proposal')
    t['day'] = date(2016, 5, 30) + pd.to_timedelta(t['day'], 'd')
    t['room'] = 'Session ' + t['room']

    t = t[['kind_slug', 'proposal_id', 'day', 'time', 'duration', 'room']]

    dfs.append(t)

    t = pd.read_csv('tutorials.csv')

    t['kind_slug'] = 'tutorial'
    t['proposal_id'] = t.pop('ID')
    t['day'] = pd.to_datetime(t['Day Slot'])
    t['time'] = t['Time Slot'].str.extract('([^ ]*)')
    t['duration'] = 200
    t['room'] = 1
    t = t.sort_values(['Title'])
    t['room'] = t.groupby(['day', 'time'])['room'].cumsum()
    t['room'] = t['room'].apply(lambda n: 'Tutorial {}'.format(n))

    t = t[['kind_slug', 'proposal_id', 'day', 'time', 'duration', 'room']]

    dfs.append(t)

    #t.to_csv('schedule.csv', index=False)

    pd.concat(dfs).to_csv('schedule.csv', index=False)

if __name__ == '__main__':
    main()
