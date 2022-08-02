from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get("HOST")
database = os.environ.get("DATABASE")
user_name = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_USER_PASS")

print(host)
print(database)
print(user_name)
print(password)

