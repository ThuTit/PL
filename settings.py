import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')
JIRA_URL = os.getenv('JIRA_URL')

PL_URL_DEV = os.getenv('PL_URL_DEV')
PL_URL_TEST = os.getenv('PL_URL_TEST')
PL_URL_UAT = os.getenv('PL_URL_UAT')

PPM_URL = os.getenv('PPM_URL')

PPM_DB_NAME = os.getenv('PPM_DB_NAME')
PPM_DB_USERNAME = os.getenv('PPM_DB_USERNAME')
PPM_DB_PASSWORD = os.getenv('PPM_DB_PASSWORD')
PPM_DB_HOST = os.getenv('PPM_DB_HOST')
PPM_DB_PORT = os.getenv('PPM_DB_PORT')
