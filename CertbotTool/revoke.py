import os

domain = input('Domain: ')
os.system('certbot revoke --cert-path /etc/letsencrypt/archive/%s/cert1.pem' % domain)
os.system('certbot delete')
