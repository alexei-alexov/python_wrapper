"""
This module launch app
"""

from app import *
import json

config = json.load(open("config.json", "r"))

wrapper = controllers.orm.Wrapper(config)

user_controller = models.user.UserController()

user_1 = \
    models.user.User("fullName1", "email1", "password1", "avatar", True, 1)

user_controller.add_user(wrapper, user_1)
user_list = user_controller.get_all_users(wrapper)
print user_list
