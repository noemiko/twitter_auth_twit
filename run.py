from flask import Flask
from flask import request
from flask import redirect

from tweepy import OAuthHandler
from tweepy import TweepError
from tweepy import API

app = Flask(__name__)

C_TOKEN = ''
C_SECRET = ''
CALLBACK_URL = 'http://localhost:5000/callback'
auth = OAuthHandler(
    C_TOKEN,
    C_SECRET,
    CALLBACK_URL)

@app.route('/')
def hello_world():
    try:
        redirect_url = auth.get_authorization_url()
        return redirect(redirect_url)
    except TweepError as err:
        return err


@app.route('/callback')
def callback():
    verifier = request.args.get('oauth_verifier')
    try:
        token = auth.get_access_token(verifier)
        key, secret = token
        auth.set_access_token(key, secret)
    except TweepError:
        print('Error! Failed to get access token.')
    else:
        api = API(auth)
        api.update_status(status='tweepy + oauth!2')
        return 'Tweet has been send!'

if __name__ == "__main__":
    app.run(debug=True, port=500)
