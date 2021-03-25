import os
import sys
import traceback

from cbircbot2.modules.Users.db.db import UserDB
from cbircbot2.core.sockets import  Socket
from cbircbot2.core.params import  EnvironmentParams
from cbircbot2.core.client import IrcClient
from cbircbot2.core.modules import IrcModules
from cbircbot2.core.input import InputText

from cbircbot2.modules.Users.db.models.AdminModel import AdminModel, UserModel
from cbircbot2.modules.Users.db.models.PiadaModel import PiadaModel
db = UserDB('d','localhost',9100)
