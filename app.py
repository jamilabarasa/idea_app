from flask import request, json
from config import app
from models import Member, Team
from repository import saveMember, getMemberById, deleteMemberById, saveTeam
from domain import MemberDomain
from datetime import datetime

@app.route("/members",methods=["POST"])
def member():

    member_data = request.json

    member = Member(name=member_data["name"],email=member_data["email"],profileImageUrl=member_data["profileImageUrl"],gender=member_data["gender"])
    
    saveMember(member)

    return member.serialize,201

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