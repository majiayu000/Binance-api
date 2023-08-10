import asyncio
import logging

try:

    from binance_api import BinanceBase
    from spot import SpotOrder, SpotWallet
    from utils.error import ClientError
except ModuleNotFoundError:
    logging.info("ModuleNotFoundError")
    
    import os
    import sys
    current_path = os.path.abspath(os.path.dirname(__file__))
    root_path = os.path.split(current_path)[0]
    if root_path not in sys.path:
        sys.path.append(root_path)
        
    from binance_api import BinanceBase
    from spot import SpotOrder, SpotWallet
    from utils.error import ClientError



# Usage
class TestApi(BinanceBase, SpotWallet, SpotOrder):
    ...


async def main():
    # Todo: read api from config
    api_key = ""
    api_secret = ""

    async with TestApi(api_key, api_secret) as binance:
        
        # wallet
        result = await binance.asset_detail()
        logging.info(result)
    
        # trade
        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 0.002,
            "price": 49500,
        }
        
        try:
            response = await binance.new_order_test(**params)
            logging.info(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )


if __name__ == "__main__":
    asyncio.run(main())
