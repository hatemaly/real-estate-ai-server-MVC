from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings

config_data = {
    'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID,
    'GOOGLE_CLIENT_SECRET': settings.GOOGLE_CLIENT_SECRET
}

config = Config(environ=config_data)
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:4200/login',
    client_kwargs={'scope': 'openid profile email'},
)

def init_oauth(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)