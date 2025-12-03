# referenced GeekforGeeks.
# https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/

import bcrypt

# example password
password = 'password123'

# converting password to array of bytes
bytes = password.encode('utf-8')

# generating the salt
salt = bcrypt.gensalt()

# Hashing the password
hash = bcrypt.hashpw(bytes, salt)

print(hash)

#-------------------------------------checking password
# example password
password = 'passwordabc'

# converting password to array of bytes
bytes = password.encode('utf-8')

# generating the salt
salt = bcrypt.gensalt()

# Hashing the password
hash = bcrypt.hashpw(bytes, salt)

# Taking user entered password 
userPassword =  'password000'

# encoding user password
userBytes = userPassword.encode('utf-8')

# checking password
result = bcrypt.checkpw(userBytes, hash)

print(result)