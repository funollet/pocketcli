#!/usr/bin/env python
# delete_all_my_data.py
#
# Copyright (C) 2014  Jordi Funollet Pujol <funollet@fastmail.fm>

import pocket
import click
import ConfigParser


def connect(conf):
    cfg = ConfigParser.SafeConfigParser()
    cfg.read(conf)
    consumer_key = cfg.get("pocket", "consumer_key")
    access_token = cfg.get("pocket", "access_token")

    return pocket.Pocket(consumer_key, access_token)



@click.command(help='Do you really want ALL your bookmarks permanently deleted from Pocket?')
@click.option('-c', '--conf', default='auth.ini',
        help="INI file containing authentication data; see script 'get_auth.py'")
def delete_all_my_data(conf):

    pock = connect(conf)

    r,h = pock.get()
    for item in r['list'].keys():
        pock = pock.delete(item)
    pock.commit()


if __name__ == '__main__':
    delete_all_my_data()
