from minhwa import db

class DHWALIST(db.Model):
    list_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    writer = db.Column(db.String(150), nullable=False)
    img = db.Column(db.String(500), nullable=True)
    publi = db.Column(db.String(150), nullable=True)

class DHWACART(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('dhwalist.list_id'))
    dhwalist = db.relationship('DHWALIST', backref=db.backref('dhwalist_set'))
    username = db.Column(db.String(150), db.ForeignKey('dhwauser.id'), nullable=False)
    dhwauser = db.relationship('DHWAUSER', backref=db.backref('dhwauser_set'))
    subject = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    writer = db.Column(db.String(150), nullable=True)
    publi = db.Column(db.String(150), nullable=True)
    rent_date = db.Column(db.DateTime(), nullable=True)
    return_date = db.Column(db.DateTime(), nullable=True)

class DHWAUSER(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tell = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.Text(), nullable=True)
    postcode = db.Column(db.Integer, nullable=True)