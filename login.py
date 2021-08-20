#! /usr/bin/env python3

import requests, sys, getpass

url = 'https://signin.intra.42.fr/users/sign_in'

session = requests.session()

def get_csrf(r):
	csrf = {
		'payload': dict(),
		'param': False,
		'token': False
	}

	for line in r.text.split('\n'):
		if 'csrf' in line:
			if 'csrf-param' in line:
				csrf['param'] = line.split('"')[3]
			elif 'csrf-token' in line:
				csrf['token'] = line.split('"')[3]

	if not csrf['param'] or not csrf['token']:
		return False

	csrf['payload'] = {csrf['param']: csrf['token']}

	return(csrf['payload'])

payload = get_csrf(session.get(url))

if not payload:
	print('Error: Could not get csrf values', file=sys.stderr)
	exit(1)

payload['user[login]'] = input('42 login: ')
payload['user[password]'] = getpass.getpass()

r = session.post(url, data=payload)

if 'signin' in r.url:
	inside_div = False
	for line in r.text.split('\n'):
		if inside_div:
			print(line.split('>')[1].split('<')[0], file=sys.stderr)
			break
		inside_div = ('notifications-flash-top-bar' in line)
	exit(1)

print('Cookie `_intra_42_session_production`:', session.cookies.get('_intra_42_session_production'))
