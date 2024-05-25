# -*- coding: utf-8 -*-
import os
from ecdsa import SigningKey, SECP256k1
import sha3
import re
import random
import string
import requests
import time

def randuseragent():
    req = requests.get("https://techpatterns.com/downloads/firefox/useragentswitcher.xml")
    if req.status_code == 200:
        regex = re.findall(r'" useragent="(.*?)"', req.content.decode('utf-8'))
        if regex:
            random_user_agent = random.choice(regex)
            return random_user_agent
        else:
            print("No user agents found. Continuing with default user agent.")
    else:
        print("Failed to retrieve user agents.")
    return ""

def keccak256(data):
    k = sha3.keccak_256()
    k.update(data)
    return k.digest()

def create_eth_address():
    priv_key = SigningKey.generate(curve=SECP256k1)
    priv_key_der = priv_key.to_string()
    pub_key = priv_key.get_verifying_key().to_string()
    pub_key_hash = keccak256(pub_key)
    eth_address = pub_key_hash[-20:].encode('hex')
    return priv_key_der.encode('hex'), eth_address

def RandomGenerator(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def genmail():
    RandomStringForPREFIX = RandomGenerator(8)
    domains = ["1secmail.com", "1secmail.org", "1secmail.net", "icznn.com", "ezztt.com", "vjuum.com", "laafd.com", "txcct.com"]
    domain = random.choice(domains)
    return "{}@{}".format(RandomStringForPREFIX, domain)

def verify_email(usern, domain):
    try:
        pesan = requests.get("https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}".format(usern, domain)).json()[0]
        baca_pesan = requests.get("https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}".format(usern, domain, pesan['id'])).json()["body"]
        regex_url = re.findall('href="(.*?)"', baca_pesan)[0]
        return regex_url
        time.sleep(5)
    except IndexError:
        print("No messages found for {}@{}".format(usern, domain))
        return ""
    except Exception as e:
        print("An error occurred while verifying email: {}")
        return ""

def main(coderef, i):
    private_key, eth_address = create_eth_address()
    prv8 = "0x" + eth_address
    print("\n================Reff : {} =>> {} ================".format(coderef, i))
    EMAIL = genmail()
    usern = EMAIL.split("@")[0]
    domain = EMAIL.split("@")[1]
    print("• Ethereum Address: " + prv8)
    print("• Register Process Please wait ..... ")
    ua = randuseragent()
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Cookie": "_ga=GA1.1.613432755.1716565438; _ga_6MLGV253VV=GS1.1.1716565437.1.1.1716565559.0.0.0",
    }
    try:
        sex = requests.Session()
        data = {
            "email": EMAIL,
            "referal": coderef,
            "walletAddress": "0x" + eth_address,
            "submit": "Register Now",
        }
        req = sex.post("https://nftnova.net/airdrop/", data=data, headers=headers).content
        if "title: 'Success'" in req:
            regex = re.findall("referralCode = '(.*?)';", req)
            print("• Success => Reff Code : " + regex[0])
            print("• Get Token .... ")
            time.sleep(5)
        regex_url = verify_email(usern, domain)
        print("• Verify  Account .... ")
        print(regex_url)
        time.sleep(5)
        proses_verif = sex.get(regex_url,headers=headers)
        if "text: 'Email verified'" in proses_verif.content or "title: 'Success'" in proses_verif.content:
        	time.sleep(5)
        	print("• Done bro .....")
    except Exception as e:
        print("- ERROR: " + str(e))

if __name__ == "__main__":
    print("\nNftNova | Shin Code")
    coderef = raw_input("[-] Input Referral Code : ")
    loop = raw_input("[-] How Many Referrals Do You Want? : ")
    for i in range(int(loop)):
        try:
            main(coderef, i)
            time.sleep(5)
        except Exception as e:
            print("An error occurred in the main loop: {}".format(e))
