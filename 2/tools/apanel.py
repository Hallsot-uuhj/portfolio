from datetime import datetime
from tools.main import *
import requests
import psutil
import time
import re

vk,lp = sys()

def getUserID(uid):
	if isinstance(uid,int):
		return uid
	if 'https' in uid:
		check = uid.replace('https://vk.com/','')
		if 'id' in check:
			return int(check.replace('id', ''))
		elif 'club' in check:
			return int(check.replace('club', '-'))
		else:
			return int(vk.utils.resolveScreenName(screen_name=check)['object_id'])
	elif 'id' in uid:
		return int(re.findall(r'id\d+', str(uid))[0].replace('id',''))
	elif 'club' in uid:
		return int(re.findall(r'club\d+', str(uid))[0].replace('club','-'))

def getUserName(uid):
	id = getUserID(uid)
	if id < 0:
		inf = vk.groups.getById(group_id=str(id).split('-')[1])[0]
		return f"{inf['name']}", id
	elif id > 0:
		inf = vk.users.get(user_ids=id)[0]
		return f"{inf['first_name'][0]}. {inf['last_name']}", id

def checkCf(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f'SELECT * FROM chats WHERE cid={chat_id}')
			return True if result == 1 else False
	finally:
		connect.close()

def checkAudio(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM chats WHERE cid={chat_id}')
			return cursor.fetchone()['punishment']
	finally:
		connect.close()

def getGreetAudio(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM chats WHERE cid={chat_id}')
			return cursor.fetchone()['greeting_audio']
	finally:
		connect.close()

def regCf(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f'SELECT * FROM chats WHERE cid={chat_id}')
			if result == 1:
				return 'Ну здравствуйте ещё раз.'
			else:
				cursor.execute(f"INSERT INTO `chats`(cid,greeting) VALUES({chat_id},' ')")
				cursor.execute(f'''
CREATE TABLE `{chat_id}`(
`id` INT NOT NULL AUTO_INCREMENT,
`uid` INT NOT NULL,
`admin` INT NOT NULL DEFAULT '0',
`nick` varchar(100) NOT NULL DEFAULT 'null',
`warns` INT NOT NULL DEFAULT '0',
`messages` INT NOT NULL DEFAULT '0',
`ban` INT NOT NULL DEFAULT '0',
`dateban` INT NOT NULL DEFAULT '0',
`ban_reason` varchar(255) NOT NULL DEFAULT 'null',
`ban_by` varchar(255) NOT NULL DEFAULT 'null',
`mute` INT NOT NULL DEFAULT '0',
PRIMARY KEY (`id`)) ENGINE=InnoDB''')
				return 'Беседа зарегистрирована, приятного пользования.\nПеред использованием не забудьте выдать мне права администратора!'

	finally:
		connect.commit()
		connect.close()

def checkUser(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f'SELECT * FROM `{chat_id}` WHERE uid={uid}')
			row = cursor.fetchone()
			if uid > 0:
				if result == 0:
					if uid == 479938230:
						cursor.execute(f"INSERT INTO `{chat_id}`(uid,admin,messages) VALUES({uid},4,1)")

					elif uid == getOwnerId(chat_id+2000000000):
						cfName = vk.messages.getConversationsById(peer_ids=chat_id+2000000000,group_id=199992660)['items'][0]['chat_settings']['title']
						cursor.execute(f'UPDATE `chats` SET title="{cfName}" WHERE cid={chat_id}')
						cursor.execute(f"INSERT INTO `{chat_id}`(uid,admin,messages) VALUES({uid},4,1)")
						
					else:
						cursor.execute(f"INSERT INTO `{chat_id}`(uid,messages) VALUES({uid},1)")
				else:
					if row['mute'] > int(time.time()):
						vk.messages.removeChatUser(chat_id=chat_id,member_id=uid)
					row['messages'] += 1
					cursor.execute(f"UPDATE `{chat_id}` SET messages={row['messages']} WHERE uid={uid}")

	finally:
		connect.commit()
		connect.close()

def getOwnerId(peer_id):
	return vk.messages.getConversationsById(
		peer_ids=peer_id, 
		group_id=199992660)['items'][0]['chat_settings']['owner_id']

def getGreeting(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			r = cursor.execute(f'SELECT * FROM chats WHERE cid={chat_id}')
			row = cursor.fetchone()
			gr = row['greeting']
			return gr if gr == ' ' else '%s\n\n' % gr
	finally:
		connect.close()

def admLvl(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			r = cursor.execute(f'SELECT * FROM `{chat_id}` WHERE uid={uid}')
			return cursor.fetchone()['admin'] if r != 0 else r
	finally:
		connect.close()

def admins(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM `{chat_id}`')
			adms = '\n'.join(
f"[id{getUserName(u['uid'])[1]}|{getUserName(u['uid'])[0]}] | {u['admin']} уровень."
for u in cursor.fetchall()
if u['admin'] != 0
)
			return adms
	finally:
		connect.close()

def setAudio(chat_id,type,aud):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			aud = f"audio{aud['owner_id']}_{aud['id']}"
			if type == 'punishment':
				cursor.execute(f"UPDATE `chats` SET {type}='{aud}' WHERE cid={chat_id}")
			elif type == 'greeting':
				cursor.execute(f"UPDATE `chats` SET {type}_audio='{aud}' WHERE cid={chat_id}")

	finally:
		connect.commit()
		connect.close()

def Greet(chat_id,type,text):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			if type == 'set':
				cursor.execute(f"UPDATE `chats` SET greeting='{text}' WHERE cid={chat_id}")
			elif type == 'del':
				cursor.execute(f"UPDATE `chats` SET greeting=' ' WHERE cid={chat_id}")

	finally:
		connect.commit()
		connect.close()

def generateMt(chat_id,type):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			users = vk.messages.getConversationMembers(peer_id=chat_id+2000000000, group_id=199992660)['profiles']
			if type == '=0':
				return ', '.join(
f"[id{usr['id']}|{usr['first_name'][0]}. {usr['last_name']}]" 
for usr in users if admLvl(chat_id,usr['id']) <= 0
)
			elif type in ['=a','=а']:
				return ', '.join(
f"[id{usr['id']}|{usr['first_name'][0]}. {usr['last_name']}]" 
for usr in users if admLvl(chat_id,usr['id']) > 0
)	

	finally:
		connect.close()

def top(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:     
			result = cursor.execute(f'SELECT * FROM `{chat_id}`')
			row = cursor.fetchall()
			msgs = [i['messages'] for i in row]
			users = [i['uid'] for i in row]
			sortedData = sorted(zip(msgs, users), key=lambda n: int(n[0]), reverse=True)
			top = '\n'.join(
f'{i}. [id{n[1]}|{getUserName(n[1])[0]}] - {n[0]} сообщений.' 
for i, n in enumerate(sortedData, 1) if int(n[0]) >= 10
)
			messages = 0
			for msg in msgs:
				messages += msg
			return top, messages

	finally:
		connect.close()

def getUserDateReg(uid):
	s = requests.Session()
	r = s.post(f"https://vk.com/foaf.php?id={uid}")
	t = re.findall(r"<ya:created dc:date=\".+\"/>", r.text)[0]
	t = re.findall(r"\d+-\d+-\d+T\d+:\d+:\d+", t)[0].replace('-','.')
	t = t.split('T')
	d = t[0].split('.')
	return f"{d[2]}.{d[1]}.{d[0].replace('20','')} {t[1]}"

def procctime(seconds):
	m,s = divmod(seconds, 60)
	h,m = divmod(m, 60)
	d,h = divmod(h, 24)
	d,h,m,s = str(int(d)),str(int(h)),str(int(m)),str(int(s))
	days = f'{d} дня'
	hours = f'{h} часа'
	minuts = f'{m} минут'
	seconds = f'{s} секунд'

	if '1' in d[-1]: days = f'{d} день'
	elif '2' in d[-1] or '3' in d[-1] or '4' in d[-1]: days = f'{d} дня'
	else: days = f'{d} дней'

	if '1' in h[-1]: hours = f'{h} час'
	elif '2' in h[-1] or '3' in h[-1] or '4' in h[-1]: hours = f'{h} часа'
	else: hours = f'{h} часов'

	if '1' in m[-1]: minuts = f'{m} минута'
	elif '2' in m[-1] or '3' in m[-1] or '4' in m[-1]: minuts = f'{m} минуты'
	else: minuts = f'{m} минут'

	if '1' in s[-1]: seconds = f'{s} секунда'
	elif '2' in s[-1] or '3' in s[-1] or '4' in s[-1]: seconds = f'{s} секунды'
	else: seconds = f'{s} секунд'
	return f'{days} {hours} {minuts} {seconds}'

def getUpTime():
	Unix = lambda start=psutil.boot_time(): time.time() - start
	return procctime(Unix())

def getUserInfo(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			name,uid = getUserName(uid)    
			result = cursor.execute(f'SELECT * FROM `{chat_id}` WHERE uid={uid}')
			if result == 1:
				row = cursor.fetchone()
				join_date = [kk['join_date']
	for kk in vk.messages.getConversationMembers(peer_id=chat_id+2000000000,group_id=199992660)['items']
	if kk['member_id'] == uid]
				cfName = vk.messages.getConversationsById(peer_ids=chat_id+2000000000,
					group_id=199992660)['items'][0]['chat_settings']['title']
				Unix = lambda start=join_date[0]: int(time.time()) - start
				join_date = datetime.fromtimestamp(join_date[0])
				admin_lvl = f'\nАдмин уровень: {row["admin"]}' if row['admin'] != 0 else ''
				text = f'''
	Информация о пользователе "[id{uid}|{name}]"\n
	Беседа: "{cfName}" [ID: {chat_id}]{admin_lvl}
	Количество сообщений: {row["messages"]}
	Дата регистрации: {getUserDateReg(uid)}
	Добавлен в конференцию: {join_date.strftime("%d.%m.%y %H:%M:%S")}
	Никнейм пользователя: {row["nick"] if row["nick"] != "null" else "-"}
	Время нахождения: {procctime(Unix())}
	'''
				return text
			else:
				text = f'''
	Информация о пользователе "[id{uid}|{name}]"\n
	Беседа: "-" [ID: {chat_id}]
	Количество сообщений: -
	Дата регистрации: {getUserDateReg(uid)}
	Добавлен в конференцию: -
	Никнейм пользователя: -
	Время нахождения: -
	'''
				return text

	finally:
		connect.close()

def setAdmLvl(chat_id,uid,lvl):
	connect = connection()
	try:
		cursor = connect.cursor()
		result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={uid}")
		if result == 1:
			cursor.execute(f"UPDATE `{chat_id}` SET admin={lvl} WHERE uid={uid}")
		else:
			cursor.execute(f"INSERT INTO `{chat_id}`(uid,admin) VALUES({uid},{lvl})")

	finally:
		connect.commit()
		connect.close()

def count_warns(count):
	if count == 0: return '0/3 0/2'
	elif count == 1: return '0/3 1/2'
	elif count == 2: return '1/3 0/2'
	elif count == 3: return '1/3 1/2'
	elif count == 4: return '2/3 0/2'
	elif count == 5: return '2/3 1/2'
	elif count == 6: return '3/3 0/2'

def setWarns(chat_id,inf,count,reason):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={inf[1]}")
			row = cursor.fetchone()
			alls = None
			if result == 1:
				alls = row['warns'] + count
				if alls >= 6: alls = 6
				cursor.execute(f"UPDATE `{chat_id}` SET warns={alls} WHERE uid={inf[1]}")

			else:
				alls = count
				cursor.execute(f"INSERT INTO `{chat_id}`(uid,warns) VALUES({inf[1]},{count})")

			cause = f'Причина: {reason}' if len(list(reason)) != 0 else ''
			return f"Пользователю [id{inf[1]}|{inf[0]}] выдано {count} предупреждений\n\nКоличество: {count_warns(alls)}\n{cause}", alls

	finally:
		connect.commit()
		connect.close()

def endWarns(chat_id,inf,count,reason):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={inf[1]}")
			row = cursor.fetchone()
			alls = None
			if result == 1:
				alls = row['warns'] - count
				if alls <= 0: alls = 0
				cursor.execute(f"UPDATE `{chat_id}` SET warns={alls} WHERE uid={inf[1]}")

			else:
				alls = count
				cursor.execute(f"INSERT INTO `{chat_id}`(uid,warns) VALUES({inf[1]},{count})")

			cause = f'Причина:{reason}' if len(list(reason)) != 0 else ''
			return f"Пользователю [id{inf[1]}|{inf[0]}] снято {count} предупреждений\n\nКоличество: {count_warns(alls)}\n{cause}"

	finally:
		connect.commit()
		connect.close()

def warns(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM `{chat_id}`')
			warns = '\n'.join(
f"[id{getUserName(u['uid'])[1]}|{getUserName(u['uid'])[0]}] - {count_warns(u['warns'])}"
for u in cursor.fetchall()
if u['warns'] != 0
)
			return warns,0 if warns == '' else 1
	finally:
		connect.close()

def mywarns(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM `{chat_id}` WHERE uid={uid}')
			row = cursor.fetchone()
			return count_warns(row['warns'])
	finally:
		connect.close()

def ban(chat_id,uid,reason,from_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={uid}")
			row = cursor.fetchone()
			cause = reason if len(list(reason)) != 0 else '-'
			if result == 1:
				if row['ban'] == 1: return '',0
				else:
					cursor.execute(f"UPDATE `{chat_id}` SET ban=1 WHERE uid={uid}")
					cursor.execute(f"UPDATE `{chat_id}` SET ban_reason='{cause}' WHERE uid={uid}")
					cursor.execute(f"UPDATE `{chat_id}` SET dateban='{int(time.time())}' WHERE uid={uid}")
					cursor.execute(f"UPDATE `{chat_id}` SET ban_by='{from_id}' WHERE uid={uid}")

			else:
				cursor.execute(f"INSERT INTO `{chat_id}`(uid,ban,ban_reason,dateban,ban_by) VALUES({uid},1,'{cause}','{int(time.time())}','{getUserName(from_id)[0]}')")

			return f'Причина:{reason}' if len(list(reason)) != 0 else '',1

	finally:
		connect.commit()
		connect.close()

def checkban(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `blist` WHERE uid={uid}")
			if result == 1: return True
			else:
				result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={uid}")
				row = cursor.fetchone()
				if result == 1:
					if row['ban'] == 1: return True
					else: return False
				else:
					return False

	finally:
		connect.close()

def unban(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={uid}")
			row = cursor.fetchone()
			if result == 1:
				if row['ban'] == 0: return 0
				else:
					cursor.execute(f"UPDATE `{chat_id}` SET ban=0 WHERE uid={uid}")
					cursor.execute(f"UPDATE `{chat_id}` SET ban_reason='null' WHERE uid={uid}")
					cursor.execute(f"UPDATE `{chat_id}` SET dateban='0' WHERE uid={uid}")
					cursor.execute(f"UPDATE `{chat_id}` SET ban_by='null' WHERE uid={uid}")

			else:
				return 0

			return 1

	finally:
		connect.commit()
		connect.close()

def binfo(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			r = cursor.execute(f'SELECT * FROM `{chat_id}` WHERE uid={uid}')
			row = cursor.fetchone()
			if not checkban(chat_id,uid): return '',0
			else:
				text = ''
				if r == 1 and row['ban'] == 1:
					cfName = vk.messages.getConversationsById(peer_ids=chat_id+2000000000,
					group_id=199992660)['items'][0]['chat_settings']['title']
					date = datetime.fromtimestamp(row['dateban'])
					ban_by = getUserName(int(row["ban_by"]))
					text += f'1. Беседа: "{cfName}" [{chat_id}], выдал: [id{ban_by[1]}|{ban_by[0]}], дата: {date.strftime("%d.%m.%y %H:%M")}, причина: {row["ban_reason"]}\n\n'
				r = cursor.execute(f"SELECT * FROM `blist` WHERE uid={uid}")
				if r == 1:
					row = cursor.fetchone()
					date = datetime.fromtimestamp(row['dateban'])
					ban_by = getUserName(int(row["by"]))
					cid = row['cid']
					cfName = vk.messages.getConversationsById(peer_ids=cid+2000000000,
					group_id=199992660)['items'][0]['chat_settings']['title']
					text += f'2. Беседа: "{cfName}" [{cid}], выдал: [id{ban_by[1]}|{ban_by[0]}], дата: {date.strftime("%d.%m.%y %H:%M")}, причина: {row["reason"]}'

				return text,1

	finally:
		connect.close()

def setNick(chat_id,uid,nick):
	connect = connection()
	try:
		cursor = connect.cursor()
		result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={uid}")
		if result == 1:
			cursor.execute(f"UPDATE `{chat_id}` SET nick='{nick}' WHERE uid={uid}")
		else:
			cursor.execute(f"INSERT INTO `{chat_id}`(uid,nick) VALUES({uid},'{nick}')")

	finally:
		connect.commit()
		connect.close()

def delNick(chat_id,uid):
	connect = connection()
	try:
		cursor = connect.cursor()
		result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={uid}")
		row = cursor.fetchone()
		if result == 1:
			if row['nick'] == 'null': return 0
			else:
				cursor.execute(f"UPDATE `{chat_id}` SET nick='null' WHERE uid={uid}")
				return 1
		else:
			return 0

	finally:
		connect.commit()
		connect.close()

def nicks(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM `{chat_id}`')
			nicks = '\n'.join(
f"[id{getUserName(u['uid'])[1]}|{getUserName(u['uid'])[0]}] - {u['nick']}"
for u in cursor.fetchall()
if u['nick'] != 'null'
)
			return nicks,0 if nicks == '' else 1
	finally:
		connect.close()

def mute(chat_id,inf,tim,reason):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={inf[1]}")
			row = cursor.fetchone()
			if tim > 20160:
				return 'Время мута не должно быть больше 14 дней (20160 м).'
			elif tim <= 0:
				return 'Время мута не должно быть меньше 0.'
			else:
				if result == 1:
					if row['mute'] > int(time.time()): return 'У пользователя уже есть блокировка чата.'
					else: cursor.execute(f"UPDATE `{chat_id}` SET mute={int(time.time())+tim*60} WHERE uid={inf[1]}")

				else:
					cursor.execute(f"INSERT INTO `{chat_id}`(uid,mute) VALUES({inf[1]},{int(time.time())+tim/60})")
			mute_time = datetime.fromtimestamp(int(time.time())+tim*60)
			return f'Пользователь [id{inf[1]}|{inf[0]}] был заглушён администратором на {tim} мин.\n\nВремя окончания мута: {mute_time.strftime("%d.%m.%y %H:%M:%S")}\n{reason}'

	finally:
		connect.commit()
		connect.close()

def unmute(chat_id,inf,reason):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `{chat_id}` WHERE uid={inf[1]}")
			row = cursor.fetchone()
			if result == 1:
				if row['mute'] < int(time.time()): return 'У пользователя нету блокировки чата.'
				else: cursor.execute(f"UPDATE `{chat_id}` SET mute=0 WHERE uid={inf[1]}")

			else: return 'У пользователя нету блокировки чата.'
			return f'Пользователь [id{inf[1]}|{inf[0]}] был разглушен администратором.{reason}'

	finally:
		connect.commit()
		connect.close()

def titleUpdate(chat_id,cfName):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'UPDATE `chats` SET title="{cfName}" WHERE cid={chat_id}')
	finally:
		connect.commit()
		connect.close()

def getTitle(chat_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM `chats` WHERE cid={chat_id}')
			return cursor.fetchone()['title']
	finally:
		connect.close()

def getChats():
	connect = connection()
	try:
		with connect.cursor() as cursor:
			cursor.execute(f'SELECT * FROM `chats`')
			return [row['cid'] for row in cursor.fetchall()]
	finally:
		connect.close()

def gban(chat_id,uid,reason,from_id):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `blist` WHERE uid={uid}")
			cause = reason if len(list(reason)) != 0 else '-'
			if result == 0:
				cursor.execute(f"INSERT INTO `blist`(cid,uid,reason,dateban,`by`) VALUES({chat_id},{uid},'{cause}','{int(time.time())}','{getUserName(from_id)[1]}')")

			else:
				return '',0

			return f'Причина:{reason}' if len(list(reason)) != 0 else '',1

	finally:
		connect.commit()
		connect.close()

def ungban(chat_id,uid):
	connect = connection()
	try:
		with connect.cursor() as cursor:
			result = cursor.execute(f"SELECT * FROM `blist` WHERE uid={uid}")
			if result == 1:
				cursor.execute(f"DELETE FROM `blist` WHERE uid={uid}")

			else:
				return 0

			return 1

	finally:
		connect.commit()
		connect.close()