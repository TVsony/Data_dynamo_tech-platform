from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, db):
        self.collection = db['users']

    def create_user(self, email, password):
        hashed_pw = generate_password_hash(password)
        self.collection.insert_one({'email': email, 'password': hashed_pw})

    def find_user(self, email):
        return self.collection.find_one({'email': email})

    def check_password(self, stored_pw, given_pw):
        return check_password_hash(stored_pw, given_pw)
