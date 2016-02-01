

class UserAware:

    @classmethod
    def all(cls, user_id):
        return cls.query.filter_by(user_id = user_id).all()
