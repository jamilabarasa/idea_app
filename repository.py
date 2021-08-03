from models import db, Member, Team ,Family

def saveMember(member:Member):
    
    db.session.add(member)
    
    db.session.commit()

def getMemberById(id:int):
    
    member = Member.query.filter_by(id=id).first()

    return member

def deleteMemberById(id:int):

    member:Member = getMemberById(id)

    db.session.delete(member)

    db.session.commit()


def findMemberByEmail(email:str):

    member = Member.query.filter_by(email=email).first()

    return member

def saveTeam(team:Team):

    db.session.add(team)

    db.session.commit()

def getAllTeams():

     teams = Team.query.all()

     return teams

def deleteTeamByName(name:str):

    team = Team.query.filter_by(name=name).first()

    db.session.delete(team)

    db.session.commit()
    
def getAllFamily():

    family = Family.query.all()

    return family

     


