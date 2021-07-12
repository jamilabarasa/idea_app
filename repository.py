from models import db, Member

def saveMember(member:Member):
    db.session.add(member)
    db.session.commit()