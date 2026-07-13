from __future__ import annotations

import logging
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any
import requests
from settings import get_coreio_settings

logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings(category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

@dataclass(frozen=True)
class CoreIOClient:
    hostname: str
    username: str
    password: str
    port: int
    timeout_seconds: int
    verify_tls: bool

    def __post_init__(self):
        object.__setattr__(self, "base_url", f"https://{self.hostname}:{self.port}")
        object.__setattr__(self, 'session', requests.Session())
        self.session.verify = self.verify_tls
        self.session.headers.update({'Content-Type': 'application/json'})
        self.authenticated = False

    def login(self) -> bool:
        logger.debug('Core I/O login: fetching CSRF token from %s', self.base_url)
        response = self.session.get(self.base_url, timeout=self.timeout_seconds)
        response.raise_for_status()

        csrf_token = response.cookies.get('csrftoken')
        if not csrf_token:
            logger.error('Core I/O login failed: CSRF token not found in response cookies')
            return False
        
        login_data = {'username': self.username, 'password': self.password}
        login_response = self.session.post(
            f'{self.base_url}/api/v0/login',
            data=login_data,
            headers={'X-CSRFToken': csrf_token},
            timeout=self.timeout_seconds
        )

        if login_response.status_code != HTTPStatus.OK:
            logger.error('Core I/O login failed: %s %s', login_response.status_code, login_response.text)
            self.authenticated = False
            return False
        
        login_json = login_response.json()
        if 'error' in login_json:
            logger.error('Core I/O login failed: %s', login_json['error'])
            self.authenticated = False
            return False
        
        self.authenticated = True
        logger.info('Core I/O login successful')
        return True
    
    def get(self, path: str, **kwargs: Any) -> requests.Response:
        self._ensure_authenticated()
        return self.session.get(f'{self.base_url}{path}', timeout=self.timeout_seconds, **kwargs)
    
    def post(self, path: str, data: Any | None = None, json: Any | None =None, **kwargs: Any) -> requests.Response:
        self._ensure_authenticated()
        return self.session.post(
            f'{self.base_url}{path}', data=data, json=json, timeout=self.timeout_seconds, **kwargs
        )
    
    def get_extensions_status(self) ->dict[str, Any]:
        response = self.get('/api/v0/extensions/status')
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            self.login()
            response = self.get('/api/v0/extensions/status')
        response.raise_for_status()
        return response.json()
    
    def get_extensions_list(self) -> dict[str, Any]:
        response = self.get('/api/v0/extensions/list')
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            self.login()
            response = self.get('/api/v0/extensions/list')
        response.raise_for_status()
        return response.json()
    
    def _ensure_authenticated(self):
        if not self.authenticated:
            if not self.login():
                raise RuntimeError('Unable to authenticate with Core I/O. Please check your credentials and try again.')
            
def create_coreio_client() -> CoreIOClient:
    settings = get_coreio_settings()
    return CoreIOClient(
        hostname=settings.hostname,
        username=settings.username,
        password=settings.password,
        port=settings.port,
        timeout_seconds=settings.timeout_seconds,
        verify_tls=settings.verify_tls
    )

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Connect to Core I/O and query status")
    parser.add_argument('--status', action='store_true', help='Get the status of Core I/O extensions')
    parser.add_argument('--list', action='store_true', help='Get the list of Core I/O extensions')
    args = parser.parse_args()

    client = create_coreio_client()
    if not client.login():
        raise SystemExit(1)
    
    if args.status:
        print(client.get_extensions_status())
    elif args.list:
        print(client.get_extensions_list()) 
    else:
        print("Core I/O client is ready. Use --status or --list to query extensions.")