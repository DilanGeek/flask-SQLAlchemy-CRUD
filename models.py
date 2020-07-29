from app import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(250))
    
    def __str__(self):
        return(
            f'Id: {self.id},'
            f'Name: {self.name},'
            f'Last Name: {self.last_name},'
            f'Email: {self.email}'
        )