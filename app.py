import functools
from os import name
from flask import request, render_template, redirect, session, make_response
from flask.helpers import flash
from google import auth
from config import AUTHORIZATION_SCOPE, AUTHORIZATION_URL, AUTH_REDIRECT_URI, AUTH_STATE_KEY, app, CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN_URI, AUTH_TOKEN_KEY, BASE_URI, LANDING_URI
from models import Member, Team
from repository import saveMember, getMemberById, deleteMemberById, saveTeam, getMembers, findMemberByEmail
from domain import MemberDomain
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
from authlib.client import OAuth2Session, oauth2_session

def isLoggedIn():
    return True if AUTH_TOKEN_KEY in session else False

def build_credentials():
    if not isLoggedIn():
        raise Exception('User must be logged in')

    oauth2_tokens = session[AUTH_TOKEN_KEY]
    
    return Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)


def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()



def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)


@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        oauth_session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope = AUTHORIZATION_SCOPE, redirect_uri= AUTH_REDIRECT_URI )

        uri, state = oauth_session.authorization_url(AUTHORIZATION_URL)

        session[AUTH_STATE_KEY] = state

        session.permanent = True

        return redirect(uri,code=302)

@app.route('/auth')
@no_cache
def google_auth_redirect():
    req_state = request.args.get('state', default=None, type=None)

    if req_state != session[AUTH_STATE_KEY]:
        response = make_response('Invalid state parameter', 401)
        return response
    
    oauth2_session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state= session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = oauth2_session.fetch_access_token(
                        ACCESS_TOKEN_URI,            
                        authorization_response=request.url)

    session[AUTH_TOKEN_KEY] = oauth2_tokens

    user = get_user_info()

    member : Member = findMemberByEmail(user["email"])

    if member is None:
        new_member = Member(name=user["name"],email=user["email"],profileImageUrl=user["picture"])
        saveMember(new_member)
        flash("You were successfully registered","info")
    else:
        flash("Welcome back : {}".format(user["name"]),"info")

    return redirect(LANDING_URI, code=302)

@app.route('/logout')
@no_cache
def logout():

    session.pop(AUTH_TOKEN_KEY, None)

    session.pop(AUTH_STATE_KEY, None)

    flash("Logged out","info")

    return redirect(BASE_URI, code=302)

@app.route("/members",methods=["POST","GET"])
def member():
    if request.method == "POST":
        member_data = request.json

        member = Member(name=member_data["name"],email=member_data["email"],profileImageUrl=member_data["profileImageUrl"],gender=member_data["gender"])
        
        saveMember(member)

        return member.serialize,201

    elif request.method == "GET":

        members = getMembers()

        return render_template('members.html', members = members)

@app.route("/members/<int:id>",methods=["GET","DELETE"])
def member_detail(id):
    if request.method == "GET":
        
        member:Member = getMemberById(id)

        if(member):
            return member.serialize
        
        return {"message":"Member with the specified id does not exist"},404

    elif request.method == "DELETE":

        deleteMemberById(id)

        return {"success":"Member was deleted"},202

@app.route("/team",methods=["POST"])
def team():
    # receive the request
    request_data = request.json 

    member_list = []

    for member in request_data["members"]:

        memberDomain = MemberDomain(member["email"], member["role"])

        member_list.append(memberDomain.serialize)

    team = Team(name=request_data["name"],members=member_list)

    saveTeam(team)

    return team.serialize


if(__name__== "__main__"):
    app.run(debug=True)