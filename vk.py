# -*- coding: utf-8 -*-
import requests, json, Image
from StringIO import StringIO
from settings import token, groupId

class VkBot:
	
	def __init__(self, token, groupId):
		self.token = token
		self.groupId = groupId
	
	def requestVkApi(self, method, payload):
		"""	Функция для запроса к API"""
		url = 'https://api.vk.com/method/%s' %method
		res = requests.get(url, params=payload, timeout=5)
		return res.text
		
	def groupMembers(self):
		"""Функция для получения подписчиков паблика"""
		idInGroup = json.loads(self.requestVkApi('groups.getMembers', {'group_id':self.groupId,'access_token':self.token}))[u'response'][u'users']
		return idInGroup

	def inviteGroupMembers(self, idUser, captchaKey=None, captchaSid=None):
		"""Функция для приглашения в друзья подписчиков паблика"""
		idInvite = json.loads(self.requestVkApi('friends.add', {'user_id':idUser,'access_token':self.token,'captcha_key':captchaKey,'captcha_sid':captchaSid}))
		if 'error' in idInvite:
			#print idInvite['error']['error_code'], idInvite['error']['error_msg'], 'id =',idInvite['error']['request_params'][3]['value']
			if idInvite['error']['error_code']==14:
				captcha = Image.open(StringIO(requests.get(str(idInvite['error']['captcha_img'])).content))
				captcha.show()
				raw = raw_input("Введите каптчу, пожалуйста: ")
				print "Повторим запрос: ", self.inviteGroupMembers(idUser,str(raw),str(idInvite['error']['captcha_img'][34:46]))
				#requestVkApi('friends.add', {'user_id':str(id),'access_token':token,'captcha_key':str(raw),'captcha_sid':str(idInvite['error']['captcha_img'][34:46])})
		else:
			if idInvite['response']==1:
				print "Отправлена заявка на добавление пользователя %s в друзья" % idUser
			elif idInvite['response']==2:
				print "Вы уже отправляли заявку на добавления пользователя %s" %idUser
			elif idInvite['response'] == 4:
				print "Повторная отправка заявки пользователю %s" % idUser

if __name__ == '__main__':
	vkBot = VkBot(token,groupId)	
	print "id подписчиков паблика %s:\n" %groupId
	print vkBot.groupMembers()
	print "\n"
	for id in vkBot.groupMembers():
		vkBot.inviteGroupMembers(id)
	#vkBot.inviteGroupMember('248194698')
	

	


