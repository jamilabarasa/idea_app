from models import db, Member, Team

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