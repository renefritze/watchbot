import string

from tasbot.plugin import IPlugin
from tasbot.config import *


class Main(IPlugin):
	def __init__(self, name, tasclient):
		IPlugin.__init__(self, name, tasclient)
		self.admins = []

	def onpong(self):
		self.logger.debug("pong")
		for (user,pidfile) in self.bots:
			if not user in self.tasclient.users:
				self.logger.error('bot %s not found ckilling pidfile %s'%(user,pidfile))
				os.system('/usr/local/bin/ckill %s'%pidfile)

	def onload(self, tasc):
		self.app = tasc.main
		self.admins = self.app.config.GetOptionList('tasbot', "admins")
		self.bots = self.app.config.items('watchbot') 

