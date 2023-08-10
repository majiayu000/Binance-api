from utils.error import ParameterArgumentError
from utils.util import (
    check_required_parameter,
    check_required_parameters,
    check_enum_parameter,
)

class SpotMarket:
    async def ping(self):
        """Test Connectivity
        Test connectivity to the Rest API.

        GET /api/v3/ping

        https://binance-docs.github.io/apidocs/spot/en/#test-connectivity

        """

        url_path = "/api/v3/ping"
        return await self.query(url_path)


    async def time(self):
        """Check Server Time
        Test connectivity to the Rest API and get the current server time.

        GET /api/v3/time

        https://binance-docs.github.io/apidocs/spot/en/#check-server-time

        """

        url_path = "/api/v3/time"
        return await self.query(url_path)


    async def exchange_info(
        self, symbol: str = None, symbols: list = None, permissions: list = None
    ):
        """Exchange Information
        Current exchange trading rules and symbol information

        GET /api/v3/exchangeinfo

        https://binance-docs.github.io/apidocs/spot/en/#exchange-information

        Args:
            symbol (str, optional): the trading pair
            symbols (list, optional): list of trading pairs
            permissions (list, optional): display all symbols with the permissions matching the parameter provided (eg.SPOT, MARGIN, LEVERAGED)
        """

        url_path = "/api/v3/exchangeInfo"
        if symbol and symbols:
            raise ParameterArgumentError("symbol and symbols cannot be sent together.")
        if symbol and permissions or symbols and permissions:
            raise ParameterArgumentError(
                "permissions cannot be sent together with symbol or symbols"
            )
        check_type_parameter(symbols, "symbols", list)
        check_type_parameter(permissions, "permissions", list)

        params = {
            "symbol": symbol,
            "symbols": convert_list_to_json_array(symbols),
            "permissions": convert_list_to_json_array(permissions),
        }
        return await self.query(url_path, params)


    async def depth(self, symbol: str, **kwargs):
        """Get orderbook.

        GET /api/v3/depth

        https://binance-docs.github.io/apidocs/spot/en/#order-book

        Args:
            symbol (str): the trading pair
        Keyword Args:
            limit (int, optional): limit the results. async default 100; max 5000. If limit > 5000, then the response will truncate to 5000.
        """

        check_required_parameter(symbol, "symbol")
        params = {"symbol": symbol, **kwargs}
        return await self.query("/api/v3/depth", params)


    async def trades(self, symbol: str, **kwargs):
        """Recent Trades List
        Get recent trades (up to last 500).

        GET /api/v3/trades

        https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list

        Args:
            symbol (str): the trading pair
        Keyword Args:
            limit (int, optional): limit the results. async default 500; max 1000.
        """
        check_required_parameter(symbol, "symbol")
        params = {"symbol": symbol, **kwargs}
        return await self.query("/api/v3/trades", params)


    async def historical_trades(self, symbol: str, **kwargs):
        """Old Trade Lookup
        Get older market trades.

        GET /api/v3/historicalTrades

        https://binance-docs.github.io/apidocs/spot/en/#old-trade-lookup

        Args:
            symbol (str): the trading pair
        Keyword Args:
            limit (int, optional): limit the results. async default 500; max 1000.
            formId (int, optional): trade id to fetch from. async default gets most recent trades.
        """
        check_required_parameter(symbol, "symbol")
        params = {"symbol": symbol, **kwargs}
        return await self.limit_request("GET", "/api/v3/historicalTrades", params)


    async def agg_trades(self, symbol: str, **kwargs):
        """Compressed/Aggregate Trades List

        GET /api/v3/aggTrades

        https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list

        Args:
            symbol (str): the trading pair
        Keyword Args:
            limit (int, optional): limit the results. async default 500; max 1000.
            formId (int, optional): id to get aggregate trades from INCLUSIVE.
            startTime (int, optional): Timestamp in ms to get aggregate trades from INCLUSIVE.
            endTime (int, optional): Timestamp in ms to get aggregate trades until INCLUSIVE.
        """

        check_required_parameter(symbol, "symbol")
        params = {"symbol": symbol, **kwargs}
        return await self.query("/api/v3/aggTrades", params)


    async def klines(self, symbol: str, interval: str, **kwargs):
        """Kline/Candlestick Data

        GET /api/v3/klines

        https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

        Args:
            symbol (str): the trading pair
            interval (str): the interval of kline, e.g 1s, 1m, 5m, 1h, 1d, etc.
        Keyword Args:
            limit (int, optional): limit the results. async default 500; max 1000.
            startTime (int, optional): Timestamp in ms to get aggregate trades from INCLUSIVE.
            endTime (int, optional): Timestamp in ms to get aggregate trades until INCLUSIVE.
        """
        check_required_parameters([[symbol, "symbol"], [interval, "interval"]])

        params = {"symbol": symbol, "interval": interval, **kwargs}
        return await self.query("/api/v3/klines", params)


    async def ui_klines(self, symbol: str, interval: str, **kwargs):
        """Kline/Candlestick Data

        GET /api/v3/uiKlines

        https://binance-docs.github.io/apidocs/spot/en/#uiklines

        Args:
            symbol (str): the trading pair
            interval (str): the interval of kline, e.g 1s, 1m, 5m, 1h, 1d, etc.
        Keyword Args:
            limit (int, optional): limit the results. async default 500; max 1000.
            startTime (int, optional): Timestamp in ms to get aggregate trades from INCLUSIVE.
            endTime (int, optional): Timestamp in ms to get aggregate trades until INCLUSIVE.
        """
        check_required_parameters([[symbol, "symbol"], [interval, "interval"]])

        params = {"symbol": symbol, "interval": interval, **kwargs}
        return await self.query("/api/v3/uiKlines", params)


    async def avg_price(self, symbol: str):
        """Current Average Price

        GET /api/v3/avgPrice

        https://binance-docs.github.io/apidocs/spot/en/#current-average-price

        Args:
            symbol (str): the trading pair
        """

        check_required_parameter(symbol, "symbol")
        params = {
            "symbol": symbol,
        }
        return await self.query("/api/v3/avgPrice", params)


    async def ticker_24hr(self, symbol: str = None, symbols: list = None, **kwargs):
        """24hr Ticker Price Change Statistics

        GET /api/v3/ticker/24hr

        https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics

        Args:
            symbol (str, optional): the trading pair
            symbols (list, optional): list of trading pairs
        """

        if symbol and symbols:
            raise ParameterArgumentError("symbol and symbols cannot be sent together.")
        check_type_parameter(symbols, "symbols", list)
        params = {
            "symbol": symbol,
            "symbols": convert_list_to_json_array(symbols),
            **kwargs,
        }
        return await self.query("/api/v3/ticker/24hr", params)


    async def ticker_price(self, symbol: str = None, symbols: list = None):
        """Symbol Price Ticker

        GET /api/v3/ticker/price

        https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker

        Args:
            symbol (str, optional): the trading pair
            symbols (list, optional): list of trading pairs
        """

        if symbol and symbols:
            raise ParameterArgumentError("symbol and symbols cannot be sent together.")
        check_type_parameter(symbols, "symbols", list)
        params = {"symbol": symbol, "symbols": convert_list_to_json_array(symbols)}
        return await self.query("/api/v3/ticker/price", params)


    async def book_ticker(self, symbol: str = None, symbols: list = None):
        """Symbol Order Book Ticker

        GET /api/v3/ticker/bookTicker

        https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker

        Args:
            symbol (str, optional): the trading pair
            symbols (list, optional): list of trading pairs
        """

        if symbol and symbols:
            raise ParameterArgumentError("symbol and symbols cannot be sent together.")
        check_type_parameter(symbols, "symbols", list)
        params = {"symbol": symbol, "symbols": convert_list_to_json_array(symbols)}
        return await self.query("/api/v3/ticker/bookTicker", params)


    async def rolling_window_ticker(self, symbol: str = None, symbols: list = None, **kwargs):
        """Rolling window price change statistics

        The window used to compute statistics is typically slightly wider than requested windowSize.

        openTime for /api/v3/ticker always starts on a minute, while the closeTime is the current time of the request. As such, the effective window might be up to 1 minute wider than requested.

        E.g. If the closeTime is 1641287867099 (January 04, 2022 09:17:47:099 UTC) , and the windowSize is 1d. the openTime will be: 1641201420000 (January 3, 2022, 09:17:00 UTC)

        Weight(IP): 2 for each requested symbol regardless of windowSize.

        The weight for this request will cap at 100 once the number of symbols in the request is more than 50.

        GET /api/v3/ticker

        https://binance-docs.github.io/apidocs/spot/en/#rolling-window-price-change-statistics

        Args:
            symbol (str, optional): the trading pair
            symbols (str, optional): : list of trading pairs. The maximum number of symbols allowed in a request is 100.
        Keyword Args:
            windowSize (str, optional): async defaults to 1d if no parameter provided.
        """

        if symbol and symbols:
            raise ParameterArgumentError("symbol and symbols cannot be sent together.")
        check_type_parameter(symbols, "symbols", list)
        params = {
            "symbol": symbol,
            "symbols": convert_list_to_json_array(symbols),
            **kwargs,
        }
        url_path = "/api/v3/ticker"
        return await self.query(url_path, params)
