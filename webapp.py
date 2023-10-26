from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
import json

app = Flask(__name__)


fileObject = open("creds.json","r")
jsoncontent = fileObject.read()
creds = json.loads(jsoncontent)


client_id = creds['client_id']
client_secret = creds['client_secret']
authorization_base_url = creds['authorization_base_url']
token_url =  creds['token_url']

@app.route("/")
def demo():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)
  
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    github = OAuth2Session(client_id, token=session['oauth_token'])

    return jsonify(github.get('https://api.github.com/user').json())


if __name__ == "__main__":
    os.environ['OATHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(ssl_context="adhoc")
    
