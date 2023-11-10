from modules.system import *

token, bot, p = session()
bot.remove_command("help")

@bot.event
async def on_ready():
	DiscordComponents(bot)
	#: Update channel <Registration>;
	channel = await bot.fetch_channel(channels["Регистрация"])
	await channel.purge(limit=1)
	emb = discord.Embed(colour=COLOR_EMBEDS['neutral'])
	emb.set_image(url="https://psv4.userapi.com/c237231/u310796427/docs/d38/6211ebb440c9/registratsia.png?extra=mjyf8Lebvn0OjtnH-j1bdE17ZSJz4laDBkteP-q6-JUzgJWTCcq2SGohuVa9afi4jkj2iVTPelUjqxTW9qhiW65XwVnMOgwXtvpSwSXEkYUiM1j0GZvvt7BnMqm3i7P2NH2yACVzq7OuzYWxVLbie2q8")
	row = ActionRow(Button(style=ButtonStyle.blue, label='Зарегистрироваться', custom_id='reg'))
	await channel.send(embed=emb, components=[row])
	#: Update channel <profile roles>;
	channel = await bot.fetch_channel(channels["Игровые роли"])
	await channel.purge(limit=4)
		#: Genders;
	emb = discord.Embed(colour=COLOR_EMBEDS['neutral'])
	emb.set_image(url="https://psv4.userapi.com/c237031/u310796427/docs/d37/dd27c11e120c/gendernye.png?extra=ZNfjRuHGKDzotkZE0I77CBJQOvm9pw9hbIfyKwxA2ZPixbxqRkXXWVSIVyqPURGUIiCH8PpiwSW9ZZ2oBy1zH6KQcf7TwsZZcjJdE2I2PZnbCPAhwRG0JZR4GmBcwzsMYZyGc6hq6cXfpa6xE6SR4j0h")
	row = ActionRow(Button(label='Мужчина', custom_id='male'), Button(label='Девушка', custom_id='female'))
	await channel.send(embed=emb, components=[row])
		#: Notifications;
	emb = discord.Embed(colour=COLOR_EMBEDS['neutral'])
	emb.set_image(url="https://psv4.userapi.com/c237031/u310796427/docs/d3/70f8e444df34/uvedomlenia.png?extra=cv5whuKay_FvWs9ZGMUTprjw7K9BlL4y5gD5lwcwiUAXUY2a3Fpr5eFeJVBGmK0GcsmzYz6JHSqYe0ujCicnG9VYBt5ZmKXydFZP3FqUOBZsSfa66zJHo4m11QBq1TLPa_bjXVwtvFq_eCUWGeySXYAt")
	row = ActionRow(Button(label='Новости', custom_id='news'), Button(label='Розыгрыши', custom_id='raffles'), Button(label='Стримы', custom_id='streams'), Button(label='Турниры', custom_id='tournaments'))
	await channel.send(embed=emb, components=[row])
		#: Mein legends;
	emb = discord.Embed(colour=COLOR_EMBEDS['neutral'])
	emb.set_image(url="https://psv4.vkuseraudio.net/s/v1/d/6qVYquG9yskTUFVIwkQ7IJallMtzODJw2UrzNoTjkgtRE-pYNMbsCOP5i0fdJlzUDKLv1g5rjG7Esw4xwx-BKP7wmbpetLx0KhSHHI9k6-4ER6Tw3qcbeA/meyn_legendy.png")
	row = ActionRow(Select(placeholder="Мейн-легенды", options = [SelectOption(label = "Бладхаунд", value = "legends_Бладхаунд"),SelectOption(label = "Габралтор", value = "legends_Габралтор"),SelectOption(label = "Лайфлайн", value = "legends_Лайфлайн"),SelectOption(label = "Патфайндер", value = "legends_Патфайндер"),SelectOption(label = "Рэйф", value = "legends_Рэйф"),SelectOption(label = "Бангалор", value = "legends_Бангалор"),SelectOption(label = "Каустик", value = "legends_Каустик"),SelectOption(label = "Мираж", value = "legends_Мираж"),SelectOption(label = "Октейн", value = "legends_Октейн"),SelectOption(label = "Ватсон", value = "legends_Ватсон"),SelectOption(label = "Крипто", value = "legends_Крипто"),SelectOption(label = "Ревенант", value = "legends_Ревенант"),SelectOption(label = "Лоба", value = "legends_Лоба"),SelectOption(label = "Рампарт", value = "legends_Рампарт"),SelectOption(label = "Хорайзон", value = "legends_Хорайзон"),SelectOption(label = "Фьюз", value = "legends_Фьюз"),SelectOption(label = "Валькирия", value = "legends_Валькирия"),SelectOption(label = "Сиар", value = "legends_Сиар"),SelectOption(label = "Эш", value = "legends_Эш"),SelectOption(label = "Мэгги", value = "legends_Мэгги"),SelectOption(label = "Ньюкасл", value = "legends_Ньюкасл")]))
	await channel.send(embed=emb, components=[row])
		#: Game roles;
	emb = discord.Embed(colour=COLOR_EMBEDS['neutral'])
	emb.set_image(url="https://psv4.userapi.com/c237031/u310796427/docs/d8/acd3146dad25/rangi.png?extra=Xi9WtayaryrDO7N09H5zQL7JPTa6Lw38Zq6g0VeNVeWuzjDiNIagvQXd_hpwW00o4JDCvplm4G-8MVhMnMROLxac2UZYQjsVv_zlBsmSRRyYTeI7_N35VlGU2uU37t3yrkvI4MV6s4PY21ukCBKSNPBQ")
	emb.set_footer(text="Кнопка \"Обновить\" недоступна для Steam игроков.")
	row = ActionRow(Button(label='Рейтинг КБ', custom_id='KBrank'), Button(label='Рейтинг Арены', custom_id='Arank'), Button(style=ButtonStyle.blue, label='Обновить', custom_id='update'))
	await channel.send(embed=emb, components=[row])
	#: Print mention;
	print('<{0.user}> is running | v1.2\n'.format(bot))

@bot.event
async def on_message(message):
	if message.author.discriminator not in ['0337','0000']:
		print("[Log]<{0.channel.name}> - {0.author}: {0.content}".format(message))

	await bot.process_commands(message)

@bot.event
async def on_member_join(member):
	cid = f'hi_button_{member}'
	emb = discord.Embed(description = f'*Здравствуй,* **{member.mention}**!{emojies[":jumpi:"]}\n*Ты на сервере* ***[‧₊Holy Apex Legends˚₊](https://discord.gg/Yy6fyef6BY)***\n\n╭︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿ꔫ\n(ᅠˎᅠᅠᅠˊᅠᅠᅠˎᅠᅠᅠˊᅠᅠᅠˎ\n) {emojies[":1_:"]}**`Число участников сервера:`** **[{member.guild.member_count}](https://discord.gg/Yy6fyef6BY)**{emojies[":wuii:"]}\n( {emojies[":2_:"]}**`Количество бустов:`** **[{member.guild.premium_subscription_count}](https://discord.gg/Yy6fyef6BY)**{emojies[":rupee:"]}\n) {emojies[":3_:"]}**`Владелец сие мира:`** **{member.guild.owner.mention}**\n(ᅠˊᅠᅠᅠˎᅠᅠᅠˊᅠᅠᅠˎᅠᅠᅠˊ\n╰‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿ +.* ʚ𐐚', colour=COLOR_EMBEDS['neutral'])
	emb.set_thumbnail(url=member.avatar_url)
	emb.set_image(url=random.choice(gifs))
	channel = await bot.fetch_channel(channels["Приветствия"])
	row = ActionRow(Button(style=ButtonStyle.gray, label='Поздороваться', custom_id=cid))
	msg = await channel.send(embed=emb, components=[row])
	messages_for_edit.update({cid: [member, msg, emb]})

@bot.command(pass_context=True)
async def stats(ctx, member: discord.Member=None):
	if check_reg(ctx.message.author.id):
		if not_warns([int(y.id) for y in ctx.message.author.roles]):
			await ctx.send(check_stats(member.id if member is not None else ctx.message.author.id))
		else:
			await ctx.send("Нельзя использовать данную команду при наличии действующей роли варна.")
	else:
		await ctx.send("Невозможно использовать данную команду, пока Вы не зарегистрируете себя через команду /reg")

@bot.command(pass_context=True)
async def newseason(ctx):
	member_roles = [int(y.id) for y in ctx.message.author.roles]
	if ROLES['owner'] in member_roles or ROLES['delegate'] in member_roles:
		text, roles = new_season()
		for x in roles:
			try:
				member = await ctx.guild.fetch_member(x)
				for n in roles[x]:
					role = get(member.guild.roles, id=n)
					await member.remove_roles(role)
			except: pass
		await ctx.send(text)
	else:
		await ctx.send("У вас нету доступа к этой команде.")

@bot.command(pass_context=True)
async def mod(ctx, member: discord.Member=None):
	if if_moder([int(y.id) for y in ctx.message.author.roles]):
		await ctx.channel.purge(limit=1)
		if member is not None:
			if not(if_moder([int(y.id) for y in member.roles])):
				msg = await ctx.send("Вы точно хотите продолжить?", components = [[Button(style=ButtonStyle.blue, label='Продолжить', custom_id="yes"), Button(style=ButtonStyle.gray, label = "Отменить", custom_id = "cancel")]])
				interaction = await bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
				if interaction.component.id == "yes":
					await msg.delete()
					mms = await interaction.send(content=f"Выберите действие с <@{member.id}>:", components=[Select(placeholder = "Наказания", options = [SelectOption(label = "Исключение игрока с сервера", value = "kick"), SelectOption(label = "Текстовая затычка", value = "mute"), SelectOption(label = "Голосовая затычка", value = "vc_mute"), SelectOption(label = "Предупреждение", value = "warn"), SelectOption(label = "Блокировка на сервере", value = "ban")])])
					inter = await bot.wait_for("select_option")
					delegates = ",".join(f"<@{member.id}>" for member in get(ctx.guild.roles, id=ROLES['delegate']).members)

					if inter.values[0] == 'kick':
						await mms.delete()
						mms_1 = await inter.send(content="Напишите пункты причин через запятую.\nПравила сервера - https://delicate-airport-891.notion.site/a665f8b722f1496081374ed99c5f97d8")
						msg = await bot.wait_for('message'); reason = msg.content
						await mms_1.delete()
						await msg.delete()
						last = await ctx.send(f"Всё верно?\n\nНарушитель: <@{member.id}>\nПричина: {reason}\nТип наказания: kick", components = [[Button(style=ButtonStyle.blue, label='Подтвердить', custom_id="yes"), Button(style=ButtonStyle.gray, label = "Отменить", custom_id = "cancel")]])
						intt = await bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
						if intt.component.id == "yes":
							await last.delete()
							channel = await bot.fetch_channel(channels["Наказания"])
							log_msg = f"Выдал: <@{ctx.message.author.id}>\nНарушитель: <@{member.id}>\nПричина: {reason}\nТип наказания: kick"
							await channel.send(log_msg)
							await member.send(embed=discord.Embed(description=f"Вас исключили с сервера {member.guild.name}\n\nВыдал: <@{ctx.message.author.id}>\nПричина: {reason}\n\nПравила сервера (по пунктам): [*click*](https://delicate-airport-891.notion.site/a665f8b722f1496081374ed99c5f97d8)\nНе согласны с наказанием? Можете обратиться к руководству: <@{ADMIN_ID}>, {delegates}"))
							await member.kick(reason=log_msg)
							await intt.respond(content="Нарушитель наказан.")
						else:
							await last.delete()
							await intt.respond(content="Действие отменено.")

					if inter.values[0] in ['mute','vc_mute']:
						await mms.delete()
						mms_1 = await inter.send(content="Напишите пункты причин через запятую.\nПравила сервера - https://delicate-airport-891.notion.site/a665f8b722f1496081374ed99c5f97d8")
						msg = await bot.wait_for('message'); reason = msg.content
						await mms_1.delete()
						await msg.delete()
						mms_2 = await ctx.send(content="Выберите срок действия наказания.", components=[
							Select(
								placeholder = "Время", 
								options = [
									SelectOption(label = "30м", value = "1800"), 
									SelectOption(label = "1ч", value = "3600"), 
									SelectOption(label = "2ч", value = "7200"), 
									SelectOption(label = "3ч", value = "10800"),
									SelectOption(label = "4ч", value = "14400"),
									SelectOption(label = "5ч", value = "18000"),
									SelectOption(label = "6ч", value = "21600"),
									SelectOption(label = "7ч", value = "25200"),
									SelectOption(label = "8ч", value = "28800"),
									SelectOption(label = "9ч", value = "32400"),
									SelectOption(label = "10ч", value = "36000"),
									SelectOption(label = "11ч", value = "39600"),
									SelectOption(label = "12ч", value = "43200"),
									SelectOption(label = "24ч", value = "86400")
								])])
						intt = await bot.wait_for("select_option")
						time_mute, time_label = int(intt.values[0]), [x['label'] for x in intt.raw_data['message']['components'][0]['components'][0]['options'] if x['value'] == intt.values[0]][0]
						await mms_2.delete()
						last = await intt.send(f"Всё верно?\n\nНарушитель: <@{member.id}>\nПричина: {reason}\nВремя действия: {time_label}\nТип наказания: {inter.values[0]}", components = [[Button(style=ButtonStyle.blue, label='Подтвердить', custom_id="yes"), Button(style=ButtonStyle.gray, label = "Отменить", custom_id = "cancel")]])
						intt = await bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
						if intt.component.id == "yes":
							await last.delete()
							channel = await bot.fetch_channel(channels["Наказания"])
							log_msg = f"Выдал: <@{ctx.message.author.id}>\nНарушитель: <@{member.id}>\nПричина: {reason}\nВремя действия: {time_label}\nТип наказания: {inter.values[0]}"
							await channel.send(log_msg)
							role = get(member.guild.roles, id=ROLES[inter.values[0]])
							await member.add_roles(role, reason=log_msg)
							await intt.respond(content="Нарушитель наказан.")
							await asyncio.sleep(time_mute)
							await member.remove_roles(role, reason="Истёк срок наказания")
						else:
							await last.delete()
							await intt.respond(content="Действие отменено.")

					if inter.values[0] == 'ban':
						await mms.delete()
						mms_1 = await inter.send(content="Напишите пункты причин через запятую.\nПравила сервера - https://delicate-airport-891.notion.site/a665f8b722f1496081374ed99c5f97d8")
						msg = await bot.wait_for('message'); reason = msg.content
						await mms_1.delete()
						await msg.delete()
						mms_2 = await ctx.send(content="Выберите срок действия наказания.", components=[
							Select(
								placeholder = "Время", 
								options = [
									SelectOption(label = "1д", value = "86400"), 
									SelectOption(label = "7д", value = "604800"), 
									SelectOption(label = "15д", value = "1296000"),
									SelectOption(label = "30д", value = "2592000"),
									SelectOption(label = "Навсегда", value = "0")
								])])
						intt = await bot.wait_for("select_option")
						time_ban, time_label = int(intt.values[0]), [x['label'] for x in intt.raw_data['message']['components'][0]['components'][0]['options'] if x['value'] == intt.values[0]][0]
						await mms_2.delete()
						last = await intt.send(f"Всё верно?\n\nНарушитель: <@{member.id}>\nПричина: {reason}\nВремя действия: {time_label}\nТип наказания: ban", components = [[Button(style=ButtonStyle.blue, label='Подтвердить', custom_id="yes"), Button(style=ButtonStyle.gray, label = "Отменить", custom_id = "cancel")]])
						intt = await bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
						if intt.component.id == "yes":
							await last.delete()
							channel = await bot.fetch_channel(channels["Наказания"])
							log_msg = f"Выдал: <@{ctx.message.author.id}>\nНарушитель: <@{member.id}>\nПричина: {reason}\nВремя действия: {time_label}\nТип наказания: ban"
							await channel.send(log_msg)
							await member.send(embed=discord.Embed(description=f"Вас заблокировали на сервере {member.guild.name}\n\nВыдал: <@{ctx.message.author.id}>\nПричина: {reason}\nВремя действия: {time_label}\n\nПравила сервера (по пунктам): [*click*](https://delicate-airport-891.notion.site/a665f8b722f1496081374ed99c5f97d8)\nНе согласны с наказанием? Можете обратиться к руководству: <@{ADMIN_ID}>, {delegates}"))
							await member.ban(reason=log_msg)
							await intt.respond(content="Нарушитель наказан.")
							if time_ban != 0:
								await asyncio.sleep(time_ban)
								user = await bot.fetch_user(member.id)
								await ctx.guild.unban(user)
						else:
							await last.delete()
							await intt.respond(content="Действие отменено.")

					if inter.values[0] == 'warn':
						await mms.delete()
						mms_1 = await inter.send(content="Напишите пункты причин через запятую.\nПравила сервера - https://delicate-airport-891.notion.site/a665f8b722f1496081374ed99c5f97d8")
						msg = await bot.wait_for('message', check = lambda message: message.author == ctx.author); reason = msg.content
						await mms_1.delete()
						await msg.delete()
						mms_2 = await ctx.send(content="Выберите кол-во предупреждений.", components=[[Button(label='1', custom_id="1"), Button(label='2', custom_id="2"), Button(label='3', custom_id="3")]])
						intt = await bot.wait_for("button_click")
						warns_label = int(intt.component.id)
						await mms_2.delete()
						last = await intt.send(f"Всё верно?\n\nНарушитель: <@{member.id}>\nПричина: {reason}\nКоличество предупреждений: {warns_label}\nТип наказания: warn", components = [[Button(style=ButtonStyle.blue, label='Подтвердить', custom_id="yes"), Button(style=ButtonStyle.gray, label = "Отменить", custom_id = "cancel")]])
						intt = await bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
						if intt.component.id == "yes":
							await last.delete()
							channel = await bot.fetch_channel(channels["Наказания"])
							log_msg = f"Выдал: <@{ctx.message.author.id}>\nНарушитель: <@{member.id}>\nПричина: {reason}\nКоличество предупреждений: {warns_label}\nТип наказания: warn"
							await channel.send(log_msg)
							await member.send(embed=discord.Embed(description=f"Вам выданы предупреждения на сервере {member.guild.name}\n\nВыдал: <@{ctx.message.author.id}>\nПричина: {reason}\nКоличество предупреждений: {warns_label}\n\nПравила сервера (по пунктам): [*click*](https://delicate-airport-891.notion.site/a665f8b722f1496081374ed99c5f97d8)\nНе согласны с наказанием? Можете обратиться к руководству: <@{ADMIN_ID}>, {delegates}"))
							warns = len([y for y in member.roles if not(not_warns([int(y.id)]))])+warns_label
							member_nick = member.nick if member.nick is not None else member.name
							if warns < 3:
								role = get(member.guild.roles, id=warn_role[warns])
								await member.add_roles(role, reason=log_msg)
								if warns-warns_label == 0:
									await member.edit(nick=member_nick + " 🐁")
								await intt.respond(content="Нарушитель наказан.")
								await asyncio.sleep(604800)
								warns = len([y for y in member.roles if not(not_warns([int(y.id)]))])-warns_label
								role = get(member.guild.roles, id=warn_role[warns+warns_label])
								await member.remove_roles(role, reason="Истёк срок наказания")
								if warns == 0:
									await member.edit(nick=member_nick.replace("🐁", ""))
							else:
								await member.ban(reason=f"Выдал: {ctx.message.author}\nПричина: 3/3")
								await intt.respond(content="Нарушитель наказан.")
								await asyncio.sleep(604800)
								user = await bot.fetch_user(member.id)
								await ctx.guild.unban(user)

						else:
							await last.delete()
							await intt.respond(content="Действие отменено.")
				else:
					await msg.delete()
					await interaction.send(content="Действие отменено")
			else:
				await ctx.send("Использование этой команды не распространяется на персонал модерации.")
		else:
			await ctx.send("Использование: /mod <member>")
	else:
		await ctx.send("У вас нету доступа к этой команде.")

@bot.event
async def on_button_click(inter):
	if "hi_button" in inter.component.id:
		member, msg, emb = messages_for_edit[inter.component.id]
		if inter.author != member:
			await msg.edit(embed=emb, components=[])
			channel = await bot.fetch_channel(channels["Общий"])
			await channel.send(f'{member.mention}, вам сказал(а) привет - {inter.author.mention}')
			del messages_for_edit[inter.component.id]
		else:
			await inter.respond(content="Нельзя поздароваться с самим собой.")

	elif inter.component.id == "reg":
		if not(check_reg(inter.author.id)):
			if not_warns([int(y.id) for y in inter.author.roles]):
				await inter.send(content="Выберите платформу", components=[Select(placeholder = "Платформы", options = [SelectOption(label = "Steam", value = "steam"),SelectOption(label = "Origin", value = "origin"),SelectOption(label = "Xbox", value = "xbox"),SelectOption(label = "Playstation", value = "playstation")])])
				intt = await bot.wait_for("select_option")
				if intt.values[0] != "steam":
					await intt.send("Напишите свой никнейм в игре. (Нужно написать максимально точно, чтобы избежать похожих ников)")
					msg = await bot.wait_for('message', check = lambda message: message.author == inter.author); nickname = msg.content
					await msg.delete()
					text, roles = reg_track(inter.author.id, intt.values[0], nickname)
					if len(roles) == 0: await inter.author.send(text)
					else:
						for x in roles:
							role = get(inter.author.guild.roles, id=x)
							await inter.author.add_roles(role)
						await inter.author.edit(nick=nickname)
						await inter.author.send(text)
					data = get_info(inter.author.id)
					channel = await bot.fetch_channel(channels["Логи регистраций"])
					emb = discord.Embed(description=f"Зарегистрировался новый пользователь:\n\nDiscord: {inter.author.mention}\nУровень: {data['lvl']} lvl\nРанг: {data['rank']}\nРанг на арене: {data['rank_arena']}\nКол-во убийств: {data['murders']}\nПлатформа: {data['platform']}", colour=COLOR_EMBEDS['neutral'])
					emb.set_thumbnail(url=inter.author.avatar_url)
					await channel.send(embed=emb)
				else:
					if not(check_reg(inter.author.id)):
						await intt.respond(type=6)
						await inter.author.send("Вам нужно отправить скриншот своего профиля с данными арены или королевской битвы (Все зависит от того, где вы хотите зарегистрировать свой ранг).", components=[[Button(style=ButtonStyle.blue, label='Продолжить', custom_id="yes"), Button(label='Отменить', custom_id="-")]])
						intt = await bot.wait_for("button_click")
						if intt.component.id == "yes":
							await intt.send("Отправьте скриншот.")
							msg = await bot.wait_for("message", check = lambda message: message.author == inter.author and isinstance(message.channel, discord.DMChannel))
							try:
								png_url = msg.attachments[0].url
								with open("unknown.png", "wb") as f: f.write(requests.get(png_url).content)
								channel = await bot.fetch_channel(channels["Запросы ролей"])
								chan = await bot.fetch_channel(channels["Логи запросов"])
								await channel.send(f"Новый запрос роли от {inter.author.mention}:", file=discord.File("unknown.png"), components=[[Button(style=ButtonStyle.blue, label='Подтвердить', custom_id="yes"), Button(label='Отменить', custom_id="-")]])
								intt = await bot.wait_for("button_click")
								if intt.component.id == "yes":
									await intt.send(content="Выберите ранг", components=[Select(placeholder = "Королевская битва", options = [SelectOption(label = "Bronze", value = "Bronze"),SelectOption(label = "Silver", value = "Silver"),SelectOption(label = "Gold", value = "Gold"),SelectOption(label = "Platinum", value = "Platinum"),SelectOption(label = "Diamond", value = "Diamond"),SelectOption(label = "Master", value = "Master"),SelectOption(label = "Predator", value = "Predator")]),Select(placeholder = "Арена", options = [SelectOption(label = "Bronze", value = "Bronze_a"),SelectOption(label = "Silver", value = "Silver_a"),SelectOption(label = "Gold", value = "Gold_a"),SelectOption(label = "Platinum", value = "Platinum_a"),SelectOption(label = "Diamond", value = "Diamond_a"),SelectOption(label = "Master", value = "Master_a"),SelectOption(label = "Predator", value = "Predator_a")])])
									inttr = await bot.wait_for("select_option")
									rank = inttr.values[0]
									await inttr.send("Напишите никнейм, уровень и кол-во убийств игрока через пробел.")
									nickname, lvl, kills = (await bot.wait_for("message", check = lambda message: message.author == intt.author)).content.split(" ")
									await channel.purge(limit=1)
									text, roles = reg_steam(inter.author.id, nickname, rank, int(lvl), int(kills))
									for x in roles:
										role = get(inter.author.guild.roles, id=x)
										await inter.author.add_roles(role)
									await inter.author.edit(nick=nickname)
									await inter.author.send(text)
									data = get_info(inter.author.id)
									emb = discord.Embed(description=f"Зарегистрирован новый пользователь Steam:\n\nDiscord: {inter.author.mention}\nСкриншот: [*click*]({png_url})\nУровень: {data['lvl']} lvl\nРанг: {data['rank']}\nРанг на арене: {data['rank_arena']}\nКол-во убийств: {data['murders']}\nПлатформа: {data['platform']}", colour=COLOR_EMBEDS['neutral'])
									emb.set_thumbnail(url=inter.author.avatar_url)
									await chan.send(embed=emb)
								else:
									await intt.send("Напишите причину отмены.")
									msg = await bot.wait_for("message", check = lambda message: message.author == intt.author)
									await inter.author.send(f"Запрос на регистрацию был отклонён модератором.\nПричина: {msg.content}")
									await channel.send("Действие отменено.")
									await chan.send(embed=discord.Embed(description=f"Модератор {intt.author.mention} отменил запрос роли.\nЗапросил: {inter.author.mention}\nСкриншот: [*click*]({png_url})\nПричина отклонения: {msg.content}", colour=COLOR_EMBEDS['negative']))

							except IndexError:
								await inter.author.send(f"Вы должны были отправить скриншот своего профиля.\nПопробуйте заново зарегистрироваться в канале <#{channels['Регистрация']}>")
						else:
							await intt.send("Действие отменено.")
					else:
						await inter.author.send("Вы уже зарегистрированы.")
			else:
				await inter.respond(content="Нельзя использовать данную команду при наличии действующей роли варна.")
		else:
			await inter.send("Вы уже зарегистрированы.")

	elif inter.component.id == "update":
		if check_reg(inter.author.id):
			if not_warns([int(y.id) for y in inter.author.roles]):
				if get_platform(inter.author.id) != 'steam':
					text, roles = upd_track(inter.author.id)
					for i,x in enumerate(roles):
						for n in x:
							try:
								if not i:
									role = get(inter.author.guild.roles, id=n)
									await inter.author.remove_roles(role)
								else:
									role = get(inter.author.guild.roles, id=n)
									await inter.author.add_roles(role)
							except: pass
					await inter.send(text)
				else:
					await inter.send("Данная функция не работает для Steam пользователей :/")
			else:
				await inter.send("Нельзя использовать данную команду при наличии действующей роли варна.")
		else:
			await inter.send(f"Невозможно использовать данную команду, пока Вы не зарегистрируетесь в канале <#{channels['Регистрация']}>")

	elif inter.component.id == "Arank":
		if check_reg(inter.author.id):
			role_id = get_rank_roles(inter.author.id)[1]
			if role_id != 0:
				role = get(inter.author.guild.roles, id=role_id)
				if role_id in [int(y.id) for y in inter.author.roles]:
					await inter.author.remove_roles(role)
					await inter.send("Роль ранга на арене снята.")
				else:
					await inter.author.add_roles(role)
					await inter.send("Роль ранга на арене выдана.")
			else:
				btns = [[Button(style=5, label='Зарегистрировать КБ', url="https://discord.gg/bV9SWKtQ3K"), Button(style=5, label='Написать в поддержку', url="https://discord.gg/QGmFfzz9y5")]]
				await inter.send(embed=discord.Embed(description="**ОШИБКА!**\nОтсутствуют ваши данные с режима \"**Королевской Битвы**\".", colour=COLOR_EMBEDS['negative']),components=btns)
		else:
			await inter.send(f"Невозможно использовать данную команду, пока Вы не зарегистрируетесь в канале <#{channels['Регистрация']}>")

	elif inter.component.id == "KBrank":
		if check_reg(inter.author.id):
			role_id = get_rank_roles(inter.author.id)[0]
			if role_id != 0:
				role = get(inter.author.guild.roles, id=role_id)
				if role_id in [int(y.id) for y in inter.author.roles]:
					await inter.author.remove_roles(role)
					await inter.send("Роль ранга в кб снята.")
				else:
					await inter.author.add_roles(role)
					await inter.send("Роль ранга в кб выдана.")
			else:
				btns = [[Button(style=5, label='Зарегистрировать Арену', url="https://discord.gg/bV9SWKtQ3K"), Button(style=5, label='Написать в поддержку', url="https://discord.gg/QGmFfzz9y5")]]
				await inter.send(embed=discord.Embed(description="**ОШИБКА!**\nОтсутствуют ваши данные с режима \"**Арены**\".ᅠᅠᅠᅠᅠᅠᅠᅠ", colour=COLOR_EMBEDS['negative']),components=btns)
		else:
			await inter.send(f"Невозможно использовать данную команду, пока Вы не зарегистрируетесь в канале <#{channels['Регистрация']}>")

	elif inter.component.id in ['male','female','news','raffles','streams','tournaments']:
		role_id = ROLES[inter.component.id]
		role = get(inter.author.guild.roles, id=role_id)
		if role_id in [int(y.id) for y in inter.author.roles]:
			await inter.author.remove_roles(role)
			await inter.send("Роль снята.")
		else:
			await inter.author.add_roles(role)
			await inter.send("Роль выдана.")

@bot.event
async def on_select_option(inter):
	if "legends" in inter.values[0]:
		legend_role_id = mein_roles[inter.values[0].split('_')[1]]
		role = get(inter.author.guild.roles, id=legend_role_id)
		if legend_role_id in [int(y.id) for y in inter.author.roles]:
			await inter.author.remove_roles(role)
			await inter.send("Роль снята.")
		else:
			all_legends = len([y for y in inter.author.roles if int(y.id) in mein_roles_list])
			if all_legends < 3:
				await inter.author.add_roles(role)
				await inter.send("Роль выдана.")
			else:
				await inter.send("Можно выбрать максимум 3 мейн-легенды.")

bot.run(token)