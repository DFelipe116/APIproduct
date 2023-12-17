from jwt import encode, decode

pwd = "1234567890"

def create_token(data: dict, secret=pwd):
    token = encode(payload=data, key=secret, algorithm="HS256")
    return token

def validate_token(token):
    data = decode(token, pwd, algorithms=["HS256"])
    return data