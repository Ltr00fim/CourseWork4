import base64
import hashlib
import hmac
from dao.user import UserDao
from config import Config


class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def create(self, data):
        data["password"] = self.get_hash(data["password"])
        return self.dao.create(data)

    def update(self, data):
        uid = data["id"]
        user = self.get_one(uid)

        user.email = data["email"]
        user.password = data["password"]
        user.name = data["name"]
        user.surname = data["surname"]
        user.favorite_genre = data["favorite_genre"]

        return self.dao.update(user)

    def update_partial(self, data, uid):
        user = self.get_one(uid)
        if "password_1" and "password_2" in data:
            if self.get_hash(data["password_1"]) == user.password:
                user.password = self.get_hash(data["password_2"])
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = data["password"]
            user.password = self.get_hash(data["password"])
        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "favorite_genre" in data:
            user.favorite_genre = data["favorite_genre"]
        return self.dao.update(user)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_password(self, password_hash, other_password):
        decoded_digist = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            other_password.encode("utf-8"),
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digist, hash_digest)
