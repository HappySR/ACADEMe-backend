# Run this file 3 times to get 3 different secret keys and set it in JWT_SECRET_KEY, SECRET_KEY, and REFRESH_SECRET_KEY in the .env file

import secrets

print(secrets.token_urlsafe(32))  # Generates a secure random key
