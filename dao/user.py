class User(object):
    """ Modeling user object class to encapsulate user_id and dob."""
    user_id = None
    dob = None

    def __init__(self, user_id, dob):
        self.user_id = user_id
        self.dob = dob

    def get_id(self):
        return self.user_id

    def get_birthday(self):
        return self.dob
