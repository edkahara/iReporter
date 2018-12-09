import os
from dotenv import load_dotenv, find_dotenv

from flask import current_app
from app import create_app

load_dotenv(find_dotenv)
app = create_app(os.getenv('FLASK_ENV'))

if __name__ == '__main__':
    app.run()
