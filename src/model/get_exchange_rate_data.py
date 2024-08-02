#!/usr/bin/env python3

import requests

def fetch_exchange_rates(api_key):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json() 

def get_specific_rates(api_key,first_currency,second_currency):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{first_currency}/{second_currency}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()