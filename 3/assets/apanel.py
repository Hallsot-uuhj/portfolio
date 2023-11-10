from datetime import datetime
import pymysql.cursors, requests
import vk_api, re, time, emoji
from . import Settings as st

vk = vk_api.VkApi(token=st.TOKEN)
vk = vk.get_api()
conn = lambda: pymysql.connect(host='localhost', user='root', password='root', db='vkbot', cursorclass=pymysql.cursors.DictCursor)
title = lambda pid: vk.messages.getConversationsById(peer_ids=pid,group_id=st.GROUP_ID)['items'][0]['chat_settings']['title']

def date(unix):
	unix = datetime.fromtimestamp(unix)
	return unix.strftime("%H:%M - %d.%m.%y")

def get_id(id):
	if isinstance(id,int):
		return id
	if 'https' in id:
		check = id.replace('https://vk.com/','')
		if 'id' in check:
			return int(check.replace('id', ''))
		elif 'club' in check:
			return int(check.replace('club', '-'))
		else:
			return int(vk.utils.resolveScreenName(screen_name=check)['object_id'])
	elif 'id' in id:
		return int(re.findall(r'id\d+', id)[0].replace('id',''))
	elif 'club' in id:
		return int(re.findall(r'club\d+', id)[0].replace('club','-'))

def get_username(uid, nc='nom'):
	id = get_id(uid)
	if id < 0:
		id *= -1
		inf = vk.groups.getById(group_id=id)[0]
		return f"{inf['name']}", id, f"[club{id}|{inf['name']}]"
	elif id > 0:
		inf = vk.users.get(user_ids=id, name_case=nc)[0]
		return f"{inf['first_name'][0]}. {inf['last_name']}", id, f"[id{id}|{inf['first_name'][0]}. {inf['last_name']}]" 

def datereg(uid):
	params = {'id': uid}
	r = requests.post('https://vk.com/foaf.php', params=params)
	datereg = re.findall(r'dc:date=".+">', str(r.content))[0].split("\"")[1].replace('+03:00', '').replace('T', ' ')
	return datereg

def check_chat(peer_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			return curl.execute(f'SELECT * FROM `chats` WHERE peer_id={peer_id}')
	finally:connect.close()

def check_users(user_id,peer_id, event=False):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `users` WHERE user_id={user_id} AND peer_id={peer_id}')
			inf = curl.fetchone()
			if event:
				curl.execute(f'UPDATE `users` SET last_msg={int(time.time())} WHERE user_id={user_id} AND peer_id={peer_id}')
				with open(st.PATH_LOGS, 'r') as f: txt = f.read()
				with open(st.PATH_LOGS, 'w') as f:
					date = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
					f.write(f'{txt}<cid={event["object"]["peer_id"]-2000000000}>[{date}] {get_username(event["object"]["from_id"])[2]}: {emoji.demojize(event["object"]["text"])}\n')
				rsult = curl.execute(f'SELECT * FROM `mutes` WHERE user_id={user_id} AND peer_id={peer_id}')
				if rsult > 0:
					if curl.fetchone()['end_date'] <= int(time.time()):
						curl.execute(f'DELETE FROM `mutes` WHERE user_id={user_id} AND peer_id={peer_id}')
					else:
						i_history_append(-st.GROUP_ID, peer_id, 'kick', user_id)
						vk.messages.send(message=f"{st.TAG} Пользователь {get_username(user_id)[2]} был исключен из беседы.\nПричина: блокировка чата.", random_id=0, peer_id=peer_id)
						vk.messages.removeChatUser(chat_id=peer_id-2000000000, member_id=user_id)
			if res > 0:
				return inf['admin']
			else:
				curtime = int(time.time())
				if user_id not in st.ADMIN_IDS:
					curl.execute(f'INSERT INTO `users`(user_id,peer_id,admin,first_date,last_msg) VALUES({user_id}, {peer_id}, 0, {curtime}, {curtime})')
					return 0
				else:
					curl.execute(f'INSERT INTO `users`(user_id,peer_id,admin,first_date,last_msg) VALUES({user_id}, {peer_id}, 5, {curtime}, {curtime})')
					return 5
	finally:
		connect.commit()
		connect.close()

def kick_filter(user_id, msg, lvl, peer_id):
	for x in get_filter(peer_id):
		if x in msg.lower() and lvl <= 0:
			i_history_append(-st.GROUP_ID, peer_id, 'kick', user_id)
			vk.messages.send(message=f"{st.TAG} Пользователь {get_username(user_id)[2]} был исключен из беседы.\nПричина: использование слов в фильтре.", random_id=0, peer_id=peer_id)
			vk.messages.removeChatUser(chat_id=peer_id-2000000000, member_id=user_id)

def join_date(user_id, peer_id):
	items = vk.messages.getConversationMembers(peer_id=peer_id,group_id=st.GROUP_ID)['items']
	join_date = [item['join_date'] for item in items if item['member_id'] == user_id]
	return date(join_date[0])

def checker(user_id,peer_id):
	m = vk.messages.getConversationMembers(peer_id=peer_id,group_id=st.GROUP_ID)['items']
	members = [x['member_id'] for x in m]
	chat = vk.messages.getConversationsById(peer_ids=peer_id,group_id=st.GROUP_ID)['items'][0]['chat_settings']
	return user_id in members, user_id in chat['admin_ids']

def reg_chat(peer_id, lvl=4):
	owner_id = vk.messages.getConversationsById(peer_ids=peer_id,group_id=st.GROUP_ID)['items'][0]['chat_settings']['owner_id']
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'INSERT INTO `chats`(peer_id,greeting) VALUES({peer_id}, \'\')')
			curl.execute(f'INSERT INTO `users`(user_id,peer_id,admin) VALUES({owner_id}, {peer_id}, {lvl})')
	finally:
		connect.commit()
		connect.close()

def admins(peer_id, page):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'SELECT * FROM `users` WHERE peer_id={peer_id} AND admin>0')
			row = curl.fetchall()
			ni0,ni1,ni2 = page*st.RIC-st.RIC,page*st.RIC,round(len(row)/st.RIC,1)
			ni1 = len(row) if ni1 > len(row) else ni1
			ni2 = int(ni2)+1 if str(ni2)[-1] != '0' else int(ni2)
			if page <= ni2 and page > 0:
				message = '\n'.join(f"{x+1}. {get_username(row[x]['user_id'])[2]} - {row[x]['admin']} lvl." for x in range(ni0,ni1))
				return f"{st.TAG} Список администрации беседы:\n<<Страница: {page}/{ni2}>>\n\n{message}"
			else:return f"{st.TAG} Такой страницы не существует."
	finally:connect.close()

def i_history_append(by, peer_id, type, user_id):
	if type == 'invite': check_users(user_id, peer_id)
	connect = conn()
	try:
		with connect.cursor() as curl:curl.execute(f'INSERT INTO `invites`(uid,peer_id,time,type,`by`) VALUES({user_id}, {peer_id}, {int(time.time())},\'{type}\',{by})')
	finally:
		connect.commit(); connect.close()

def i_history(peer_id,user_id,page):
	connect = conn()
	dict_ = {'invite': 'Приглашён', 'kick': 'Исключён'}
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `invites` WHERE uid={user_id} AND peer_id={peer_id}')
			row = curl.fetchall()
			if res > 0:
				ni0,ni1,ni2 = page*st.RIC-st.RIC,page*st.RIC,round(len(row)/st.RIC,1)
				ni1 = len(row) if ni1 > len(row) else ni1
				ni2 = int(ni2)+1 if str(ni2)[-1] != '0' else int(ni2)
				if page <= ni2 and page > 0:
					message = '\n'.join(f"{dict_[row[x]['type']]} {get_username(row[x]['by'], 'ins')[2]} - <{date(row[x]['time'])}>" for x in range(ni0,ni1))
					return f'{st.TAG} Список приглашений пользователя:\n<<Страница: {page}/{ni2}>>\n\n{message}'
				else:return f"{st.TAG} Такой страницы не существует."
			else:return f"{st.TAG} Список пуст."
	finally:connect.close()

def greeting(peer_id, type, greet=''):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'SELECT * FROM `chats` WHERE peer_id={peer_id}')
			row = curl.fetchone()
			if type.lower() == 'get':
				return row['greeting']
			elif type.lower() == 'set':
				curl.execute(f'UPDATE `chats` SET greeting=\'{greet}\' WHERE peer_id={peer_id}')
				connect.commit()
				return f"{st.TAG} Приветствие успешно установлено."
			elif type.lower() == 'del':
				curl.execute(f'UPDATE `chats` SET greeting=\'\' WHERE peer_id={peer_id}')
				connect.commit()
				return f"{st.TAG} Приветствие успешно удалено."
			else:
				return f"{st.TAG} Все параметры:\n<<set (Текст)>> - установить приветствие.\n<<get>> - получить текущее приветствие.\n<<del>> - удалить приветствие."
	finally:connect.close()

def a_role(peer_id, user_id, lvl):
	check_users(user_id,peer_id)
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'UPDATE `users` SET admin={lvl} WHERE user_id={user_id} AND peer_id={peer_id}')
	finally:
		connect.commit()
		connect.close()

def if_local(peer_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f"SELECT * FROM `chats` WHERE peer_id={peer_id}")
			lid = curl.fetchone()['lid']
			if lid == 0:
				return None
			else:
				return lid
	finally:
		connect.close()

def local(type, event):
	msg = event['object']['text'].lower().split()
	from_id = event['object']['from_id']
	peer_id = event['object']['peer_id']
	chat_id = event['object']['peer_id'] - 2000000000
	connect = conn()
	try:
		with connect.cursor() as curl:
			if type == 'create':
				curl.execute(F"SELECT * FROM `chats` WHERE peer_id={peer_id}")
				if curl.fetchone()['lid'] == 0:
					curl.execute(F"SELECT MAX(lid) FROM `chats`")
					max_lid = curl.fetchone()['MAX(lid)']
					curl.execute(f'UPDATE `chats` SET lid={max_lid+1}, local_owner=True WHERE peer_id={peer_id}')
					connect.commit()
					return f"{st.TAG} Локализация под номером [{max_lid+1}] успешно создана в данной беседе[ID: {chat_id}]."
				else:
					return f"{st.TAG} Локализация уже создана."

			elif type == 'add':
				try:
					additionID = int(msg[2])
					res = curl.execute(F"SELECT * FROM `chats` WHERE peer_id={additionID+2000000000}")
					if res > 0:
						if curl.fetchone()['lid'] == 0:
							curl.execute(F"SELECT * FROM `chats` WHERE peer_id={peer_id}")
							row = curl.fetchone()
							if row['local_owner'] == 1:
								lid = row['lid']
								curl.execute(f'UPDATE `chats` SET lid={lid} WHERE peer_id={additionID+2000000000}')
								connect.commit()
								return f"{st.TAG} Беседа[ID:{additionID}] добавлена к локализации под номером {lid}."
							else:
								return f"{st.TAG} Добавлять беседы к локализации можно только из основной беседы."
						else:
							return f"{st.TAG} Беседа уже привязана к локализации."
					else:
						return f"{st.TAG} Беседы с таким идентификатором не существует."
				except IndexError:
					return f"{st.TAG} Вы не указали ID беседы."

			elif type == 'info':
				curl.execute(F"SELECT * FROM `chats` WHERE peer_id={peer_id}")
				row = curl.fetchone()
				local_info = f'Привязан[№ {row["lid"]}].' if row['lid'] != 0 else 'Не привязан.'
				res = curl.execute(F"SELECT * FROM `chats` WHERE lid={row['lid']} AND local_owner=True")
				row2 = curl.fetchone()
				owner_chat = f'Основная беседа: {title(row2["peer_id"])} [ID: {row2["peer_id"]-2000000000}].\n' if res > 0 else ''
				this_chat = f"{title(peer_id)} [ID: {chat_id}]."
				chat_counts = curl.execute(F"SELECT * FROM `chats` WHERE lid={row['lid']}")
				return f"{st.TAG} Информация о локализации:\n\nЛокализация: {local_info}\n{owner_chat}Беседа: {this_chat}\n\nВсего бесед: {chat_counts}"

			else:
				return f"{st.TAG} Данного типа не существует.\nВсе типы команды local:\n\ncreate - создать локализацию.\nadd (Беседа) - добавить локализацию.\ninfo - информация о локализации."
	finally:
		connect.close()

def get_local_chats(peer_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f"SELECT * FROM `chats` WHERE peer_id={peer_id}")
			lid = curl.fetchone()['lid']
			if lid != 0:
				curl.execute(f"SELECT * FROM `chats` WHERE lid={lid}")
				chat_ids = [x['peer_id'] for x in curl.fetchall()]; chat_ids.remove(peer_id)
				chats = '\n'.join(F"{title(x)} - [ID: {x-2000000000}]" for x in chat_ids)
				return f"{st.TAG} Список локальных бесед:\n\n{chats}\n\nЧтобы отправить сообщение -> /pm (Беседа) (Сообщение)", chat_ids
			else:
				return None, None
	finally:
		connect.close()

def get_global_chats():
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f"SELECT * FROM `chats`")
			chat_ids = [x['peer_id'] for x in curl.fetchall()]
			return chat_ids
	finally:
		connect.close()

def consists(user_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `users` WHERE user_id={user_id}')
			chats = '\n'.join(f"<<{title(x['peer_id'])}>> [ID: {x['peer_id']-2000000000}]" for x in curl.fetchall())
			return f"{st.TAG} Список бесед пользователя:\n\n{chats}\n\nВсего бесед: {res}"
	finally:
		connect.close()

def set_mute(info, peer_id, s_time, reason, by):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `mutes` WHERE user_id={info[1]} AND peer_id={peer_id}')
			if res == 0:
				end_date = int(time.time() + s_time)
				rsn = '-' if len(reason) == 0 else reason
				curl.execute(f"INSERT INTO `mutes`(user_id, peer_id, end_date, date, `by`, reason) VALUES({info[1]}, {peer_id}, {end_date}, {int(time.time())}, {by}, '{rsn}')")
				connect.commit()
				reason = f"Причина: {reason}" if len(reason) > 0 else ''
				return f"{st.TAG} Пользователь {info[2]} получил блокировку чата на {s_time//60} минут.\n\nВремя разблокировки: {date(end_date)}\n{reason}"
			else:
				row = curl.fetchone()
				return f"{st.TAG} У пользователя {info[2]} уже есть блокировка чата.\n\nВыдал: {get_username(row['by'])[2]}\nВыдано: {date(row['date'])}\nВремя разблокировки: {date(row['end_date'])}\nПричина: {row['reason']}"
	finally:
		connect.close()

def del_mute(info, peer_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `mutes` WHERE user_id={info[1]} AND peer_id={peer_id}')
			if res > 0:
				curl.execute(f'DELETE FROM `mutes` WHERE user_id={info[1]} AND peer_id={peer_id}')
				connect.commit()
				return f"{st.TAG} Пользователю {info[2]} была снята блокировка чата."
			else:
				return f"{st.TAG} У пользователя {info[2]} нету блокировка чата."
	finally:
		connect.close()

def set_ban(type, info, peer_id, reason, by):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `bans` WHERE user_id={info[1]} AND peer_id={peer_id} AND type=\'{type}\'')
			if res == 0:
				rsn = '-' if len(reason) == 0 else reason
				curl.execute(f"INSERT INTO `bans`(user_id, peer_id, type, date, `by`, reason) VALUES({info[1]}, {peer_id}, '{type}', {int(time.time())}, {by}, '{rsn}')")
				connect.commit()
				reason = f"Причина: {reason}" if len(reason) > 0 else ''
				return f"{st.TAG} Пользователь {info[2]} получил блокировку.\n{reason}"
			else:
				s_id = f"id{info[1]}" if info[1] > 0 else f"club{info[1]*-1}"
				return f"{st.TAG} У пользователя {info[2]} уже есть блокировка.\n\nЧтобы просмотреть блокировки: /binfo vk.com/{s_id}"
	finally:
		connect.close()
		if type == 'ban':
			try:vk.messages.removeChatUser(chat_id=peer_id-2000000000, member_id=info[1])
			except:pass
		elif type == 'cban':
			locals = get_local_chats(peer_id)[1]; locals.append(peer_id)
			for x in locals:
				try:
					vk.messages.removeChatUser(chat_id=x-2000000000, member_id=info[1])
					i_history_append(-st.GROUP_ID, x, 'kick', info[1])
				except:pass
		elif type == 'gban':
			globals = get_global_chats()
			for x in globals:
				try:
					vk.messages.removeChatUser(chat_id=x-2000000000, member_id=info[1])
					i_history_append(-st.GROUP_ID, x, 'kick', info[1])
				except:pass

def check_bans(user_id, peer_id, gban=False):
	connect = conn()
	try:
		with connect.cursor() as curl:
			checks = ''
			res = curl.execute(f"SELECT * FROM `bans` WHERE user_id={user_id} AND type='gban'")
			row = curl.fetchone()
			if gban:
				if res > 0:
					return f"{st.TAG} Информация о блокировке\n\nПользователь: {get_username(user_id)[2]}\nВыдал: {get_username(row['by'])[2]}\nДата и время: {date(row['date'])}"
				else:
					return f"{st.TAG} Блокировка отсутствует."
			else:
				lid = if_local(peer_id)
				res2 = curl.execute(f"SELECT * FROM `bans` WHERE user_id={user_id} AND peer_id={peer_id} AND type='ban'")
				row2 = curl.fetchone()
				if res > 0:
					checks += f"Тип: gban\nВыдал: {get_username(row['by'])[2]}\nВыдано: {date(row['date'])}\nПричина: {row['reason']}\n\n"
				if res2 > 0:
					checks += f"Тип: ban\nВыдал: {get_username(row2['by'])[2]}\nВыдано: {date(row2['date'])}\nПричина: {row2['reason']}\n\n"
				if lid:
					res = curl.execute(f"SELECT * FROM `bans` WHERE user_id={user_id} AND type='cban'")
					if res > 0:
						for x in curl.fetchall():
							curl.execute(f"SELECT * FROM `chats` WHERE peer_id={x['peer_id']}")
							if lid == curl.fetchone()['lid']:
								checks += f"Тип: cban\nВыдал: {get_username(x['by'])[2]}\nВыдано: {date(x['date'])}\nПричина: {x['reason']}"
				if checks != '':
					return True, checks
				else:
					return False, None

	finally:
		connect.close()

def del_ban(type, info, peer_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `bans` WHERE user_id={info[1]} AND peer_id={peer_id} AND type=\'{type}\'')
			if res > 0:
				curl.execute(f'DELETE FROM `bans` WHERE user_id={info[1]} AND peer_id={peer_id} AND type=\'{type}\'')
				connect.commit()
				return f"{st.TAG} Пользователю {info[2]} была снята блокировка."
			else:
				return f"{st.TAG} У пользователя {info[2]} нету блокировки."
	finally:
		connect.close()

def binfo(peer_id, user_id):
	info_ban, bans = check_bans(user_id, peer_id)
	if info_ban:
		return f"{st.TAG} Блокировки пользователя {get_username(user_id)[2]}:\n\n{bans}"
	else:
		return f"{st.TAG} У пользователя {get_username(user_id)[2]} нет блокировок."

def get(peer_id, user_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f"SELECT * FROM `users` WHERE user_id={user_id} AND peer_id={peer_id}")
			row = curl.fetchone()
			check = checker(user_id, peer_id)
			chat = f"Беседа: \"{title(peer_id)}\" [ID: {peer_id-2000000000}]\n" if check[0] else "Беседа: \"-\" [ID: 0]\n"
			additionBD = f"Добавлен в БД: {date(row['first_date'])}\n" if res > 0 else ""
			last_msg = f"Последнее сообщение: {date(row['last_msg'])}\n" if res > 0 else ""
			date_reg = f"Дата регистрации: {datereg(user_id)}\n"
			additionCT = f"Добавлен в конференцию: {join_date(user_id, peer_id)}\n" if check[0] else ""
			domains = f"Список доменов: {row['nick'].replace('none', 'отсутствуют')}\n" if res > 0 else ""
			return f"{st.TAG} Информация о пользователе {get_username(user_id)[2]}\n\n{chat}{additionBD}{last_msg}{date_reg}{additionCT}{domains}"
	finally:
		connect.close()

def point(info, peer_id, count, reason):
	connect = conn()
	try:
		with connect.cursor() as curl:
			if count >= 0:
				curl.execute(f'SELECT * FROM `users` WHERE user_id={info[1]} AND peer_id={peer_id}')
				points = curl.fetchone()['point']+count
				curl.execute(f'UPDATE `users` SET point={points} WHERE user_id={info[1]} AND peer_id={peer_id}')
				return f"{st.TAG} Пользователь {info[2]} получил {count} баллов.\n\nВсего баллов: {points}\n{reason}"
			else:
				return f"{st.TAG} Кол-во баллов не должно быть меньше нуля."
	finally:
		connect.commit()
		connect.close()

def points(peer_id, page):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'SELECT * FROM `users` WHERE peer_id={peer_id} AND point>0')
			row = curl.fetchall()
			ni0,ni1,ni2 = page*st.RIC-st.RIC,page*st.RIC,round(len(row)/st.RIC,1)
			ni1 = len(row) if ni1 > len(row) else ni1
			ni2 = int(ni2)+1 if str(ni2)[-1] != '0' else int(ni2)
			if page <= ni2 and page > 0:
				message = '\n'.join(f"{x+1}. {get_username(row[x]['user_id'])[2]} - {row[x]['point']} баллов." for x in range(ni0,ni1))
				return f"{st.TAG} Список пользователей с баллами:\n<<Страница: {page}/{ni2}>>\n\n{message}"
			else:return f"{st.TAG} Такой страницы не существует."
	finally:connect.close()

def set_warn(type, info, peer_id, reason, count, by):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'SELECT * FROM `users` WHERE user_id={info[1]} AND peer_id={peer_id}')
			row = curl.fetchone()
			if type == 'warn':
				if row['warn']<6:
					warns = row['warn']+count; warns = 6 if warns>6 else warns
					rsn = '-' if len(reason) == 0 else reason
					curl.execute(f"INSERT INTO `warnings`(user_id, peer_id, warn, date, `by`, reason) VALUES({info[1]}, {peer_id}, '+{count}', {int(time.time())}, {by}, '{rsn}')")
					curl.execute(f"UPDATE `users` SET warn={warns} WHERE user_id={info[1]} AND peer_id={peer_id}")
					connect.commit()
					reason = f"Причина: {reason}" if len(reason) > 0 else ''
					if warns == 6:
						set_ban('ban', info, peer_id, '3/3', -st.GROUP_ID)
						return f"{st.TAG} Пользователь {info[2]} получил {count} предупреждений.\n{reason}\n\nКол-во предупреждений: {st.WARNS[warns]}\n\nПользователь был заблокирован в беседе.\nПричина: 3/3."
					else:
						return f"{st.TAG} Пользователь {info[2]} получил {count} предупреждений.\n{reason}\n\nКол-во предупреждений: {st.WARNS[warns]}"
				else:
					s_id = f"id{info[1]}" if info[1] > 0 else f"club{info[1]*-1}"
					return f"{st.TAG} У пользователя {info[2]} уже 6 предупреждений.\n\nЧтобы просмотреть предупреждения: /warnings vk.com/{s_id}"
			elif type == 'unwarn':
				if row['warn']>0:
					warns = row['warn']-count; warns = 0 if warns<0 else warns
					rsn = '-' if len(reason) == 0 else reason
					curl.execute(f"INSERT INTO `warnings`(user_id, peer_id, warn, date, `by`, reason) VALUES({info[1]}, {peer_id}, '-{count}', {int(time.time())}, {by}, '{rsn}')")
					curl.execute(f"UPDATE `users` SET warn={warns} WHERE user_id={info[1]} AND peer_id={peer_id}")
					connect.commit()
					reason = f"Причина: {reason}" if len(reason) > 0 else ''
					return f"{st.TAG} Пользователю {info[2]} снято {count} предупреждений.\n{reason}\n\nКол-во предупреждений: {st.WARNS[warns]}"
				else:
					s_id = f"id{info[1]}" if info[1] > 0 else f"club{info[1]*-1}"
					return f"{st.TAG} У пользователя {info[2]} уже 0 предупреждений.\n\nЧтобы просмотреть предупреждения: /warnings vk.com/{s_id}"
	finally:
		connect.close()

def warnlist(peer_id, page):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'SELECT * FROM `users` WHERE peer_id={peer_id} AND warn>0')
			row = curl.fetchall()
			ni0,ni1,ni2 = page*st.RIC-st.RIC,page*st.RIC,round(len(row)/st.RIC,1)
			ni1 = len(row) if ni1 > len(row) else ni1
			ni2 = int(ni2)+1 if str(ni2)[-1] != '0' else int(ni2)
			if page <= ni2 and page > 0:
				message = '\n'.join(f"{x+1}. {get_username(row[x]['user_id'])[2]} - ({st.WARNS[row[x]['warn']]}) пред." for x in range(ni0,ni1))
				return f"{st.TAG} Список пользователей с предупреждениями:\n<<Страница: {page}/{ni2}>>\n\n{message}"
			else:return f"{st.TAG} Такой страницы не существует."
	finally:connect.close()

def warnings(peer_id,user_id,page):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f'SELECT * FROM `warnings` WHERE user_id={user_id} AND peer_id={peer_id}')
			row = curl.fetchall()
			if res > 0:
				ni0,ni1,ni2 = page*st.RIC-st.RIC,page*st.RIC,round(len(row)/st.RIC,1)
				ni1 = len(row) if ni1 > len(row) else ni1
				ni2 = int(ni2)+1 if str(ni2)[-1] != '0' else int(ni2)
				if page <= ni2 and page > 0:
					message = '\n'.join(f"{x+1}. выдал: {get_username(row[x]['by'])[2]}, кол-во пред: {row[x]['warn']}, дата: {date(row[x]['date'])}, причина: {row[x]['reason']}" for x in range(ni0,ni1))
					return f'{st.TAG} Список предупреждений пользователя:\n<<Страница: {page}/{ni2}>>\n\n{message}'
				else:return f"{st.TAG} Такой страницы не существует."
			else:return f"{st.TAG} Список пуст."
	finally:connect.close()

def get_filter(peer_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			curl.execute(f'SELECT * FROM `chats` WHERE peer_id={peer_id}')
			t = curl.fetchone()['filter'].split(','); t.remove('')
			return t
	finally:
		connect.close()

def filter(peer_id, type, words=[]):
	connect = conn()
	filt = get_filter(peer_id)
	try:
		with connect.cursor() as curl:
			curl.execute(f'SELECT * FROM `chats` WHERE peer_id={peer_id}')
			row = curl.fetchone()
			if type.lower() == 'list':
				if len(filt)>0: return f'{st.TAG} Список слов в фильтре:\n\n{", ".join(filt)}.'
				else: return f'{st.TAG} Список слов в фильтре пуст.'
			elif type.lower() == 'add':
				new_filter = row['filter'] + f'{",".join(words).lower()},'
				curl.execute(f'UPDATE `chats` SET filter=\'{new_filter}\' WHERE peer_id={peer_id}')
				connect.commit()
				return f"{st.TAG} Фильтр успешно обновлён."
			elif type.lower() == 'del':
				new_filter = row['filter']
				if len(words) == 1:
					new_filter = new_filter.replace(f"{words[0]},", '')
				else:
					for x in words:
						new_filter = new_filter.replace(f"{x},", '')
				curl.execute(f'UPDATE `chats` SET filter=\'{new_filter}\' WHERE peer_id={peer_id}')
				connect.commit()
				return f"{st.TAG} Фильтр успешно обновлён."
	finally:connect.close()

def domain(peer_id, type, info=[], nick='none', page=0):
	connect = conn()
	try:
		with connect.cursor() as curl:
			if type.lower() == 'list':
				curl.execute(f'SELECT * FROM `users` WHERE peer_id={peer_id} AND nick!=\'none\'')
				row = curl.fetchall()
				ni0,ni1,ni2 = page*st.RIC-st.RIC,page*st.RIC,round(len(row)/st.RIC,1)
				ni1 = len(row) if ni1 > len(row) else ni1
				ni2 = int(ni2)+1 if str(ni2)[-1] != '0' else int(ni2)
				if page <= ni2 and page > 0:
					message = '\n'.join(f"{x+1}. {get_username(row[x]['user_id'])[2]} - {row[x]['nick']}." for x in range(ni0,ni1))
					return f"{st.TAG} Список пользователей с никами:\n<<Страница: {page}/{ni2}>>\n\n{message}"
				else:return f"{st.TAG} Такой страницы не существует."
				
			elif type.lower() == 'set':
				curl.execute(f'UPDATE `users` SET nick="{nick}" WHERE peer_id={peer_id} AND user_id={info[1]}')
				connect.commit()
				return f"{st.TAG} Пользователю {info[2]} установлен никнейм <<{nick}>>."

			elif type.lower() == 'del':
				res = curl.execute(f'SELECT * FROM `users` WHERE peer_id={peer_id} AND user_id={info[1]}')
				if res > 0:
					if curl.fetchone()['nick'] != nick:
						curl.execute(f'UPDATE `users` SET nick="{nick}" WHERE peer_id={peer_id} AND user_id={info[1]}')
						connect.commit()
						return f"{st.TAG} Пользователю {info[2]} удалён никнейм."
					else:return f"{st.TAG} У пользователя не установлен никнейм."
				else:return f"{st.TAG} У пользователя не установлен никнейм."
	finally:connect.close()

def a_invite(info, peer_id, by, ID):
	connect = conn()
	try:
		with connect.cursor() as curl:
			if ID == 1:i_history_append(by,peer_id,'invite',info[1])
			curl.execute(f"UPDATE `invites` SET a_invite={ID} WHERE peer_id={peer_id} AND uid={info[1]}")
			if ID == 1:return f"{st.TAG} Пользователь {info[2]} помечен как приглашённый.\nТеперь пользователя может пригласить кто-угодно."
			else:return f"{st.TAG} Пользователю {info[2]} отклонено разрешение на приглашение."
	finally:
		connect.commit()
		connect.close()

def a_invite_ID(info, peer_id):
	connect = conn()
	try:
		with connect.cursor() as curl:
			res = curl.execute(f"SELECT * FROM `invites` WHERE peer_id={peer_id} AND uid={info[1]}")
			if res > 0:
				return curl.fetchone()['a_invite']
			else:
				return 0
	finally:connect.close()