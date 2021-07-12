class MemberDomain():

    email = ""
    role = ""

    def __init__(self, email, role):
        self.email = email
        self.role = role

    @property
    def serialize(self):
        return{
            'email':self.email,
            'role':self.role
        }