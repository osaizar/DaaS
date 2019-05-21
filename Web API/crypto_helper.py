import crypt
import random
import string

def generate_salt(size=8, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_password_hash(passwd):
    salt = '$6$'+generate_salt()
    hashed = crypt.crypt(passwd,salt)
    return hashed

def check_password_hash(orig, check):
    salt = orig.split("$")[2]
    print(salt)
    hashed = crypt.crypt(check, "$6$"+salt)
    return bool(hashed == orig)
