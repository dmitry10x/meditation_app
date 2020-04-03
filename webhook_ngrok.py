import requests
import json

token_view_list = [
					{'name':'meditation_tracker_app', 'token':'1194336597:AAHj4RczQZ9C9Xg4E_YXMCaoID1Ju1q_gfg', 'view_url':'bot'}
]


def setwebhooks_via_ngrok(ngrok_url, token_view_list=token_view_list):
	for i in token_view_list:
		#first we gotta delete existing webhooks
		try:
			print(i['name'])
			url = 'http://api.telegram.org/bot{}/deletewebhook'.format(i['token'])
			answer = requests.post(url)
			print(answer.json())
		except Exception as e:
			print(e)

		#ok now we`re gonnna set new webhooks <'__'>
		try:
			url = "http://api.telegram.org/bot{}/setwebhook?url={}/{}/".format(i['token'], ngrok_url, i['view_url'])
			answer = requests.post(url)
			print(answer.json())
			print(url)
		except Exception as e:
			print(e)

setwebhooks_via_ngrok('https://67fb6892.ngrok.io')
