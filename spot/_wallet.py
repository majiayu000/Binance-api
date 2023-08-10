from utils.util import (
    check_required_parameter,
    check_required_parameters,
    check_enum_parameter,
)



class SpotWallet:
    async def system_status(self):
        """System Status (System)
        Fetch system status.

        GET /sapi/v1/system/status

        https://binance-docs.github.io/apidocs/spot/en/#system-status-sapi-system
        """

        return await self.query("/sapi/v1/system/status")

    async def coin_info(self, **kwargs):
        """All Coins' Information (USER_DATA)
        Get information of coins (available for deposit and withdraw) for user.

        GET /sapi/v1/capital/config/getall

        https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data

        Keyword Args:
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        return await self.sign_request("GET", "/sapi/v1/capital/config/getall", kwargs)

    async def account_snapshot(self, type: str, **kwargs):
        """Daily Account Snapshot (USER_DATA)

        GET /sapi/v1/accountSnapshot

        https://binance-docs.github.io/apidocs/spot/en/#daily-account-snapshot-user_data

        Parameteres:
        type -- mandatory/string -- "SPOT", "MARGIN", "FUTURES"

        Args:
            type (str): "SPOT", "MARGIN", "FUTURES"
        Keyword Args:
            startTime (int, optional)
            endTime (int, optional)
            limit (int, optional): min 7, max 30, async default 7
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        check_required_parameter(type, "type")
        payload = {"type": type, **kwargs}
        return await self.sign_request("GET", "/sapi/v1/accountSnapshot", payload)

    async def account_status(self, **kwargs):
        """Account Status (USER_DATA)
        Fetch account status detail.

        GET /sapi/v1/account/status

        https://binance-docs.github.io/apidocs/spot/en/#account-status-sapi-user_data

        Keyword Args:
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        return await self.sign_request("GET", "/sapi/v1/account/status", kwargs)

    async def api_trading_status(self, **kwargs):
        """Account API Trading Status (USER_DATA)
        Fetch account api trading status detail.

        GET /sapi/v1/account/apiTradingStatus

        https://binance-docs.github.io/apidocs/spot/en/#account-api-trading-status-sapi-user_data

        Keyword Args:
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        return await self.sign_request(
            "GET", "/sapi/v1/account/apiTradingStatus", kwargs
        )

    async def asset_detail(self, **kwargs):
        """Asset Detail (USER_DATA)
        Fetch details of assets supported on Binance.

        GET /sapi/v1/asset/assetDetail

        https://binance-docs.github.io/apidocs/spot/en/#asset-detail-sapi-user_data

        Keyword Args:
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        return await self.sign_request("GET", "/sapi/v1/asset/assetDetail", kwargs)

    async def trade_fee(self, **kwargs):
        """Trade Fee (USER_DATA)
        Fetch trade fee, values in percentage.

        GET /sapi/v1/asset/traasync defee

        https://binance-docs.github.io/apidocs/spot/en/#trade-fee-sapi-user_data

        Keyword Args:
            symbol (str, optional)
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        return await self.sign_request("GET", "/sapi/v1/asset/traasync defee", kwargs)

    async def funding_wallet(self, **kwargs):
        """Funding Wallet (USER_DATA)

        POST /sapi/v1/asset/get-funding-asset

        https://binance-docs.github.io/apidocs/spot/en/#funding-wallet-user_data

        Keyword Args:
            asset (str, optional)
            needBtcValuation (str, optional): true or false
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        return await self.sign_request(
            "POST", "/sapi/v1/asset/get-funding-asset", kwargs
        )

    async def user_asset(self, **kwargs):
        """User Asset (USER_DATA)

        Get user assets, just for positive data.

        Weight(IP): 5

        POST /sapi/v3/asset/getUserAsset

        https://binance-docs.github.io/apidocs/spot/en/#user-asset-user_data

        Keyword Args:
            asset (str, optional): If asset is blank, then query all positive assets user have.
            needBtcValuation (str, optional)
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        url_path = "/sapi/v3/asset/getUserAsset"
        return await self.sign_request("POST", url_path, {**kwargs})

    async def api_key_permissions(self, **kwargs):
        """Get API Key Permission (USER_DATA)

        GET /sapi/v1/account/apiRestrictions

        https://binance-docs.github.io/apidocs/spot/en/#get-api-key-permission-user_data

        Keyword Args:
            recvWindow (int, optional): The value cannot be greater than 60000
        """

        return await self.sign_request(
            "GET", "/sapi/v1/account/apiRestrictions", kwargs
        )


