import logging
from typing import Any, Dict, Optional

import aiohttp
import ujson
from utils.error import *
from ujson import JSONDecodeError
from utils.auth import ed25519_signature, hmac_hashing, rsa_signature
from utils.format import cleanNoneValue, encoded_string
from utils.util import get_timestamp
from aiohttp.client import ClientTimeout
from aiohttp.client_reqrep import ClientResponse
from types import TracebackType



class BinanceBase:
    API_URL: str = "https://api.binance.com"
    API_RATE_LIMIT_PER_SEC: int = 1
    PAIR_TRADE_RATE_COUNTER_LIMIT: int = 150
    __version__: str = "3.10"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: Optional[str] = API_URL,
        timeout: Optional[int] = None,
        proxies: Optional[Dict[str, str]] = None,
        show_limit_usage: bool = False,
        show_header: bool = False,
        private_key: Optional[str] = None,
        private_key_pass: Optional[str] = None,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.timeout = timeout
        self.proxies = proxies
        self.show_limit_usage = show_limit_usage
        self.show_header = show_header
        self.private_key = private_key
        self.private_key_pass = private_key_pass
        self.session = aiohttp.ClientSession(
            headers={
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "binance-connector-python/" + self.__version__,
                "X-MBX-APIKEY": api_key,
            }
        )

        if show_limit_usage:
            self.show_limit_usage = True

        if show_header:
            self.show_header = True

        if isinstance(proxies, dict):
            self.proxies = proxies

        self._logger = logging.getLogger(__name__)

    def check_credential(self) -> bool:
        if self.api_key and self.api_secret:
            return True
        return False

    async def query(self, url_path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return await self.send_request("GET", url_path, payload=payload)

    async def _get_sign(self, payload: str) -> str:
        if self.private_key:
            try:
                return ed25519_signature(self.private_key, payload, self.private_key_pass)
            except ValueError:
                return rsa_signature(self.private_key, payload, self.private_key_pass)
        else:
            return hmac_hashing(self.api_secret, payload)

    async def sign_request(
        self, http_method: str, url_path: str, payload: Optional[Dict[str, Any]] = None
    ) -> Any:
        if payload is None:
            payload = {}
        payload["timestamp"] = get_timestamp()
        query_string = self._prepare_params(payload)
        payload["signature"] = await self._get_sign(query_string)
        print(f"sign is {payload}")
        return await self.send_request(http_method, url_path, payload)

    async def send_request(
        self, http_method: str, url_path: str, payload: Optional[Dict[str, Any]] = None
    ) -> Any:
        if payload is None:
            payload = {}
        url = self.base_url + url_path
        self._logger.debug("url: " + url)
        params = cleanNoneValue(
            {
                "url": url,
                "params": self._prepare_params(payload),
                "timeout": self.timeout,
                "proxy": self.proxies,
            }
        )

        timeout = ClientTimeout(total=15)
        async with getattr(self.session, http_method.lower())(**params) as response:
            response_data = await response.json()

            self._logger.debug("raw response from server:" + await response.text())
            # self._handle_exception(response)

            try:
                data = await response.json()
            except ValueError:
                data = await response.text()

            result = {}

            if self.show_limit_usage:
                limit_usage = {}
                for key in response.headers.keys():
                    key = key.lower()
                    if (
                        key.startswith("x-mbx-used-weight")
                        or key.startswith("x-mbx-order-count")
                        or key.startswith("x-sapi-used")
                    ):
                        limit_usage[key] = response.headers[key]
                result["limit_usage"] = limit_usage

            if self.show_header:
                result["header"] = response.headers

            if len(result) != 0:
                result["data"] = data
                return result
            logging.info(f"data is {data}")
            return data

    async def __aenter__(self) -> 'BinanceBase':
        return self

    async def __aexit__(self, exc_type: Optional[type], exc_value: Optional[Exception], traceback: Optional[TracebackType]) -> None:
        await self.session.close()

    def _prepare_params(self, params: Dict[str, Any]) -> str:
        return encoded_string(cleanNoneValue(params))

    def _handle_exception(self, response: ClientResponse) -> None:
        status_code = response.status
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = ujson.loads(response.text)
            except JSONDecodeError:
                raise ClientError(
                    status_code, None, response.text, None, response.headers
                )
            error_data = None
            if "data" in err:
                error_data = err["data"]
            raise ClientError(
                status_code, err["code"], err["msg"], response.headers, error_data
            )
        raise ServerError(status_code, response.text)
