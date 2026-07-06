import keyring

# Sometimes, you need to use set_password instead of the UI on Windows if the password is too long, e.g. api key
# keyring.set_password("system", "username", "password")
# keyring.get_password("system", "username")

print(keyring.get_password("https://app.infisical.com", "secret01"))