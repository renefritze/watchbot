import string

from tasbot.plugin import IPlugin
from tasbot.config import *


class Main(IPlugin):
	def __init__(self, name, tasclient):
		IPlugin.__init__(self, name, tasclient)
		self.admins = []

	def oncommandfromserver(self, command, args, socket):
		pass

	def onload(self, tasc):
		self.app = tasc.main
		self.admins = self.app.config.GetOptionList('tasbot', "admins")
