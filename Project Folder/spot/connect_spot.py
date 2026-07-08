import os
from typing import Optional
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util

from robot_config import get_hostname, get_username, get_password

DEFAULT_SDK_NAME = "DoorInspecClient"

def _apply_credentials_from_env() -> None:
    username = get_username()
    password = get_password()
    if username and password:
        os.environ["BOSDYN_CLIENT_USERNAME"] = username
        os.environ["BOSDYN_CLIENT_PASSWORD"] = password

def create_sdk(sdk_name: str = DEFAULT_SDK_NAME) -> bosdyn.client.Sdk:
    return bosdyn.client.create_standard_sdk(sdk_name)

def connect_spot(hostname: Optional[str] = None, verbose: bool = False):
    hostname = hostname or get_hostname()
    bosdyn.client.util.setup_logging(verbose)
    _apply_credentials_from_env()

    sdk = create_sdk()
    robot = sdk.create_robot(hostname)
    bosdyn.client.util.authenticate(robot)
    robot.time_sync.wait_for_sync()

    if robot.is_estopped():
        raise RuntimeError("Robot is estopped. Please use the client to configure E-Stop.")
    
    return robot

def acquire_lease(robot, must_acquire: bool = True, return_at_exit: bool = True):
    lease_clent = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    return bosdyn.client.lease.LeaseKeepAlive(lease_clent, must_acquire=must_acquire, return_at_exit=return_at_exit)
