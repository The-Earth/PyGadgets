import os

domain = ''

while 1:
    add = input('Add a domain: ')
    if add == '0':
        break
    domain += '-d '+ add

os.system('certbot certonly --standalone %s' % domain)
    
