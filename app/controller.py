# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Functions

from app.models import User
import hashlib
import os


class UserConfig():
    """A class for temporary storage of user settings.
    """
    def __init__(self, id):
        self.id: int = id
        self.first_name: str = None
        self.last_name: str = None
        self.username: str = None
        self.language_code: str = None
        self.is_bot: bool = None
        self.town: str = None
        self.password: bytes = None
        self.time: int = None
        self.day: int = None
        self.quantity: int = None
        self.salt: bytes = None

    def all_data(self) -> dict:
        result = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'language_code': self.language_code,
            'is_bot': self.is_bot,
            'town': self.town,
            'password': self.password,
            'time': self.time,
            'day': self.day,
            'quantity': self.quantity,
            'salt': self.salt
        }
        return result


def check_user_in_db(name: int) -> bool:
    """Searching for a database entry by user ID

    Args:
        name (int): User ID (unique)

    Returns:
        bool: Returns True or False
    """
    dbquery = User.select(User.q.userID == name)
    result = bool(dbquery.count())
    return result


def write_user_in_db(data: dict) -> None:
    """Database settings recording

    Args:
        data (dict): dictionary of user settings
    """
    User(userID=data['id'],
         userFirstName=data['first_name'],
         userLastName=data['last_name'],
         userName=data['username'],
         languageCode=data['language_code'],
         isBot=data['is_bot'],
         userTown=data['town'],
         userPassword=data['password'],
         remindTime=data['time'],
         remindDay=data['day'],
         remindQuantity=data['quantity'],
         salt=data['salt']
         )
    return


def delete_user_in_db(name: str) -> None:
    """Delete for a database entry by user ID

    Args:
        name (str): User ID (unique)
    """
    dbquery = User.select(User.q.userID == name)
    User.delete(dbquery[0].id)
    return


def read_user_in_db(user_id: int) -> dict:
    """Reading user settings from the database

    Args:
        user_id (int): User ID (unique)

    Returns:
        dict: Returns the dictionary with all user settings
    """
    dbquery = User.select(User.q.userID == user_id)
    result = {
        'id': dbquery[0].userID,
        'first_name': dbquery[0].userFirstName,
        'last_name': dbquery[0].userLastName,
        'username': dbquery[0].userName,
        'language_code': dbquery[0].languageCode,
        'is_bot': dbquery[0].isBot,
        'town': dbquery[0].userTown,
        'password': dbquery[0].userPassword,
        'time': dbquery[0].remindTime,
        'day': dbquery[0].remindDay,
        'quantity': dbquery[0].remindQuantity,
        'salt': dbquery[0].salt
        }
    return result


def hash_password(password: str, salt: bytes = None, salt_len: int = 32,
                  algorithm: str = 'sha512', iteration: int = 10000,
                  _dklen: int = 64) -> dict:
    """ Function generates password hash
        When only one password is transmitted,
        new salt and hash will be generated.
        When passing the password and salt,
        a hash will be generated using the passed salt.

    Args:
        password (str): password.
        salt (bytes, optional): salt.
        salt_len (int, optional): Length of newly generated salt (at least 32).
        Defaults to 32.
        algorithm (str, optional): Selecting a hash generation algorithm:
        SHA1, SHA224, SHA256, SHA384, and SHA512. Defaults to 'sha512'.
        iteration (int, optional): iteration number. Defaults to 10000.
        _dklen (int, optional): The length of the generated hash key.
        Defaults to 64.

    Returns:
        Dict: returns a dictionary with salt and password hash.
    """
    if salt is None:
        salt = os.urandom(salt_len)
    else:
        salt = salt
    b_password = password.encode(encoding='utf-8')
    hash_from_password = hashlib.pbkdf2_hmac(
        algorithm,
        b_password,
        salt,
        iteration,
        dklen=64
    )
    result = {
        'salt': salt,
        'hash': hash_from_password
    }
    return result
