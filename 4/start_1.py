import discord, re
from time import *
from function import *
import datetime
from discord.ext import commands

token, bot, p, tag = session()

@bot.event
async def on_ready():
	print('ta')

@bot.event
async def on_voice_state_update(member, before, after):
	try:
		if before.channel == None and after.channel != None:
			start_time = time()
			count(member.id, start_time)
			print(f'Пользователь «{member.nick}» зашёл в канал: {after.channel}')
		elif before.channel != None and after.channel == None:
			result(member.id)
			print(f'Пользователь «{member.nick}» вышел из канала: {before.channel}')

	except:
		pass

@bot.event
async def on_message(message):
	await bot.process_commands(message)
	msg = message.content.split(' ')
	if msg[0] == f'{p}top':
		lvl = check_lvl(message.author.id)
		if lvl >= 1:
			await message.channel.send(top())

	if msg[0] == f"{p}admins":
		lvl = check_lvl(message.author.id)
		if lvl >= 1:
			await message.channel.send(admins())

	if msg[0] == f"{p}warns":
		lvl = check_lvl(message.author.id)
		if lvl >= 2:
			await message.channel.send(warns())

	if msg[0] == f"{p}ahelp":
		lvl = check_lvl(message.author.id)
		if lvl >= 1:
			await message.channel.send(
'''
**1/2 уровень админ прав:**
```.ahelp - помощь в администрирование.
.top - топ пользователей по онлайну
.admins - список администраторов```
**Rexana Bot
Модератор Discord**
```/tempmute
/unmute```


**3 уровень админ прав:**
```.clear - очистка чата.
.kick - кик пользователя с сервера.
.warn - выдать предупреждение.
.warns - список пользователей с варнами.
```

**4 уровень админ прав:**
```.fmess - отправить сообщение от имени бота.
.unwarn - снять предупреждение.
```

**5 уровень админ прав:**
```.givebotadm - выдать админ права.
```

**6 уровень админ прав:**
```.topallclear - очистка голосово онлайна.
```''')

@bot.command(pass_context=True)
async def givebotadm(ctx, member: discord.Member, reason=None):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 5:
		check = get_admin(lvl, check_lvl(member.id))
		if check == 0:
			if int(reason) < 5:
				text = add_admin(member.id, reason)
				await ctx.send(text)
				await member.send(f'```py\nВам были выданы права администратора {reason} уровня\nОт пользователя: {ctx.message.author.name}\nВаш ID: {member.id}\n```')
			else:
				await ctx.send('```py\nНельзя выдать уровень более чем 4 lvl.\n```')
		else:
			await ctx.send(f'```py\nВаш уровень меньше или совпадает с уровнем пользователя.\n```') 

@bot.command(pass_context=True)
async def topallclear(ctx):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 6:
		text = topclear()
		await ctx.send(text)

@bot.command(pass_context=True)
async def clearuser(ctx, member: discord.Member):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 6:
		text = clearuser(member.id, member.nick)
		await ctx.send(text)

@bot.command(pass_context=True)
async def fmess(ctx, *, arg):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 4:
		await ctx.channel.purge(limit=1)
		await ctx.send(arg)

@bot.command(pass_context=True)
async def clear(ctx, arg):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 3:
		await ctx.channel.purge(limit=1)
		await ctx.channel.purge(limit=int(arg))
		await ctx.send(f'```py\n✅ - Было удалено {arg} сообщений\n```')
		sleep(1.5)
		await ctx.channel.purge(limit=1)

@bot.command(pass_context=True)
async def kick(ctx, member: discord.Member, *, reason=None):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 3:
		check = get_admin(lvl, check_lvl(member.id))
		if check == 0:
			await member.send(f"```py\nВы были кикнуты с сервера\nАдминистратор: {ctx.message.author.nick}\nПричина: {reason}\n```")
			await member.kick(reason=reason)
			await ctx.send(f'```py\nПользователь «{member.nick}» (ID: {member.id}) был кикнут с сервера.\nПричина: {reason}\n```')
		else:
			await ctx.send('```py\nВаш уровень меньше или совпадает с уровнем пользователя.\n```')

@bot.command(pass_context=True)
async def warn(ctx, member: discord.Member, arg, *, reason=None):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 3:
		check = get_admin(lvl, check_lvl(member.id))
		if check == 0:
			i, text = add_warn(member.id, arg, reason, member.nick)
			await ctx.send(text)
			if int(arg) < 0 or int(arg) > 3:
				pass
			else:
				await member.send(f"```py\nВам было выдано {arg} предупреждения\nАдминистратор: {ctx.message.author.nick}\nКоличество: {i}/3\n\nПричина: {reason}\n```")
				if int(i) >= 3:
					await member.kick(reason=reason)
		else:
			await ctx.send('```py\nВаш уровень меньше или совпадает с уровнем пользователя.\n```')

@bot.command(pass_context=True)
async def unwarn(ctx, member: discord.Member, arg):
	lvl = check_lvl(ctx.message.author.id)
	if lvl >= 4:
		i, text = un_warn(member.id, arg, member.nick)
		await ctx.send(text)
		if int(arg) <= 0 or int(arg) > 3:
			pass
		else:
			await member.send(f"```py\nВам было снято {arg} предупреждения\nАдминистратор: {ctx.message.author.nick}\nКоличество: {i}/3\n\nПричина: {reason}\n```")

bot.run(token)