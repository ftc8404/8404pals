import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask import session, url_for, request
import secrets


def setup_session():
    if(not session.get('state')):
        session['state'] = secrets.token_urlsafe(32)


def check_if_auth():
    if(session.get('authenticated')):
        if(session['authenticated'] == True):
            return True
    return False


def get_login_url(from_url):
    url = url_for('login_oauth')
    url += "?from="+from_url
    return url


def get_auth_url():
    setup_session()
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'google_oauth_client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'])

    flow.redirect_uri = url_for(
        'oauth_callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true', state=session['state'])
    return authorization_url


def getToken(auth_code):
    setup_session()
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'google_oauth_client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'],
        state=session['state'])
    flow.redirect_uri = url_for('oauth_callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}
