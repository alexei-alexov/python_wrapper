"""
This module is used to work with bicycle
"""


class Bicycle(object):
    """
    This class is model representation of bicycle row
    """

    def __init__(self, name, description, is_deleted, user_id, id=-1):
        """
        Default init
        """

        self.name = name
        self.description = description
        self.is_deleted = is_deleted
        self.user_id = user_id
        self.id = id

    def get_data(self, need_id=False):
        result = (self.name, self.description, self.is_deleted, self.user_id)
        if need_id:
            result += (self.id,)
        return result

    def __repr__(self):
        return str(self.get_data(True))


class CicycleController(object):
    """
    This class provides work with bicycle in SQL
    """

    table_name = "bicycles"
    fields = ("name", "description", "isDeleted", "user_id")

    def get_fields(self, need_id=False):
        """
        Return fields tuple
        """
        result = self.fields

        if need_id:
            result += "id"
        return result

    def add_bicycle(self, wrapper, bicycle):
        """
        This method add bicycle instance to table
        """
        wrapper.insert(wrapper, self.get_fields(), bicycle.get_data())

    def update_bicycle(self, wrapper, bicycle):
        """
        This method update bicycle row
        """
        if user.id == -1:
            raise WrongData("Bicycle is not in a table")

        data_row = bicycle.get_data()
        fields = self.get_fields()
        # prepare set statement in update
        set_query = "{} = {}, " * (len(data_row) - 1) + "{} = {}"
        #

        def filter_func(i):
            data_row[(i - 1) / 2] if i % 2 == 1 else fields[i / 2]

        length = len(data_row)*2
        formated = set_query.format(*filter(filter_func, range(length)))
        wrapper.\
            update(self.table_name, bicycle.get_data(), "id = " + bicycle.id)

    def delete_bicycle(self, wrapper, bicycle):
        """
        This method delete choosen bicycle, user should be in database
        """
        if user.id == -1:
            raise WrongData("Bicycle is not in a table")

        wrapper.delete(self.table_name, "id = " + bicycle.id)

    def get_user(self, wrapper, id):
        """
        This method return bycicle with specific id
        """
        if id <= 0:
            raise WrongData("Id cannot be negative")

        return wrapper.select(self.table_name, self.get_fields(), "id = " + id)

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
