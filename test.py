import jwt

print(jwt.encode( {
    'login':'admin',
    'password':'admin'
}, 'secret_key'))