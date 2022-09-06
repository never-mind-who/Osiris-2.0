import requests
import os

token = "MzA3OTY3MTk2MzkzNTA0Nzgx.G6queB.rqUVc6pXydykxn9m6Luabkd0nP0SEP9ZAL6kN0"


headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Authorization" : token
        }


r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
t= requests.get('https://ipinfo.io/json')
print(r.json())
print("/n")
print (t.json())
print("/n")
print(os.getenv("Username"))