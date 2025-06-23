import bcrypt
print(bcrypt.hashpw(b"user1234", bcrypt.gensalt()).decode())