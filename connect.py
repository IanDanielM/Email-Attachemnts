import dropbox
import requests
from dropbox.exceptions import AuthError
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
def dropbox_connect():
    try:
        endpoint=os.getenv("endpoint")
        query_params = {"grant_type":"refresh_token",
        "client_id":os.getenv("client_id"),
        "client_secret":os.getenv("client_secret"),
        "refresh_token":os.getenv("refresh_token")
        }
        response = requests.post(endpoint,params=query_params)
        r=response.json()
        dbx = dropbox.Dropbox(r['access_token'])
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx
