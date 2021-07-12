from flask import request
from config import app
from models import Member
from repository import saveMember, getMemberById, deleteMemberById

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



if(__name__== "__main__"):
    app.run(debug=True)