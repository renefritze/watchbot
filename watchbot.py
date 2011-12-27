import string

from tasbot.plugin import IPlugin
from tasbot.config import *

class Bot(object):
	def __init__(self,name,configline):
		pair = Config.parselist(configline,',')
		self.name = name
		self.pm_cmd = pair[0]
		self.pidfile = pair[1]
		self.when_killed = 0

class Main(IPlugin):
	def __init__(self, name, tasclient):
		IPlugin.__init__(self, name, tasclient)
		self.admins = []
		self.waiting_for_reply = []
		#this equals 130s since ping time is hardcoded to 10s
		self.when_killed_wait = 13

	def _killbot(self,bot):
		msg = 'bot %s not found ckilling pidfile %s'%(bot.name,bot.pidfile)
		self.logger.error(msg)
		os.system('/usr/local/bin/ckill %s'%bot.pidfile)
		for admin in self.admins:
			self.tasclient.saypm(admin, msg)
		
	def onpong(self):
		self.logger.debug("pong")
		for bot in self.bots:
			if not bot.name in self.tasclient.users:
				if bot.when_killed == 0:
					self._killbot(bot)
				if bot.when_killed < self.when_killed_wait:
					bot.when_killed += 1
				else:
					#ALARM!
					pass
			else:
				bot.when_killed = 0
				self.waiting_for_reply.append( bot.name )
				self.tasclient.saypm( bot.name, bot.pm_cmd )
		
			
	def onsaidprivate(self, user, message):
		#clear user from queue
		if message != '':
			self.waiting_for_reply = filter (lambda a: a == user, self.waiting_for_reply)
			
	def onload(self, tasc):
		self.app = tasc.main
		self.admins = self.app.config.GetOptionList('tasbot', "admins")
		self.bots = [ Bot(name,cfg) for (name,cfg) in self.app.config.items('watchbot') ]

