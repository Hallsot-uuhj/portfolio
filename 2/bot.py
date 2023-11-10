# -*- coding: utf8 -*-
from datetime import datetime
from pythonping import ping
from tools.main import *
import tools.apanel as ap
import requests
import time

prefixes = ['/']
proccmds = 0
vk, lp = sys()

print('Bot activate')

while True:
	try:
		for event in lp.listen():
			if event.raw['type'] == 'message_new':
				if 'action' not in event.raw['object']:
					msg = event.obj.text.split(' ')
					from_id = event.obj.from_id
					if ap.checkCf(event.chat_id):
						ap.checkUser(event.chat_id,from_id)
						admLvl = ap.admLvl(event.chat_id,from_id)
						command = msg[0].lower().replace(f'{msg[0][0]}','')
						if msg[0][0] in prefixes:
							#: Commands for 1 lvl;
							if admLvl <= 0 or admLvl > 0:
								if command == 'time':
									vk.messages.send(message=datetime.strftime(datetime.now(), "%d.%m.%y - %H:%M:%S"),chat_id=event.chat_id,random_id=0)

								elif command == 'q':
									vk.messages.removeChatUser(chat_id=event.chat_id,member_id=from_id)

							if admLvl > 0:
								if command == 'admins':
									proccmds += 1
									adms = ap.admins(event.chat_id)
									vk.messages.send(disable_mentions=1,message=f'Список администраторов:\n\n{adms}',chat_id=event.chat_id,random_id=0)

								elif command == 'gc':
									proccmds += 1
									Ping = ping('vk.com').rtt_avg_ms
									uptime = ap.getUpTime()
									vk.messages.send(message=f'Информация\n\nPing: {Ping} ms\nProcessed Commands: {proccmds}\nUpTime: {uptime}',chat_id=event.chat_id,random_id=0)

								elif command == 'ahelp':
									proccmds += 1
									p = msg[0][0]
									try:
										if msg[1] == '1':
											vk.messages.send(
message=f'Команды администратора 1 уровня.\n\n{p}gc - информация о боте.\n{p}admins - список администраторов.\n{p}ahelp - список команд.',
chat_id=event.chat_id,random_id=0)
										elif msg[1] == '2' and admLvl > 1:
											vk.messages.send(
message=f'Команды администратора 2 уровня.\n\n{p}get - информация о пользователе.\n{p}mt - упоминание пользователей.\n{p}mute - выдать блокировку чата.\n{p}unmute - снять блокировку чата.\n{p}kick - исключить пользователя.\n{p}top - топ по сообщениям.\n{p}warn - выдать предупреждение.\n{p}unwarn - снять предупреждение.\n{p}warns - список предупреждений.',
chat_id=event.chat_id,random_id=0)
										elif msg[1] == '3' and admLvl > 2:
											vk.messages.send(
message=f'Команды администратора 3 уровня.\n\n{p}ban - выдать блокировку.\n{p}binfo - информация о блокировке.\n{p}unban - снять блокировку.',
chat_id=event.chat_id,random_id=0)
										elif msg[1] == '4' and admLvl > 3:
											vk.messages.send(
message=f'Команды администратора 4 уровня.\n\n{p}arang - выдать админ права.\n{p}ckick - кикнуть со всех бесед.',
chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{p}ahelp] [lvl]',chat_id=event.chat_id,random_id=0)

							#: Commands for 2 lvl;
							if admLvl > 1:
								if command == 'kick':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										if admLvl > ap.admLvl(event.chat_id,uid):
											reason = f"Причина:{event.obj.text.replace(f'{msg[0]} {msg[1]}','')}"
											if len(list(reason)) == 8: reason = ''
											mt = f'id{uid}' if uid > 0 else str(uid).replace('-','club')
											vk.messages.removeChatUser(chat_id=event.chat_id,member_id=uid)
											vk.messages.send(message=f'Пользователь [{mt}|{name}] был исключён из беседы.\n{reason}',
												chat_id=event.chat_id,random_id=0,attachment=ap.checkAudio(event.chat_id))
										else:
											vk.messages.send(message='Ваш уровень меньше или равен уровню пользователя.',chat_id=event.chat_id,random_id=0)
										
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}kick] [ID] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

									except vk_api.exceptions.ApiError as e:
										if e.code == 15: vk.messages.send(message='Пользователь является администратором беседы.',chat_id=event.chat_id,random_id=0)
										elif e.code == 935: vk.messages.send(message='Пользователя нету в данной беседе.',chat_id=event.chat_id,random_id=0)

								elif command == 'gc':
									proccmds += 1
									Ping = ping('vk.com').rtt_avg_ms
									uptime = ap.getUpTime()
									vk.messages.send(message=f'Информация\n\nPing: {Ping} ms\nProcessed Commands: {proccmds}\nUpTime: {uptime}',chat_id=event.chat_id,random_id=0)

								elif command == 'top':
									proccmds += 1
									top,msgs = ap.top(event.chat_id)
									vk.messages.send(disable_mentions=1,message=f'Топ пользователей по сообщениям:\n\n{top}\n\nВсего сообщений: {msgs}',chat_id=event.chat_id,random_id=0)

								elif command == 'mute':
									proccmds += 1
									try:
										if admLvl > ap.admLvl(event.chat_id,ap.getUserName(msg[1])[1]):
											reason = event.obj.text.replace(f'{msg[0]} {msg[1]} {msg[2]}','')
											reason = f'Причина:{reason}' if len(list(reason)) != 0 else ''
											text = ap.mute(event.chat_id,ap.getUserName(msg[1]),int(msg[2]),reason)
											vk.messages.send(message=text,chat_id=event.chat_id,random_id=0)

										else:
											vk.messages.send(message='Ваш уровень меньше или равен уровню пользователя.',chat_id=event.chat_id,random_id=0)

									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}mute] [ID] [Время] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

								elif command == 'unmute':
									proccmds += 1
									try:
										reason = event.obj.text.replace(f'{msg[0]} {msg[1]}','')
										reason = f'Причина:{reason}' if len(list(reason)) != 0 else ''
										text = ap.unmute(event.chat_id,ap.getUserName(msg[1]),reason)
										vk.messages.send(message=text,chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}unmute] [ID] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

								elif command == 'mt':
									proccmds += 1
									try:
										if msg[1].lower() in ['=0','=a','=а']:
											text = ap.generateMt(event.chat_id,msg[1].lower())
											name,uid = ap.getUserName(from_id)
											mention_text = event.obj.text.replace(f'{msg[0]} {msg[1]}','')
											if len(list(mention_text)) != 0:
												vk.messages.send(message=f'Упоминание пользователей администратором [id{uid}|{name}]:\n\n{text}.\n\nПричина вызова:{mention_text}',chat_id=event.chat_id,random_id=0)
											else:
												vk.messages.send(message='Вы забыли написать причину вызова.',chat_id=event.chat_id,random_id=0)

										else:
											vk.messages.send(message=f'Есть только два варианта упоминания: {msg[0][0]}mt =0 или =a.',chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}mt] [=int] [Текст]',chat_id=event.chat_id,random_id=0)

								elif command == 'get':
									proccmds += 1
									try:
										get = ap.getUserInfo(event.chat_id,msg[1])
										vk.messages.send(disable_mentions=1,message=get,chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}get] [ID]',chat_id=event.chat_id,random_id=0)

								elif command == 'warn':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										if admLvl > ap.admLvl(event.chat_id,uid):
											reason = event.obj.text.replace(f'{msg[0]} {msg[1]} {msg[2]}','')
											if int(msg[2]) > 5: vk.messages.send(message='Нельзя выдать более 6 предупреждений.',chat_id=event.chat_id,random_id=0)
											elif int(msg[2]) < 0: vk.messages.send(message='Нельзя выдать менее 0 предупреждений.',chat_id=event.chat_id,random_id=0)
											else:
												text,all_warns = ap.setWarns(event.chat_id,(name,uid),int(msg[2]),reason)
												vk.messages.send(disable_mentions=1,message=text,chat_id=event.chat_id,random_id=0,attachment=ap.checkAudio(event.chat_id))
												if all_warns == 6:
													vk.messages.removeChatUser(chat_id=event.chat_id,member_id=uid)
										else:
											vk.messages.send(message='Ваш уровень меньше или равен уровню пользователя.',chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}warn] [ID] [Кол-во] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

								elif command == 'unwarn':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										if admLvl > ap.admLvl(event.chat_id,uid):
											reason = event.obj.text.replace(f'{msg[0]} {msg[1]} {msg[2]}','')
											if int(msg[2]) > 5: vk.messages.send(message='Нельзя снять более 6 предупреждений.',chat_id=event.chat_id,random_id=0)
											elif int(msg[2]) < 0: vk.messages.send(message='Нельзя снять менее 0 предупреждений.',chat_id=event.chat_id,random_id=0)
											else:
												text = ap.endWarns(event.chat_id,(name,uid),int(msg[2]),reason)
												vk.messages.send(disable_mentions=1,message=text,chat_id=event.chat_id,random_id=0)
										else:
											vk.messages.send(message='Ваш уровень меньше или равен уровню пользователя.',chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}unwarn] [ID] [Кол-во] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

								elif command == 'warns':
									proccmds += 1
									warns,ctn = ap.warns(event.chat_id)
									if ctn != 0: vk.messages.send(disable_mentions=1,message=f'Список пользователей с предупреждениями:\n\n{warns}',chat_id=event.chat_id,random_id=0)
									else: vk.messages.send(message='Список пуст.',chat_id=event.chat_id,random_id=0)

							#: Commands for 3 lvl;
							if admLvl > 2:
								if command == 'ban':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										if admLvl > ap.admLvl(event.chat_id,uid):
											reason = event.obj.text.replace(f'{msg[0]} {msg[1]}','')
											reason,code = ap.ban(event.chat_id,uid,reason,from_id)
											if code == 1:
												vk.messages.send(disable_mentions=1,message=f'Пользователь [id{uid}|{name}] был заблокирован.\n{reason}',chat_id=event.chat_id,random_id=0,attachment=ap.checkAudio(event.chat_id))
												vk.messages.removeChatUser(chat_id=event.chat_id,member_id=uid)
											else:
												vk.messages.send(message='У пользователя уже есть блокировка.',chat_id=event.chat_id,random_id=0)
										else:
											vk.messages.send(message='Ваш уровень меньше или равен уровню пользователя.',chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}ban] [ID] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

									except vk_api.exceptions.ApiError as e:
										if e.code == 15: vk.messages.send(message='Пользователь является администратором беседы.',chat_id=event.chat_id,random_id=0)
										elif e.code == 935: vk.messages.send(message='Пользователя нету в данной беседе.',chat_id=event.chat_id,random_id=0)

								elif command == 'unban':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										reason = event.obj.text.replace(f'{msg[0]} {msg[1]}','')
										reason = f'Причина:{reason}' if len(list(reason)) != 0 else ''
										code = ap.unban(event.chat_id,uid)
										if code == 1:
											vk.messages.send(disable_mentions=1,message=f'Пользователь [id{uid}|{name}] был разблокирован.\n{reason}',chat_id=event.chat_id,random_id=0)
										else:
											vk.messages.send(message='У пользователя нету блокировок.',chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}unban] [ID] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

								elif command == 'binfo':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										binfo, code = ap.binfo(event.chat_id,uid)
										if code == 1:
											vk.messages.send(disable_mentions=1,message=f'Блокировки пользователя "[id{uid}|{name}]"\n\n{binfo}',chat_id=event.chat_id,random_id=0)
										else:
											vk.messages.send(message='У пользователя нету блокировок.',chat_id=event.chat_id,random_id=0)

									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}binfo] [ID]',chat_id=event.chat_id,random_id=0)

							#: Commands for 4 lvl;
							if admLvl > 3:
								if command == 'arang':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										if admLvl > ap.admLvl(event.chat_id,uid):
											if int(msg[2]) >= admLvl or int(msg[2]) < 0:
												if admLvl == 5:
													ap.setAdmLvl(event.chat_id,uid,msg[2])
													vk.messages.send(message=f'Пользователю [id{uid}|{name}] были выданы права администратора {msg[2]} уровня.',disable_mentions=1,chat_id=event.chat_id,random_id=0)
												else:
													vk.messages.send(message='Нельзя выдать уровень больше или равного вашему.\n Также нельзя выдать уровень менее нуля.',disable_mentions=1,chat_id=event.chat_id,random_id=0)
											else:
												ap.setAdmLvl(event.chat_id,uid,msg[2])
												vk.messages.send(message=f'Пользователю [id{uid}|{name}] были выданы права администратора {msg[2]} уровня.',disable_mentions=1,chat_id=event.chat_id,random_id=0)
										else:
											vk.messages.send(message='Ваш уровень меньше или равен уровню пользователя.',chat_id=event.chat_id,random_id=0)
									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}arang] [ID] [lvl]',chat_id=event.chat_id,random_id=0)

								elif command == 'ckick':
									proccmds += 1
									try:
										name,uid = ap.getUserName(msg[1])
										if admLvl > ap.admLvl(event.chat_id,uid):
											reason = f"Причина:{event.obj.text.replace(f'{msg[0]} {msg[1]}','')}"
											if len(list(reason)) == 8: reason = ''
											mt = f'id{uid}' if uid > 0 else str(uid).replace('-','club')
											for cid in ap.getChats():
												try:
													vk.messages.removeChatUser(chat_id=cid,member_id=uid)
												except vk_api.exceptions.ApiError:
													pass
											vk.messages.send(message=f'Пользователь [{mt}|{name}] был исключён из всех бесед.\n{reason}',
												chat_id=event.chat_id,random_id=0,attachment=ap.checkAudio(event.chat_id))
										else:
											vk.messages.send(message='Ваш уровень меньше или равен уровню пользователя.',chat_id=event.chat_id,random_id=0)

									except IndexError:
										vk.messages.send(message=f'Использование: [{msg[0][0]}ckick] [ID] [Причина(не обязательно)]',chat_id=event.chat_id,random_id=0)

					else:
						if command == 'start':
							proccmds += 1
							text = regCf(event.chat_id)
							vk.messages.send(message=text,chat_id=event.chat_id,random_id=0)

				else:
					usr = ap.getUserName(event.obj.from_id)
					if event.raw['object']['action']['type'] == 'chat_invite_user':
						usr = ap.getUserName(event.raw['object']['action']['member_id'])
						if event.raw['object']['action']['member_id'] != -199992660:
							if event.raw['object']['action']['member_id'] > 0:
								if ap.checkban(event.chat_id,usr[1]):
									vk.messages.send(message=f'У пользователя есть блокировка.\nПросмотреть блокировки: /binfo https://vk.com/id{usr[1]}',chat_id=event.chat_id,random_id=0)
									vk.messages.removeChatUser(chat_id=event.chat_id,member_id=usr[1])
									
							else:
								vk.messages.send(message='Один бот хорошо, а два лучше... Или нет?',chat_id=event.chat_id,random_id=0)
						else:
							text = ap.regCf(event.chat_id)
							vk.messages.send(message=text,chat_id=event.chat_id,random_id=0)


	except Exception:
		pass

	except requests.exceptions.ReadTimeout:
		time.sleep(30)