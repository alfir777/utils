#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

path_ssl = '/etc/letsencrypt/live/jatu.ru-0001'
path_privkey = os.path.join('privkey.pem', path_ssl)
password_pfx = 'password_pfx'

if os.path.exists('/var/lib/plexmediaserver/certificate.pfx'):
    time_pfx = os.path.getctime('/var/lib/plexmediaserver/certificate.pfx')
    time_privkey = os.path.getctime(path_privkey)

    if time_pfx < time_privkey:
        os.system(f'openssl pkcs12 -export -out ~/certificate.pfx '
                  f'-password pass:"{password_pfx}" -inkey {path_ssl}/privkey.pem'
                  f' -in {path_ssl}/cert.pem -certfile {path_ssl}/chain.pem')
        os.system('mv ~/certificate.pfx /var/lib/plexmediaserver')
        os.system('chown plex:plex /var/lib/plexmediaserver/certificate.pfx')
        os.system('service apache2 restart')
        os.system('service plexmediaserver restart')
else:
    os.system(f'openssl pkcs12 -export -out ~/certificate.pfx '
              f'-password pass:"{password_pfx}" -inkey {path_ssl}/privkey.pem'
              f' -in {path_ssl}/cert.pem -certfile {path_ssl}/chain.pem')
    os.system('mv ~/certificate.pfx /var/lib/plexmediaserver')
    os.system('chown plex:plex /var/lib/plexmediaserver/certificate.pfx')
    os.system('service apache2 restart')
    os.system('service plexmediaserver restart')
