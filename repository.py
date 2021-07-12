from models import db, Member

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