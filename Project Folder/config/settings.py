from __future__ import annotations

import os
from dataclasses import dataclass

def _get_bool(env_name: str, default:bool = False) -> bool:
    value = os.getenv(env_name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")

@dataclass(frozen=True)
class Settings:
    hostname: str
    username: str
    password: str
    port: int
    timeout_seconds: int
    verbose: bool
    save_image_path: str

def get_settings() -> Settings:
    return Settings(
        hostname=os.getenv("SPOT_HOSTNAME", os.getenv("SPOT_HOSTNAME", "192.168.80.3")),
        username=os.getenv("SPOT_USERNAME", os.getenv("SPOT_USERNAME", "user")),
        password=os.getenv("SPOT_PASSWORD", os.getenv("SPOT_PASSWORD", "")),
        port=int(os.getenv("SPOT_PORT", os.getenv("SPOT_PORT", "443"))),
        timeout_seconds=int(os.getenv("SPOT_TIMEOUT_SECONDS", os.getenv("SPOT_TIMEOUT_SECONDS", "30"))),
        verbose=_get_bool("SPOT_VERBOSE", False),
        save_image_path=os.getenv("SPOT_SAVE_IMAGE_PATH", os.getenv("SPOT_SAVE_IMAGE_PATH", "./images"))
    )

@dataclass(frozen=True)
class CoreIOSettings:
    hostname: str
    username: str
    password: str
    port: int
    timeout_seconds: int
    verify_tls: bool

def get_coreio_settings() -> CoreIOSettings:
    return CoreIOSettings(
        hostname=os.getenv("COREIO_HOSTNAME", os.getenv("COREIO_HOSTNAME", "192.168.80.3")),
        username=os.getenv("COREIO_USERNAME", os.getenv("COREIO_USERNAME", "user")),
        password=os.getenv("COREIO_PASSWORD", os.getenv("COREIO_PASSWORD", "")),
        port=int(os.getenv("COREIO_PORT", os.getenv("COREIO_PORT", "443"))),
        timeout_seconds=int(os.getenv("COREIO_TIMEOUT_SECONDS", os.getenv("COREIO_TIMEOUT_SECONDS", "30"))),
        verify_tls=_get_bool("COREIO_VERIFY_TLS", True)
    )

def get_spot_config() -> dict:
    settings = get_settings()
    return {
        "hostname": settings.hostname,
        "username": settings.username,
        "password": settings.password,
        "port": settings.port,
        "timeout_seconds": settings.timeout_seconds,
        "verbose": settings.verbose,
        "save_image_path": settings.save_image_path
    }