from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import bosdyn.client
from bosdyn.client.robot import Robot

class AuthenticationConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class RobotCredentials:
    mode: str
    username: str | None = None
    password: str | None = None
    payload_credentials_file: Path | None = None


def load_credentials() -> RobotCredentials:
    mode = os.getenv("SPOT_AUTH_MODE", "payload").strip().lower()
    if mode == "user":
        username = os.getenv("SPOT_USERNAME")
        password = os.getenv("SPOT_PASSWORD")
        if not username or not password:
            raise AuthenticationConfigurationError(
                "SPOT_USERNAME and SPOT_PASSWORD are required"
            )
        return RobotCredentials(
            mode="user",
            username=username,
            password=password,
        )