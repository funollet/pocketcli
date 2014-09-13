#!/usr/bin/env python
# get_auth.py
#
# Copyright (C) 2014  Jordi Funollet Pujol <funollet@fastmail.fm>


from pocket import Pocket
import time
from ConfigParser import SafeConfigParser
import click

consumer_key = '31652-e58264375cc6e7872768e161'
redirect_uri = 'noplacetogo'


@click.command(help='Authorize the application with your Pocket account. Save it to CONF_FILE.')
@click.argument('conf_file', default='auth.ini')
def get_auth(conf_file):

    request_token = Pocket.get_request_token(consumer_key=consumer_key, redirect_uri=redirect_uri)

# URL to redirect user to, to authorize your app
    auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
    print """Please visit this URL to autorize the application:

        %s

    You've got 60 seconds.""" % auth_url

    time.sleep(60)

    user_credentials = Pocket.get_credentials(consumer_key=consumer_key, code=request_token)
    access_token = user_credentials['access_token']

    cfg = SafeConfigParser()
    cfg.add_section('pocket')
    cfg.set('pocket', 'access_token', access_token)
    cfg.set('pocket', 'consumer_key', consumer_key)
    with open(conf_file) as dest:
        cfg.write(dest)


if __name__ == '__main__':
    get_auth()
