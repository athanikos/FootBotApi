from keyring import set_password, get_password

set_password('FootBotApi', 'foot', 'test')
print(get_password('FootBotApi', 'foot'))