import requests
import random

with open("./src/proxies.txt", "r") as file:
    proxies = file.read().splitlines()
print(proxies)

timeout = 10

def get_valid_proxy(timeout=timeout, retries=5):
    random.shuffle(proxies)
    for proxy in proxies:
        retries_left = retries
        while retries_left > 0:
            try:
                response = requests.get('https://www.google.com', proxies={'http': proxy}, timeout=timeout)
                if response.status_code == 200:
                    return proxy
            except (requests.exceptions.Timeout, requests.exceptions.ProxyError):
                pass
            retries_left -= 1
    raise ValueError('No valid proxies found.')