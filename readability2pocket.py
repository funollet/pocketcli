#!/usr/bin/env python
# readability2pocket.py
#
# Copyright (C) 2014  Jordi Funollet Pujol <funollet@fastmail.fm>

import pocket
import json
import time
import click
import ConfigParser


def connect(conf):
    cfg = ConfigParser.SafeConfigParser()
    cfg.read(conf)
    consumer_key = cfg.get("pocket", "consumer_key")
    access_token = cfg.get("pocket", "access_token")

    return pocket.Pocket(consumer_key, access_token)





def epoch(t):
    return int(time.mktime(time.strptime(t, '%Y-%m-%dT%H:%M:%S')))


@click.command()
@click.option('-c', '--conf', default='auth.ini',
        help="INI file containing authentication data; see script 'get_auth.py'")
@click.option('-b', '--bookmarks', default='readability.json',
    help='File with bookmarks exported from Readability')
def import_readability_data(conf, bookmarks):
    pock = connect(conf)
    readability = json.load(open(bookmarks))
    bookmarks = readability['bookmarks']

    # Import as unarchived all bookmarks not already present (just URL and time_added).

    all, __ = pock.get(state='all')
    urls = [ i['given_url'] for i in all['list'].values() ]
    absent = [ it for it in bookmarks if it['article__url'] not in urls]

    for new_bookmark in absent:
        pock.bulk_add(url=new_bookmark['article__url'], time=epoch(new_bookmark['date_added']))

    pock.commit()

    # Mark archived bookmarks as archived items at Pocket.

    all, __ = pock.get(state='all')
    archived = { it['article__url']: it['date_archived'] for it in bookmarks if it['archive'] }

    for article in all['list'].values():
        url = article['given_url']
        item_id = article['item_id']
        if archived.has_key(url):
            pock.archive(item_id=item_id, time=epoch(archived[url]))

    pock.commit()


if __name__ == '__main__':
    import_readability_data()
