#!/usr/bin/env python2.7
#
# Take various CSV inputs and produce a read-to-import conference schedule.

import pandas as pd
from datetime import date

def main():

    t = pd.read_csv('talks.csv')

    t['kind_slug'] = 'talk'
    t['proposal_id'] = t.pop('proposal')
    t['day'] = date(2016, 5, 30) + pd.to_timedelta(t['day'], 'd')
    t['room'] = 'Session ' + t['room']

    t = t[['kind_slug', 'proposal_id', 'day', 'time', 'duration', 'room']]

    t.to_csv('talks2.csv', index=False)

if __name__ == '__main__':
    main()
