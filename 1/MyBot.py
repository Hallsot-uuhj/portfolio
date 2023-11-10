from vk_api import longpoll, vk_api
from datetime import datetime
import requests
import json
import time
import re
from random import randint

init = vk_api.VkApi(token='token')
vk = init.get_api() 
lp = longpoll.VkLongPoll(init)
MY_ID = 41234

def detime(time):
	date = datetime.fromtimestamp(time)
	return date.strftime("%H:%M:%S")

def get_id(uid):
	check_link = uid.split('/')
	if 'https:' in check_link:
		return vk.utils.resolveScreenName(screen_name=check_link[3])['object_id']
	else:
		if 'club' in uid:
			cid = re.findall(r'club\d+', str(uid))[0]
			return int(cid.replace('club','-'))
		elif 'id' in uid:
			uid = re.findall(r'id\d+', str(uid))[0]
			return int(uid.replace('id',''))
		else:
			return int(uid)

def get_name(uid):
	uid = get_id(uid)
	info = vk.users.get(user_ids=uid)[0]
	return f"{info['last_name']} {info['first_name'][0]}."

def proc(event, data):
	if event == 'type':
		return data[0]
	if event == 'message_id':
		return data[1]
	if event == 'peer_id':
		return data[3]
	if event == 'date':
		return data[4]
	if event == 'text':
		return data[5]
	if event == 'user_id':
		try:
			return data[6]['from']
		except:
			return 0
	if event == 'chat_id':
		if data[3] > 2000000000:
			return data[3] - 2000000000
		else:
			return 0
	if event == 'triffle':
		return data[7]

	if event == 'rand':
		return data[8]


for event in lp.listen():
	try:
		if proc('type',event.raw) == 4:
			msg = proc('text',event.raw).split(' ')
			if proc('peer_id',event.raw) < 2000000000 and proc('peer_id',event.raw) != MY_ID:
				data = {}
				with open('logs.json','r') as f:
					data = json.load(f)
					peer_id = str(proc('peer_id',event.raw))
					if proc('rand',event.raw) > 0:
						text = f'От меня - '
					elif proc('rand',event.raw) == 0:
						text = f'От него - '
					text += proc('text',event.raw)
					if proc('triffle',event.raw)!= {}:
						try:
							if (proc('triffle',event.raw)['attach1_type'] == 'doc'
								) and (
								proc('triffle',event.raw)['attach1_kind'] == 'audiomsg'):
								dat = json.loads(proc('triffle',event.raw)['attachments'])
								if text != 'От меня - '  or text != 'От него - ':
									text += f"\n⠀⠀Голосовая: {dat[0]['audio_message']['link_mp3']}"
								else:
									text += f"Голосовая: {dat[0]['audio_message']['link_mp3']}"
						except KeyError:
							pass

					if peer_id not in data['ls']:
						data['ls'].update(
							{
								peer_id: {
									"log": [text], 
									"date": [int(time.time())]
								}
							}
						)
					else:
						data['ls'][peer_id]['log'].append(text)
						data['ls'][peer_id]['date'].append(int(time.time()))

				with open('logs.json','w') as f:
					json.dump(data,f)

			elif proc('peer_id',event.raw) == MY_ID:
				if msg[0] == '/logs':
					try:
						peer_id = str(get_id(msg[1]))
						with open('logs.json','r') as f:
							data = json.load(f)
							if peer_id not in data['ls']:
								vk.messages.send(message='В базе данных нету сообщений от данного пользователя',user_id=proc('peer_id',event.raw),random_id=0)
							else:
								if int(msg[2]) <= len(data['ls'][peer_id]['date']) and int(msg[2]) > 0:
									count = len(data['ls'][peer_id]['date']) - int(msg[2])
									cout = len(data['ls'][peer_id]['date'])
									text = '\n'.join(f'[id{MY_ID}|({detime(data["ls"][peer_id]["date"][d])});] {data["ls"][peer_id]["log"][d]}' for d in range(count,cout))
									vk.messages.send(message=f'Отображено {msg[2]} сообщ. в диалоге с пользователем:\n\n{text}',user_id=proc('peer_id',event.raw),random_id=0)
								else:
									vk.messages.send(message='Кол-во запрашиваемых сообщений не должны быть меньше нуля '
															 'и больше хранящихся в базе данных сообщений.\n'
															 f'Всего сообщений с данным пользователем: {len(data["ls"][peer_id]["date"])}',user_id=proc('peer_id',event.raw),random_id=0)
					except IndexError:
						vk.messages.send(message='Использование: /logs (ID) (кол-во)',user_id=proc('peer_id',event.raw),random_id=0)

				if msg[0] == '/logslist':
					with open('logs.json','r') as f:
						data = json.load(f)
						text = '\n'.join(f"[id{d}|{get_name(d)}] - {len(data['ls'][d]['date'])}" for d in data['ls'])
						vk.messages.send(message=f'Все хранящиеся логи в личных сообщениях:\n\n{text}',user_id=proc('peer_id',event.raw),random_id=0)

				if msg[0] == '/logsremove':
					with open('logs.json','w') as f:
						data = {"ls":{},"peers":{}}
						json.dump(data,f)
					vk.messages.send(message='База данных была очищена.',user_id=proc('peer_id',event.raw),random_id=0)

			elif proc('peer_id',event.raw) > 2000000000:
				if int(proc('user_id',event.raw)) != MY_ID:
					data = {}
					with open('logs.json','r') as f:
						data = json.load(f)
						user_id = str(proc('user_id',event.raw))
						peer_id = str(proc('peer_id',event.raw))
						text = f"[id{user_id}|{get_name(user_id)}] - {proc('text',event.raw)}"
						if proc('triffle',event.raw)!= {}:
							try:
								if (proc('triffle',event.raw)['attach1_type'] == 'doc'
									) and (
									proc('triffle',event.raw)['attach1_kind'] == 'audiomsg'):
									dat = json.loads(proc('triffle',event.raw)['attachments'])
									text += f"\n⠀⠀Голосовая: {dat[0]['audio_message']['link_mp3']}"
							except KeyError:
								pass

						if peer_id not in data['peers']:
							data['peers'].update(
								{
									peer_id: {
										"log": [text], 
										"date": [int(time.time())]
										
									}
								}
							)
						else:
							data['peers'][peer_id]['log'].append(text)
							data['peers'][peer_id]['date'].append(int(time.time()))

					with open('logs.json','w') as f:
						json.dump(data,f)
				else:
					if msg[0] == '/logs':
						try:
							peer_id = str(proc('peer_id',event.raw))
							with open('logs.json','r') as f:
								data = json.load(f)
								if peer_id not in data['peers']:
									vk.messages.send(message='В базе данных нету сообщений с этой беседы',peer_id=proc('peer_id',event.raw),random_id=0)
								else:
									if int(msg[1]) <= len(data['peers'][peer_id]['date']) and int(msg[1]) > 0:
										count = len(data['peers'][peer_id]['date']) - int(msg[1])
										cout = len(data['peers'][peer_id]['date'])
										text = '\n'.join(f'[{detime(data["peers"][peer_id]["date"][d])}]: {data["peers"][peer_id]["log"][d]}' for d in range(count,cout))
										vk.messages.send(message=f'Отображено {msg[1]} сообщ. в этой беседе:\n\n{text}',peer_id=proc('peer_id',event.raw),random_id=0,disable_mentions=1)
									else:
										vk.messages.send(message='Кол-во запрашиваемых сообщений не должны быть меньше нуля '
																 'и больше хранящихся в базе данных сообщений.\n'
																 f'Всего сообщений в данном чате: {len(data["peers"][peer_id]["date"])}',peer_id=proc('peer_id',event.raw),random_id=0)
						except IndexError:
							vk.messages.send(message='Использование: /logs (кол-во)',peer_id=proc('peer_id',event.raw),random_id=0)

					elif msg[0] == '/nn':
						rand = ['q','ы','в','ф','ап','па','ш','u','e','k','l','asd','qw','er','t','y','ыва','выи','о','ро','я','.','о','н','а','м','с','ы','р']
						vk.messages.send(message=rand[randint(0,len(rand))],peer_id=proc('peer_id',event.raw),random_id=0)

	except Exception as e:
		print(e)