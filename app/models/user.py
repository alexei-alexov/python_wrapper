"""
This module work with users table
"""


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

    def get_data(self, need_id=False):
        result = (self.fullname, self.email, self.password, self.avatar, 1 if self.is_active else 0, self.role_id)
        if need_id:
            result += (self.id,)
        return result

    def __repr__(self):
        return str(self.get_data(True))


class UserController(object):
    """
    This class provide all main work with user data between database and append
    """

    table_name = "users"

    fields = ("fullName", "email", "password", "avatar", "isActive", "role_id")

    def row_to_user(self, row):
        """
        This method accept row from select query
        and translate it into user instance
        """
        return User(*row[0:])

    def get_fields(self, need_id=False):
        """
        Return all users table fields exept of id
        """
        result = self.fields
        if need_id:
            result += ("id",)
        return result

    def add_user(self, wrapper, user):
        """
        This method allow to add one from python instance to SQL database

        Args:
            wrapper (Wrapper): wrapper with connection
            user (User): user to add
        """
        print self.get_fields(), user.get_data()
        user.id = \
            wrapper.insert(self.table_name, self.get_fields(), user.get_data())

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

        data_row = user.get_data()
        fields = self.get_fields()
        # prepare set statement in update
        set_query = "fullName = '{}', email = '{}', password = '{}', avatar = '{}', isActive = {}, role_id = {}".format(*user.get_data())
        #

        wrapper.update(self.table_name, set_query, "id = " + str(user.id))

    def delete_user(self, wrapper, user):
        """
        This method delete choosen user, user should be in database
        """
        if user.id == -1:
            raise WrongData("User is not in a table")

        wrapper.delete(self.table_name, "id = " + str(user.id))

    def get_user(self, wrapper, id):
        """
        This method return user with specific id
        """
        if id <= 0:
            raise WrongData("Id cannot be negative")

        return self.row_to_user(*wrapper.select(self.table_name, self.get_fields(True), "id = " + str(id)))

    def get_all_users(self, wrapper):
        """
        This method return all users in table
        """

        result = []

        for row in wrapper.select(self.table_name, self.get_fields(True)):
            result.append(self.row_to_user(row))

        return result

    def get_users_by_field(self, wrapper, field, value):
        """
        This method return all users with specified field value
        """
        result = []

        where = "{0} = {1}".format(field, value)
        select = wrapper.select(self.table_name, self.get_fields(True), where)
        for row in select:
            result.append(self.row_to_user(row))

        return result
