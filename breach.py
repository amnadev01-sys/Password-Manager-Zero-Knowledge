import hashlib
import requests

def check_breach(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)

    for line in res.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return True

    return False