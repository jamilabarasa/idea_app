
from flask import request, json,redirect, render_template
from flask.wrappers import Request
from config import app
from models import Member, Team, db, Family
from repository import getAllTeams, saveMember, getMemberById, deleteMemberById, getAllTeams,deleteTeamByName,getAllFamily
from domain import MemberDomain
from datetime import datetime
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask.helpers import flash, url_for



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


@app.route("/team/create",methods=["POST","GET"])
def team():
    if request.method == "POST":

        team_data= Team(name = request.form["name"])

        db.session.add(team_data)

        db.session.commit()

        # get all teams
        teams = getAllTeams()

        # saveTeam(team)

        flash(team_data.serialize["name"] + " was successfully created","info") 

        return render_template('teamList.html',teams=teams)
        
        

    elif request.method == "GET":

        return render_template('team.html')

@app.route("/team/list/<name>/delete",methods=["GET","POST"])
def listTeam(name):

    team = Team.query.filter_by(name=name).first()

    if request.method == "GET":

        teams = getAllTeams()

        return render_template('teamList.html',teams=teams)

    elif request.method == "POST":

        db.session.delete(team)

        db.session.commit()

         # get all teams
        teams = getAllTeams()

        flash("team was successfully deleted","danger") 

        return render_template('teamList.html',teams=teams)

@app.route("/team/list/<name>/update",methods=["POST","GET"])
def updateTeam(name):

    team = Team.query.filter_by(name=name).first()

    if request.method == "POST":

        db.session.delete(team)

        db.session.commit()

        team_data= Team(name = request.form["name"])

        db.session.add(team_data)

        db.session.commit()

        teams = getAllTeams()

        flash("team was successfully updated","info") 

        return render_template('teamList.html',teams=teams)    

    elif request.method == "GET":

        return render_template('editTeam.html')
        

        
if(__name__== "__main__"):
    app.run(debug=True)