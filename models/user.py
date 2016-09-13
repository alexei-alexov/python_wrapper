"""
This module work with users table
"""

import controllers


class User(object):
    """
    This class is python representation of users row
    """
    
    def __init__(self, fullname, email, password, avatar, is_active, role_id, id=-1):
        """
        Default user initializer
        """
        self.fullname = fullname
        self.email = email
        self.password = password
        self.avatar = avatar
        self.is_active = is_active
        self.role_id = role_id
        self.id = id

    def get_tuple(self, need_id=False):
        return (self.id,) if need_id else () + (self.fullname, self.email, self.password, self.avatar, self.is_active, self.role_id)

class UserController(object):
    """
    This class provide all main work with user data between database and append
    """
    
    self.__table_name = "users"

    self.fields = ("fullName", "email", "password", "avatar", "isActive", "role_id")
    
    def get_fields(self):
        """
        Return all users table fields exept of id
        """
        return self.fields


    def add_user(self, wrapper, user):
        """
        This method allow to add one from python instance to SQL database
        
        Args:
            wrapper (Wrapper): wrapper with connection
            user (User): user to add
        """
        user.id = wrapper.insert(self.__table_name, self.get_fields(), user.get_tuple())


    def add_all_users(self, wrapper, users):
        """
        This method allow to add list of users into database
        
        Args:
            wrapper (Wrapper): wrapper with connection
            users (list(User)): list of users to add
        """
        for user in users:
            self.add_user(wrapper, user)


    def update_user(self, wrapper, user):
        """
        This method update selected user, user should be in database
        """
        if user.id == -1:
            raise WrongData("User is not in a table")

        wrapper.update(User.__table_name, user.get_fields(), "id = " + user.id)


    def delete_user(self, wrapper, user):
        """
        This method delete choosen user, user should be in database
        """
        if user.id == -1:
            raise WrongData("User is not in a table")

        wrapper.delete(User.__table_name, "id = " + user.id)


    def get_user(self, wrapper, id):
        """
        This method return user with specific id
        """
        if id <= 0:
            raise WrongData("Id cannot be negative")

        wrapper.select(User.__table_name, self.get_fields(), "id = " + id)
