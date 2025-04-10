import requests
import json
from flask import Flask, redirect, request

app = Flask(__name__)
with open('sensitive.json') as s:
   admin = json.load(s)
  
#actual details in seperate json file
admin_user = admin.get('reddituser')
admin_pass = admin.get('redditpass')
ID = admin.get('ID')
secret = admin.get('secret')





@app.route('/login')
#logs into my reddit account
def login():
    client_id = ID
    redirect_uri = 'https://replit.com/@scrumble/fish-fundamentals'
    scopes = ['identity', 'read'] 

    authorisation_url = f'https://www.reddit.com/api/v1/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&duration=temporary&scope={"+".join(scopes)}' 

    return redirect(authorisation_url)

@app.route('/callback')
#asks for an auth code
def callback():
    code = request.args.get('code') # asking for ann authorisation code
    access_token, refresh_token = code_for_token(code) #calls func code_for_token to exchange the code for a token
    return ('Authorisation code received: ', code) #returns code


def code_for_token(code):
    client_id = ID
    client_secret = secret
    redirect_uri = 'https://replit.com/@scrumble/fish-fundamentals'
    token_url = 'https://www.reddit.com/api/v1/access_token'
    data = {
        'grant_type': 'authorisation_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    auth = (client_id, client_secret) #checking my creds
    response = requests.post(token_url, data=data, auth=auth)
    token_data = response.json()
    access_token = token_data['access_token'] 
    refresh_token = token_data['refresh_token']
    return access_token, refresh_token

if __name__ == "__main__": #follows app route
  app.run(debug=True)