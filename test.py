from app.controllers.orm import *
from app.models.user import *
import json


wrapper = Wrapper(json.load(open("config.json", 'r')))
user_controller = UserController()
user1 = User("Grigorii", "g@gmail.com", "fff", "avatar", True, 2)
user_controller.add_user(wrapper, user1)
try:
    # user1.email = "new_mail@gmail.com"
    # user_controller.update_user(wrapper, user1)
    # print user_controller.get_all_users(wrapper)
    print user_controller.get_user(wrapper, user1.id)
finally:
    pass
    # user_controller.delete_user(wrapper, user1)
