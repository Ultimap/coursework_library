from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os

load_dotenv()

upload_img = './img/'
DATABASE_URL = os.environ['DATABASE_URL']
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
oauth2scheme = OAuth2PasswordBearer('/api/user/login')
