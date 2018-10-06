# CertbotTool

Help get new certificates from [Let's Encrypt](https://letsencrypt.org/) or revoke them. Just don't want to memorize those commands.

`certonly.py` collects all the domains you want to embed in one certificate and will wait for another domain unless it receives a `0`. 

`revoke.py` receive the domain appear in the path of the certificate you want to revoke. 

## Dependency

This tool is for Ubuntu 18.04 with [certbot](https://github.com/certbot/certbot) installed via `apt install certbot` and I guess it works well on most common Linux distribution with certbot installed.

## Acknowledgement

- [Diamond Zhou](https://diamondfsd.com/lets-encrytp-hand-https/)
- [rxblog](https://www.rxblog.xyz/lets-encrypt-certbot-remove-revoke/)

