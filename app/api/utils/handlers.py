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
