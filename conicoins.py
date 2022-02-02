
from typing import Dict
import requests
import json



def which_currency() -> str:
    '''
    This function accepts a three letter currency code from the user.
    The code is returned in lowercase letters
    ''' 
    currency = input()
    return currency.lower()


def get_amount() -> float:
    '''
    Gets the amount of the currency the user currently posesses
    '''
    my_amount = float(input())
    return my_amount


def request_rates(my_currency: str, target_currency: str) -> float:
    '''
    This function takes the 3-letter currency code given
    from which_currency() as input and trys to request json
    data from the site below. If successful, returns the data
    as a dictionary, Else, exception for JSON decode error for
    invalid currency code.
    '''
    try:
        r = requests.get(f'http://www.floatrates.com/daily/{my_currency}.json')
        rate = (json.loads(r._content)[f'{target_currency}'])['rate']
        return rate
    except json.decoder.JSONDecodeError:
        print("Could not process request. Check your currency code and try again. JSONdecode error")




def get_total(amount: float, wanted_rate: float) -> float:
    '''
    Accepts amount of currency user is holding, and the rate they want to buy
    as inputs. Returns the total they could buy in the new currency
    '''
    total_value = amount * wanted_rate
    return total_value 
    

def make_cache(my_currency: str) -> Dict[str, float]:
    '''
    Creates a dict to store currencies while the program runs.
    Initialized with rates for Euro and USD against the starting currency
    '''
    if my_currency == 'usd':
        FLOATRATES_EUR = request_rates(my_currency, 'eur')
        cache = {'eur': FLOATRATES_EUR}
        return cache
    if my_currency == 'eur':
        FLOATRATES_USD = request_rates(my_currency, 'usd')
        cache = {'usd': FLOATRATES_USD}
        return cache
    FLOATRATES_USD = request_rates(my_currency, 'usd')
    FLOATRATES_EUR = request_rates(my_currency, 'eur')
    cache = {'usd': FLOATRATES_USD, 'eur': FLOATRATES_EUR}
    
    return cache


def in_cache(amount: float, cache: Dict[str, float], currency: str) -> None:
    '''
    Takes the amount the user holds, a currency cache, and the desired currency as inputs.
    The function then checks the cash against the currency in question and prints the total 
    received in the currency
    '''
    print("Oh! It is in the cache!")
    total = get_total(amount, cache[f'{currency}'])
    print(f"You recieved {total} {currency.upper()}")


def not_in_cache(original_currency: str, new_currency: str, amount: float) -> float:
    '''
    Takes a base currency, a new currency to buy, the amount in the original as input. 
    The function returns the rate of the new currency
    '''
    print("Sorry, but it is not in the cache!")
    new_rate = request_rates(original_currency, new_currency)
    new_total = get_total(amount, new_rate)
    print(f"You recieved {new_total} {new_currency.upper()}")
    
    return new_rate


def update_cache(cache: Dict[str, float], new_currency: str, new_rate: float) -> Dict[str, float]:
    '''
    Accepts the cache (Dict[str, float]) the new currency and rates to be added as input, 
    and adds them to the cache, returns the updated cache.
    '''
    cache[new_currency] = new_rate
    return cache


def main():
    my_currency = which_currency()
    rate_cache = make_cache(my_currency)
    
    while True:
        wanted_currency = which_currency()
        if wanted_currency == "":
            break
        my_amount = get_amount()
        print("Checking the cache...")
        
        if wanted_currency in rate_cache:
            in_cache(my_amount, rate_cache, wanted_currency)
        
        else:
            new_rate = not_in_cache(my_currency, wanted_currency, my_amount)
            rate_cache[wanted_currency] = new_rate
            
            


if __name__ == '__main__':
    main()



