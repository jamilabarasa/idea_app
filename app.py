from os import name
from flask import request
from config import app
from models import Member
from repository import saveMember

@app.route("/members",methods=["POST"])
def member():

    member_data = request.json

    member = Member(name=member_data["name"],email=member_data["email"],profileImageUrl=member_data["profileImageUrl"],gender=member_data["gender"])
    
    saveMember(member)

    return {"message":"member was successfully registered"}



if(__name__== "__main__"):
    app.run(debug=True)