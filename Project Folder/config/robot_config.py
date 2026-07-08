import os

DEFAULT_HOSTNAME = os.getenv("SPOT_HOSTNAME", "192.186.80.3")
DEFAULT_USERNAME = os.getenv("SPOT_USERNAME", "user")
DEFAULT_PASSWORD = os.getenv("SPOT_PASSWORD", "mz9jmfhp68o7")

def get_robot_config():
    return {
        "hostname": DEFAULT_HOSTNAME,
        "username": DEFAULT_USERNAME,
        "password": DEFAULT_PASSWORD
    }

def get_hostname():
    return DEFAULT_HOSTNAME

def get_username():
    return DEFAULT_USERNAME

def get_password():
    return DEFAULT_PASSWORD
