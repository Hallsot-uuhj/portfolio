from vk_api.bot_longpoll import VkBotLongPoll
import assets.Settings as st
import assets.apanel as ap
import vk_api, re

vk = vk_api.VkApi(token=st.TOKEN)
lp = VkBotLongPoll(vk, st.GROUP_ID)
vk = vk.get_api()
print('start')
for event in lp.listen():
	try:
		if event.raw['type'] == 'message_new':
			msg = event.obj.text.lower().split()
			if 'action' not in event.raw['object']:
				if event.obj.peer_id != event.obj.from_id:
					if ap.check_chat(event.obj.peer_id) == 1:
						adm_lvl = ap.check_users(event.obj.from_id,event.obj.peer_id,event.raw)
						ap.kick_filter(event.obj.from_id, event.obj.text, adm_lvl, event.obj.peer_id)
						if msg[0] == '/start':
							vk.messages.send(message=f"{st.TAG} Беседа уже зарегестрирована.", random_id=0, peer_id=event.obj.peer_id)

						if adm_lvl >= 1:
							if msg[0] in ['/admins', '/adms']:
								try: page =	int(msg[1])
								except IndexError: page = 1
								vk.messages.send(message=ap.admins(event.obj.peer_id,page), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)

							elif msg[0] in ['/warnlist', '/warns']:
								try: page =	int(msg[1])
								except IndexError: page = 1
								vk.messages.send(message=ap.warnlist(event.obj.peer_id,page), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)

							elif msg[0] == '/help':
								try:
									if msg[1] == '1':
										vk.messages.send(message=st.HELP[1], random_id=0, peer_id=event.obj.peer_id)
									elif msg[1] == '2':
										if adm_lvl >= 2:
											vk.messages.send(message=st.HELP[2], random_id=0, peer_id=event.obj.peer_id)
									elif msg[1] == '3':
										if adm_lvl >= 3:
											vk.messages.send(message=st.HELP[3], random_id=0, peer_id=event.obj.peer_id)
									elif msg[1] == '4':
										if adm_lvl >= 4:
											vk.messages.send(message=st.HELP[4], random_id=0, peer_id=event.obj.peer_id)
									elif msg[1] == '5':
										if adm_lvl >= 5:
											vk.messages.send(message=st.HELP[5], random_id=0, peer_id=event.obj.peer_id)
									else:
										vk.messages.send(message=f"{st.TAG} Использование: /help (Уровень<1-{adm_lvl}>).", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /help (Уровень<1-{adm_lvl}>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/kick':
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if check[0]:
										if not check[1]:
											if alvl < adm_lvl:
												try: reason = f"Причина:{event.obj.text.split(event.obj.text.split()[1])[1]}" if event.obj.text.split(event.obj.text.split()[1])[1] != '' else ''
												except IndexError: reason = ''
												vk.messages.send(message=f"{st.TAG} Пользователь {info[2]} был исключен из беседы.\n{reason}", random_id=0, peer_id=event.obj.peer_id, attachment=st.AUDIO_IN_KICK)
												vk.messages.removeChatUser(chat_id=event.chat_id, member_id=info[1])
												ap.i_history_append(-st.GROUP_ID, event.obj.peer_id, 'kick', info[1])
											else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
										else: vk.messages.send(message=f"{st.TAG} Пользователь является администратором беседы.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователя нет в беседе.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /kick (Пользователь) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/i_history':
								try:
									try: page =	int(msg[2])
									except IndexError: page = 1
									vk.messages.send(message=ap.i_history(event.obj.peer_id, ap.get_id(msg[1]), page), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /i_history (Пользователь) (Страница).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/warnings':
								try:
									try: page =	int(msg[2])
									except IndexError: page = 1
									vk.messages.send(message=ap.warnings(event.obj.peer_id, ap.get_id(msg[1]), page), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /warnings (Пользователь) (Страница).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/binfo':
								try:
									vk.messages.send(message=ap.binfo(event.obj.peer_id, ap.get_id(msg[1])), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /binfo (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/point':
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if check[0]:
										if alvl < adm_lvl:
											msgg = event.obj.text.split(); reason = event.obj.text.replace(f"{msgg[0]} {msgg[1]} {msgg[2]}", "")
											reason = f"Причина: {reason}" if len(reason) > 0 else ''
											text = ap.point(info, event.obj.peer_id, int(msg[2]), reason)
											vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
										else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователя нет в беседе.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /point (Пользователь) (Кол-во) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/points':
								try:
									vk.messages.send(message=ap.points(event.obj.peer_id, msg[1]), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
								except IndexError:
									vk.messages.send(message=ap.points(event.obj.peer_id, 1), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)

						if adm_lvl >= 2:
							if msg[0] == '/mention':
								text = event.obj.text.replace('/mention', '')
								if len(text) > 0:
									info = vk.messages.getConversationMembers(peer_id=event.obj.peer_id, group_id=st.GROUP_ID)['profiles']
									mentions = ', '.join(f"[id{x['id']}|{x['first_name'][0]}. {x['last_name']}]" for x in info if x['id'] != event.obj.from_id)
									vk.messages.send(message=f"{st.TAG} Упоминание пользователей:\n\nУпомянувшие: {mentions}.\n\nУпомянул: {ap.get_username(event.obj.from_id)[2]}\nПричина:{text}",peer_id=event.obj.peer_id,random_id=0)
								else:
									vk.messages.send(message=f"{st.TAG} Укажите причину вызова.", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/ckick':
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if not check[1]:
										if alvl < adm_lvl:
											try: reason = f"Причина:{event.obj.text.split(event.obj.text.split()[1])[1]}" if event.obj.text.split(event.obj.text.split()[1])[1] != '' else ''
											except IndexError: reason = ''
											vk.messages.send(message=f"{st.TAG} Пользователь {info[2]} был исключен из всех локальных бесед.\n{reason}", random_id=0, peer_id=event.obj.peer_id, attachment=st.AUDIO_IN_KICK)
											_, chat_ids = ap.get_local_chats(event.obj.peer_id); chat_ids.append(event.obj.peer_id)
											for x in chat_ids:
												try:
													vk.messages.removeChatUser(chat_id=x-2000000000, member_id=info[1])
													ap.i_history_append(-st.GROUP_ID, x, 'kick', info[1])
												except: pass
										else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователь является администратором беседы.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /ckick (Пользователь) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/mute':
								try:
									info,m_time = ap.get_username(msg[1]),int(msg[2])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if check[0]:
										if not check[1]:
											if alvl < adm_lvl:
												if m_time <= 1440 and m_time > 0:
													msg = event.obj.text.split()
													reason = event.obj.text.replace(f"{msg[0]} {msg[1]} {msg[2]}", "")
													text = ap.set_mute(info, event.obj.peer_id, m_time*60, reason, event.obj.from_id)
													vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
												else: vk.messages.send(message=f"{st.TAG} Максимальное время мута не более 1440 минут(1 день) и не менее 0 минут.", random_id=0, peer_id=event.obj.peer_id)
											else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
										else: vk.messages.send(message=f"{st.TAG} Пользователь является администратором беседы.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователя нет в беседе.", random_id=0, peer_id=event.obj.peer_id)
								except (IndexError, ValueError):
									vk.messages.send(message=f"{st.TAG} Использование: /mute (Пользователь) (Время<до 1440 минут>) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/unmute':
								try:
									info = ap.get_username(msg[1]);alvl = ap.check_users(info[1],event.obj.peer_id)
									if alvl < adm_lvl:
										text = ap.del_mute(info, event.obj.peer_id)
										vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
								except (IndexError, ValueError):
									vk.messages.send(message=f"{st.TAG} Использование: /unmute (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/get':
								try:
									vk.messages.send(message=ap.get(event.obj.peer_id, ap.get_id(msg[1])), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /get (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/warn':
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if check[0]:
										if not check[1]:
											if alvl < adm_lvl:
												if int(msg[2]) >= 0:
													if int(msg[2]) <= 6:
														msg = event.obj.text.split(); reason = event.obj.text.replace(f"/warn {msg[1]} {msg[2]}", "")
														text = ap.set_warn('warn', info, event.obj.peer_id, reason, int(msg[2]), event.obj.from_id)
														vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
													else: vk.messages.send(message=f"{st.TAG} Кол-во предупреждений должно быть не более 6.", random_id=0, peer_id=event.obj.peer_id)
												else: vk.messages.send(message=f"{st.TAG} Кол-во предупреждений должно быть не меньше нуля.", random_id=0, peer_id=event.obj.peer_id)
											else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
										else: vk.messages.send(message=f"{st.TAG} Пользователь является администратором беседы.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователя нет в беседе.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /warn (Пользователь) (Кол-во) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/unwarn':
								try:
									info = ap.get_username(msg[1])
									alvl = ap.check_users(info[1],event.obj.peer_id)
									if alvl < adm_lvl:
										if int(msg[2]) >= 0:
											if int(msg[2]) <= 6:
												msg = event.obj.text.split(); reason = event.obj.text.replace(f"/unwarn {msg[1]} {msg[2]}", "")
												text = ap.set_warn('unwarn', info, event.obj.peer_id, reason, int(msg[2]), event.obj.from_id)
												vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
											else: vk.messages.send(message=f"{st.TAG} Кол-во снимаемых предупреждений должно быть не более 6.", random_id=0, peer_id=event.obj.peer_id)
										else: vk.messages.send(message=f"{st.TAG} Кол-во снимаемых предупреждений должно быть не меньше нуля.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /unwarn (Пользователь) (Кол-во) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/domain':
								try:
									if msg[1] in 'set':
										try:
											info = ap.get_username(msg[2]); ap.check_users(info[1],event.obj.peer_id); msg = event.obj.text.split(' ')
											text = event.obj.text.replace(f"{msg[0]} {msg[1]} {msg[2]}", "")[1:]
											if len(text) > 30:vk.messages.send(message=f"{st.TAG} в нике должно быть не более 30 символов.", random_id=0, peer_id=event.obj.peer_id)
											elif len(text) > 0:vk.messages.send(message=ap.domain(event.obj.peer_id,'set',info,text), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
											else:vk.messages.send(message=f"{st.TAG} укажите никнейм.", random_id=0, peer_id=event.obj.peer_id)
										except IndexError:
											vk.messages.send(message=f"{st.TAG} Использование: /domain set (Пользователь) (Никнейм).", random_id=0, peer_id=event.obj.peer_id)
									elif msg[1] == 'del':
										try:
											info = ap.get_username(msg[2])
											text = ap.domain(event.obj.peer_id,'del',info)
											vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
										except IndexError:
											vk.messages.send(message=f"{st.TAG} Использование: /domain del (Пользователь).", random_id=0, peer_id=event.obj.peer_id)
									elif msg[1] == 'list':
										page = 0
										try: page = int(msg[2])
										except IndexError: page = 1
										text = ap.domain(event.obj.peer_id,'list',page=page)
										vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
									else:
										vk.messages.send(message=f"{st.TAG} Типы команды domain:\n\n1. <<set (Пользователь) (Никнейм)>> - установить ник пользователю.\n2. <<del (Пользователь)>> - удалить ник пользователю.\n3. <<list (Страница)>> - список пользователей с никами.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /domain (Тип).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/a_invite':
								try:
									info = ap.get_username(msg[1]); ap.check_users(info[1],event.obj.peer_id)
									check, aiid = ap.checker(info[1],event.obj.peer_id)[0], ap.a_invite_ID(info, event.obj.peer_id)
									if not check:
										if aiid == 0:
											vk.messages.send(message=ap.a_invite(info, event.obj.peer_id, event.obj.from_id, 1), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
										else: vk.messages.send(message=f"{st.TAG} Пользователь уже помечен как приглашённый.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователь уже есть в беседе.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /a_invite (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

						if adm_lvl >= 3:
							if msg[0] == '/greeting':
								try:
									if msg[1] == 'set':
										text = event.obj.text.split('set')[1]
										if len(text) > 0:vk.messages.send(message=ap.greeting(event.obj.peer_id,'set',ap.emoji.demojize(text)), random_id=0, peer_id=event.obj.peer_id)
										else:vk.messages.send(message=f"{st.TAG} Использование: /greeting set (Текст).", random_id=0, peer_id=event.obj.peer_id)
									else:
										text = ap.greeting(event.obj.peer_id,msg[1])
										if len(text) == 0: text = f'{st.TAG} Приветствие отсутствует.'
										if st.TAG not in text: text = f"{st.TAG} Текущее приветствие:\n\n{text}"
										vk.messages.send(message=ap.emoji.emojize(text), random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /greeting (Тип).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/a_role':
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)[0]
									if check:
										if alvl < adm_lvl:
											if int(msg[2]) < adm_lvl:
												ap.a_role(event.obj.peer_id, info[1], msg[2])
												vk.messages.send(message=f"{st.TAG} Пользователю {info[2]} были выданы права администратора {msg[2]} уровня.", random_id=0, peer_id=event.obj.peer_id)
											else: vk.messages.send(message=f"{st.TAG} Вы не можете выдать права администратора выше или равного вашим.", random_id=0, peer_id=event.obj.peer_id)				
										else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователя нет в беседе.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /a_role (Пользователь) (Уровень).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/pm':
								try:
									if ap.if_local(event.obj.peer_id):
										text = event.obj.text.split(msg[1])[1]
										if len(text) > 0:
											_, chat_ids = ap.get_local_chats(event.obj.peer_id)
											if int(msg[1])+2000000000 in chat_ids:
												vk.messages.send(message=f"Новое сообщение из беседы[ID:{event.chat_id}]\n\nСообщение: {text}\nОтправил: {ap.get_username(event.obj.from_id)[2]}", random_id=0, chat_id=int(msg[1]))
												vk.messages.send(message=f"{st.TAG} Сообщение отправлено.", random_id=0, chat_id=event.chat_id)
											else:
												if int(msg[1]) == event.chat_id:
													vk.messages.send(message=f"{st.TAG} Нельзя отправить сообщение в эту же беседу.", random_id=0, peer_id=event.obj.peer_id)
												else:
													vk.messages.send(message=f"{st.TAG} Данная беседа не подключена к вашей локализации.", random_id=0, peer_id=event.obj.peer_id)
										else:
											vk.messages.send(message=f"{st.TAG} Введите сообщение.", random_id=0, peer_id=event.obj.peer_id)
									else:
										vk.messages.send(message=f"{st.TAG} Ваша беседа не подключена к локализации.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									text, _ = ap.get_local_chats(event.obj.peer_id)
									vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/consists':
								try:
									text = ap.consists(ap.get_id(msg[1]))
									vk.messages.send(message=text,peer_id=event.obj.peer_id,random_id=0)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /consists (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/filter':
								try:
									if msg[1] in ['add', 'del']:
										text = event.obj.text.split(msg[1])[1][1:]
										text = text.split(', ') if ',' in text else text.split(' ')
										chheck = True
										for x in text:
											if len(x)>15:
												chheck = False
												vk.messages.send(message=f"{st.TAG} в слове должно быть не более 15 символов.", random_id=0, peer_id=event.obj.peer_id)
												break
										if chheck:
											if len(text) > 0:vk.messages.send(message=ap.filter(event.obj.peer_id,msg[1],text), random_id=0, peer_id=event.obj.peer_id)
											else:vk.messages.send(message=f"{st.TAG} Использование: /filter {msg[1]} (Слово<а>).", random_id=0, peer_id=event.obj.peer_id)
									elif msg[1] == 'list':
										text = ap.filter(event.obj.peer_id,'list')
										vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
									else:
										vk.messages.send(message=f"{st.TAG} Типы команды filter:\n\n1. <<add (Слово<а>)>> - добавить в фильтр слово<а>.\n2. <<del (Слово<а>)>> - убрать из фильтра слово<а>.\n3. <<list>> - список слов в фильтре.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /filter (Тип).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] in ['/ban', '/cban']:
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if not check[1]:
										if alvl < adm_lvl:
											msg = event.obj.text.split()
											reason = event.obj.text.replace(f"{msg[0]} {msg[1]}", "")
											text = ap.set_ban(msg[0][1:], info, event.obj.peer_id, reason, event.obj.from_id)
											vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
										else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователь является администратором беседы.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: {msg[0]} (Пользователь) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] in ['/unban', '/uncban']:
								try:
									info = ap.get_username(msg[1])
									text = ap.del_ban(msg[0][3:], info, event.obj.peer_id)
									vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: {msg[0]} (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/c_invite':
								try:
									info = ap.get_username(msg[1]); ap.check_users(info[1],event.obj.peer_id)
									check, aiid = ap.checker(info[1],event.obj.peer_id)[0], ap.a_invite_ID(info, event.obj.peer_id)
									if not check:
										if aiid == 1:
											vk.messages.send(message=ap.a_invite(info, event.obj.peer_id, event.obj.from_id, 0), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
										else: vk.messages.send(message=f"{st.TAG} Пользователь и так не был помечен как приглашённый.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователь уже есть в беседе.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /c_invite (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

						if adm_lvl >= 4:
							if msg[0] == '/rasform':
								info = vk.messages.getConversationMembers(peer_id=event.obj.peer_id, group_id=st.GROUP_ID)['items']
								[
									(
										vk.messages.removeChatUser(chat_id=event.chat_id, member_id=x['member_id']), 
										ap.i_history_append(-st.GROUP_ID, event.obj.peer_id, 'kick', x['member_id'])
									) 
									for x in info 
									if (
										ap.check_users(x['member_id'],event.obj.peer_id) <= 0 and 
										x['member_id'] != -st.GROUP_ID and
										not ap.checker(x['member_id'],event.obj.peer_id)[1]
										)
								]
								vk.messages.send(message=f"{st.TAG} Беседа успешно расформирована.", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/local':
								try:
									text = ap.local(msg[1], event.raw)
									vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /local (Тип).", random_id=0, peer_id=event.obj.peer_id)

						if adm_lvl >= 5:
							if msg[0] == '/logs':
								try:
									with open(st.PATH_LOGS, 'r') as f: txt = f.read()
									txt = re.findall(r'<cid={0}>.+'.format(event.chat_id), txt)
									logs = '\n'.join(txt[i] for i in range(len(txt)-int(msg[1]), len(txt)))
									vk.messages.send(message=f'{st.TAG} Последние {msg[1]} сообщений:\n\n'+ap.emoji.emojize(re.sub(r'<.+>', '', logs)), random_id=0, peer_id=event.obj.peer_id, disable_mentions=1)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /logs (Кол-во).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/gkick':
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if not check[1]:
										if alvl < adm_lvl:
											try: reason = f"Причина:{event.obj.text.split(event.obj.text.split()[1])[1]}" if event.obj.text.split(event.obj.text.split()[1])[1] != '' else ''
											except IndexError: reason = ''
											vk.messages.send(message=f"{st.TAG} Пользователь {info[2]} был исключен во всех беседах.\n{reason}", random_id=0, peer_id=event.obj.peer_id, attachment=st.AUDIO_IN_KICK)
											chat_ids = ap.get_global_chats();
											for x in chat_ids:
												try:
													vk.messages.removeChatUser(chat_id=x-2000000000, member_id=info[1])
													ap.i_history_append(-st.GROUP_ID, x, 'kick', info[1])
												except: pass
										else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователь является администратором беседы.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /gkick (Пользователь) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/gban':
								try:
									info = ap.get_username(msg[1])
									alvl,check = ap.check_users(info[1],event.obj.peer_id),ap.checker(info[1],event.obj.peer_id)
									if not check[1]:
										if alvl < adm_lvl:
											msg = event.obj.text.split()
											reason = event.obj.text.replace(f"{msg[0]} {msg[1]}", "")
											text = ap.set_ban('gban', info, event.obj.peer_id, reason, event.obj.from_id)
											vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
										else: vk.messages.send(message=f"{st.TAG} Права администратора пользователя выше или равны вашим.", random_id=0, peer_id=event.obj.peer_id)
									else: vk.messages.send(message=f"{st.TAG} Пользователь является администратором беседы.", random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /gban (Пользователь) (Причина<не обязательно>).", random_id=0, peer_id=event.obj.peer_id)

							elif msg[0] == '/ungban':
								try:
									info = ap.get_username(msg[1])
									text = ap.del_ban('gban', info, event.obj.peer_id)
									vk.messages.send(message=text, random_id=0, peer_id=event.obj.peer_id)
								except IndexError:
									vk.messages.send(message=f"{st.TAG} Использование: /ungban (Пользователь).", random_id=0, peer_id=event.obj.peer_id)

					else:
						if msg[0] == '/start':
							ap.reg_chat(event.obj.peer_id)
							vk.messages.send(message=f"{st.TAG} Беседа успешно зарегестрирована.", random_id=0, peer_id=event.obj.peer_id)
				else:
					if msg[0] == '/check_gban':
						text = ap.check_bans(event.obj.peer_id, 0, True)
						vk.messages.send(message=text, user_id=event.obj.from_id, random_id=0)

			else:
				if ap.check_chat(event.obj.peer_id) == 1:
					adm_lvl = ap.check_users(event.obj.from_id,event.obj.peer_id)
					type = event.raw['object']['action']['type']
					member_id = event.raw['object']['action']['member_id']
					if type in [
					'chat_invite_user', 'chat_kick_user', 'chat_invite_user_by_link']:
						if type.split('_')[1] == 'invite':
							aiid = ap.a_invite_ID(ap.get_username(member_id), event.obj.peer_id)
							if adm_lvl > 0:
								if aiid == 0:
									ap.i_history_append(
										event.obj.from_id, event.obj.peer_id, 
										'invite', member_id)
								inff = ap.check_bans(member_id, event.obj.peer_id)[0]
								if not inff:
									greeting = ap.greeting(event.obj.peer_id,"get")
									if len(greeting) > 0:
										vk.messages.send(message=f'{st.TAG} Приветствуем тебя - {ap.get_username(member_id)[2]}\n\n{ap.emoji.emojize(greeting)}', random_id=0, peer_id=event.obj.peer_id, attachment=st.AUDIO_IN_GREETING)
								else:
									s_id = f"id{member_id}" if member_id > 0 else f"club{member_id*-1}"
									vk.messages.send(message=f"{st.TAG} Пользователь {ap.get_username(member_id)[2]} был исключен из беседы так как забанен.\n\nЧтобы просмотреть блокировки: /binfo vk.com/{s_id}", random_id=0, peer_id=event.obj.peer_id)
									vk.messages.removeChatUser(chat_id=event.chat_id, member_id=member_id)
							else:
								if aiid == 0:
									vk.messages.removeChatUser(chat_id=event.chat_id, member_id=member_id)
									vk.messages.removeChatUser(chat_id=event.chat_id, member_id=event.obj.from_id)
								else:
									ap.a_invite(ap.get_username(member_id), event.obj.peer_id, event.obj.from_id, 0)
									inff = ap.check_bans(member_id, event.obj.peer_id)[0]
									if not inff:
										greeting = ap.greeting(event.obj.peer_id,"get")
										if len(greeting) > 0:
											vk.messages.send(message=f'{st.TAG} Приветствуем тебя - {ap.get_username(member_id)[2]}\n\n{ap.emoji.emojize(greeting)}', random_id=0, peer_id=event.obj.peer_id, attachment=st.AUDIO_IN_GREETING)
									else:
										s_id = f"id{member_id}" if member_id > 0 else f"club{member_id*-1}"
										vk.messages.send(message=f"{st.TAG} Пользователь {ap.get_username(member_id)[2]} был исключен из беседы так как забанен.\n\nЧтобы просмотреть блокировки: /binfo vk.com/{s_id}", random_id=0, peer_id=event.obj.peer_id)
										vk.messages.removeChatUser(chat_id=event.chat_id, member_id=member_id)
						else:
							ap.i_history_append(
								event.obj.from_id, event.obj.peer_id, 
								'kick', member_id)
							if event.obj.from_id == member_id:
								vk.messages.removeChatUser(chat_id=event.chat_id, member_id=member_id)

	except Exception as e:
		if st.DEBUG:
			print('DEBUG - произошла ошибка после данного сообщения:')
			print(f'[{ap.date(int(ap.time.time()))}] {ap.get_username(event.obj.from_id)[0]}: {event.obj.text}\n')
			print('ERROR:', e)