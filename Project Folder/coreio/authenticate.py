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
    if mode == "payload":
        file_value = os.getenv(
            "SPOT_PAYLOAD_CREDENTIALS_FILE",
            "opt/payload_credentials/payload_guid_and_secret",
        )
        credentials_file = Path(file_value)
        if not credentials_file.is_file():
            raise AuthenticationConfigurationError(
                f"Payload credentials file not found: {credentials_file}"
            )
        return RobotCredentials(
            mode="payload",
            payload_credentials_file=credentials_file,
        )
    raise AuthenticationConfigurationError(
        "SPOT_AUTH_MODE must be 'user' or 'payload'"
    )

def read_payload_credentials(credentials_file: Path) -> tuple[str, str]:
    lines = [
        lines.strip()
        for line in credentials_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(lines) < 2:
        raise AuthenticationConfigurationError(
            "Payload credentials file must contain a GUID and secret"
        )
    return lines[0], lines[1]

def authenticate_robot(robot: Robot, credentials: RobotCredentials):
    if credentials.mode == "user":
        robot.authenticate(
            credentials.username,
            credentials.password,
        )
        return
    if credentials.mode == "payload":
        guid, secret = read_payload_credentials(credentials.payload_credentials_file)
        robot.authenticate_from_payload_credentials(guid, secret,)
        return
    raise AuthenticationConfigurationError(
        f"Unsupported authentication mode: {credentials.mode}"
    )