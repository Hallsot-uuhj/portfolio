import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
import pymysql.cursors

def connection():
	connection = pymysql.connect(host='localhost', user='root', password='root', db='vkbot', cursorclass=pymysql.cursors.DictCursor)
	return connection

def sys():
	vk_s = vk_api.VkApi(token='token')
	return vk_s.get_api(), VkBotLongPoll(vk_s,199992660)