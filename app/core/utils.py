import secrets
import string


def handle_server_down():
    return {
        "status": "false",
        "message": "Database server is down. Please try again later. D:"
    }


def handle_server_up():
    return {
        "status": "true",
        "message": "Database server is up. :D"
    }


def generate_user_id(length=30):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(secrets.choice(characters) for i in range(length))
    return random_id
