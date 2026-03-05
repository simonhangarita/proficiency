"""
ASYNCIO + DECORATORS EXERCISE
==============================

OBJECTIVE: Build an async cryptocurrency price tracker with custom decorators

DATA SOURCE: CoinGecko API (Free, no API key required)
API Documentation: https://www.coingecko.com/en/api/documentation

TASKS:
------
1. Create a decorator @timer that measures execution time of async functions
2. Create a decorator @retry that retries failed async operations up to 3 times
3. Create a decorator @cache that caches results for 60 seconds
4. Fetch cryptocurrency prices asynchronously for multiple coins
5. Calculate portfolio value based on holdings

API ENDPOINTS TO USE:
- Simple Price: https://api.coingecko.com/api/v3/simple/price
  Parameters: ids (comma-separated), vs_currencies (usd)
  Example: https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd

REQUIREMENTS:
- Use aiohttp for async HTTP requests
- Use asyncio for concurrent operations
- Implement all three decorators
- Handle errors gracefully
"""

import asyncio
from nturl2path import url2pathname
import aiohttp
import time
from functools import wraps
from typing import Dict, List, Any, Callable
import json



def timer(func:Callable[...,any])->Callable[...,any]:
    """
    Decorator that measures and prints execution time of async functions.
    Should print: "Function {func_name} took {time:.2f} seconds"
    """
    @wraps(func)
    async def enhancer(*args, **kwargs):
        initial_time = time.time()
        result = await func(*args, **kwargs)
        final_time = time.time()
        time_difference = final_time - initial_time
        print(f'Function {func.__name__} took {time_difference:.2f} seconds')
        return result
    return enhancer



def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator that retries failed async operations.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay in seconds between retries
    
    Should print: "Attempt {attempt}/{max_attempts} failed, retrying..."
    """
    def decorator(func:Callable[...,any])->Callable[...,any]:
        @wraps(func)
        async def enhancer(*args, **kwargs):
            for attempt in range(0,max_attempts):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    if attempt< max_attempts-1:
                        print(f'Attempt {attempt+1}/{max_attempts} failed, retrying...')
                        await asyncio.sleep(delay)
                    else:
                        print(f'Attempt {attempt+1}/{max_attempts} failed, there are no attempts left')
        return enhancer
    return decorator



def cache(time_to_load: int = 60):
    """
    Decorator that caches async function results for a specified time.
    
    Args:
        ttl: Time to live in seconds
    
    Should print: "Cache hit!" or "Cache miss, fetching..."
    """
    cache_dict = {}
    
    def decorator(func:Callable[...,any])->Callable[...,any]:
        @wraps(func)
        async def enhancer(*args, **kwargs):
            id=kwargs.get('crypto_id') or (args[1] if len(args) > 1 else None)
            if id in cache_dict:
                if time.time() - cache_dict[id][1] < time_to_load:
                    print("Cache hit!")
                    return cache_dict[id][0]
                print("Cache expired, fetching...")
                 
            else:
                print("Cache miss, fetching...")
            result = await func(*args, **kwargs)
            if id:
                cache_dict[id] = (result, time.time())
            return result
                
        return enhancer
                
    return decorator


@timer
@retry(max_attempts=3, delay=1.0)
@cache(time_to_load=60)
async def fetch_crypto_price(session: aiohttp.ClientSession, crypto_id: str) -> Dict[str, float]:
    """
    Fetch the current price of a cryptocurrency.
    
    Args:
        session: aiohttp ClientSession
        crypto_id: Cryptocurrency ID (e.g., 'bitcoin', 'ethereum')
    
    Returns:
        Dict with crypto_id and price in USD
    
    Example return: {'bitcoin': 45000.50}
    """
    url2pathname = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    try:
        async with session:
            async with session.get(url2pathname) as response:
                data = await response.json()
                price = data.get(crypto_id, {}).get('usd')
                 #we make sure that the price was fetched correctly because the free version of the api doesn't accept a big 
                #number of calls. Then we have to convert the none  values into a number by default 0 
                return {crypto_id: price if price else 0}
    except Exception as e:
        print(f'Error fetching price for {crypto_id}: {e}')
       



@timer
async def fetch_multiple_prices(crypto_ids: List[str]) -> Dict[str, float]:
    """
    Fetch prices for multiple cryptocurrencies concurrently.
    
    Args:
        crypto_ids: List of cryptocurrency IDs
    
    Returns:
        Dict mapping crypto_id to price
    
    Example: {'bitcoin': 45000.50, 'ethereum': 3000.25}
    """
    #we will use the fetch_crypto_price function to fetch prices concurrently for multiple crypto_id
    prices= await asyncio.gather(*[ fetch_crypto_price(aiohttp.ClientSession(), id) for id in crypto_ids])
   
    
    return {crypto_id: price[crypto_id] for price in prices for crypto_id in price}




@timer
async def calculate_portfolio_value(holdings: Dict[str, float]) -> float:
    """
    Calculate total portfolio value based on current prices.
    
    Args:
        holdings: Dict mapping crypto_id to amount held
        Example: {'bitcoin': 0.5, 'ethereum': 2.0, 'cardano': 1000}
    
    Returns:
        Total portfolio value in USD
    """
    #we can use the fetch multiple prices to get the dictionary with the current prices of the crypto_ids 
    #and the multiply with the holding to get the portafolio value
    list_of_holdings=list(holdings.keys())
    prices= await fetch_multiple_prices(crypto_ids=list_of_holdings)
    #we define a counter for the total value
    total_value=0
    for crypto_id in list_of_holdings:
        #we verify that the value of the price and the holdings is different than none and therefore numeric, before we make the multiplication
        if prices[crypto_id] and holdings[crypto_id]:
            total_value+= holdings[crypto_id]*prices[crypto_id]
    return total_value






async def main():
    """Main function to test your implementations."""
    
    print("=" * 60)
    print("CRYPTOCURRENCY PORTFOLIO TRACKER")
    print("=" * 60)
    
    # Test 1: Fetch single price
    print("\n--- Test 1: Fetch Bitcoin Price ---")
    async with aiohttp.ClientSession() as session:
        btc_price = await fetch_crypto_price(session, "bitcoin")
        print(f"Bitcoin price: ${btc_price.get('bitcoin', 0):,.2f}")
    
    # Test 2: Fetch multiple prices
    print("\n--- Test 2: Fetch Multiple Prices ---")
    crypto_ids = ["bitcoin", "ethereum", "cardano", "solana", "polkadot"]
    prices = await fetch_multiple_prices(crypto_ids)
    for crypto_id, price in prices.items():
        print(f"{crypto_id.capitalize()}: ${price:,.2f}")
    
    # Test 3: Calculate portfolio value
    print("\n--- Test 3: Calculate Portfolio Value ---")
    my_portfolio = {
        "bitcoin": 0.5,
        "ethereum": 2.0,
        "cardano": 1000,
        "solana": 10
    }
    print("My holdings:")
    for crypto, amount in my_portfolio.items():
        print(f"  {crypto.capitalize()}: {amount}")
    
    total_value = await calculate_portfolio_value(my_portfolio)
    print(f"\nTotal Portfolio Value: ${total_value:,.2f}")
    
    # Test 4: Test caching
    print("\n--- Test 4: Test Caching ---")
    print("Fetching Bitcoin price (should be cached from earlier):")
    async with aiohttp.ClientSession() as session:
        await fetch_crypto_price(session, "bitcoin")
    
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
