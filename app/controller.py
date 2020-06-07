from app.models import User


def check_user(name: str) -> bool:
    dbquery = User.select(User.q.userID == name)
    result = bool(dbquery.count())
    return result


def write_user(data: dict):
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
         remindQuantity=data['quantity']
         )
    return


def delete_user(name: str):
    dbquery = User.select(User.q.userID == name)
    User.delete(dbquery[0].id)
    return


def read_user(user_id: int) -> dict:
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
        'quantity': dbquery[0].remindQuantity
        }
    return result
