from Configuration import db
from datetime import datetime




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firname = db.Column(db.String(), nullable=False)
    secname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    psw = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    passdata = db.Column(db.String(), nullable=True)


    def __repr__(self):
        return 'id:{}, firname:{}, secname:{}, email:{}, psw:{},country:{},city:{},passdata:{}'.format(self.id, self.firname, self.secname, self.email,
                                                                     self.psw,self.country ,self.city,self.passdata)

class Manager(db.Model):
    __tablename__ =  'Manager_Table'
    id = db.Column(db.Integer, primary_key=True)
    firname = db.Column(db.String(), nullable=False)
    secname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    psw = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    extrapass = db.Column(db.String(),nullable=False)


    def __repr__(self):
        return 'id:{}, firname:{}, secname:{}, email:{}, psw:{},country:{},city:{},extrapass{}'.format(self.id, self.firname,
                                                                                                 self.secname,
                                                                                                 self.email,
                                                                                                 self.psw, self.country,self.city,self.extrapass)

class GuestBooking(db.Model):
    __tablename__ = 'Booking_Table'
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(), nullable=False)
    bookingfrom = db.Column(db.DateTime, nullable=False, default=datetime.today)
    bookingto = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return 'id:{}, room:{}, bookingfrom:{}, bookingto:{}'.format( self.id, self.room,
                    self.bookingfrom,
                    self.bookingto)

