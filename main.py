import jwt, os
from flask import render_template, redirect, session ,request
from flask_bcrypt import Bcrypt
from Form import Registration, SignIn, Booking, ManRegistration, InfoUpdate, ManSign, PasswordRec , NewPasswordRec
from Database import User , Manager ,GuestBooking
from Configuration import app, db, mess
from flask_mail import  Message





bcrypt = Bcrypt(app)


@app.before_first_request
def create_all():
    db.create_all()

@app.route('/')
def index():
    return render_template('MainPage.html')

@app.route('/main')
def index2():
        return render_template('ManMainPage.html')

@app.route('/rooms')
def room():
    return render_template('Room.html')

@app.route('/restaurant')
def restaurant():
    return render_template('Restaurant.html')

@app.route('/gardenpool')
def garpool():
   return render_template('GardenandPool.html')

@app.route('/checkout')
def check():
    return render_template('CheckOut.html')



#################   ROOM BOOKING OPTION    ##########################

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'id' in session:
        form = Booking()
        if form.validate_on_submit():
            guestb = GuestBooking(room=form.room.data,bookingfrom=form.bookingfrom.data,bookingto=form.bookingto.data)
            db.session.add(guestb)
            db.session.commit()
            return redirect('/rooms')
        return render_template('Booking.html', form=form)
    else:
        return redirect('/signIn')

@app.route('/manregistration', methods=['GET', 'POST'])
def manregistration():
    form = ManRegistration()
    if form.validate_on_submit():
        hashpsw = bcrypt.generate_password_hash(form.psw.data).decode('utf-8')
        manager_registration = Manager(firname=form.firname.data, secname=form.secname.data,
                             email=form.email.data, psw=hashpsw, country=form.country.data,city=form.city.data , extrapass = form.extrapass.data)
        db.session.add(manager_registration)
        db.session.commit()
        return redirect('/main')
    return render_template('ManRegistration.html', form=form)

def passportsave(file_from_form):
    file_name, file_extension = os.path.splitext(file_from_form.filename)
    file = file_name + file_extension
    file_path = os.path.join(app.root_path, 'static/passportdata', file)
    file_from_form.save(file_path)
    return file

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        if form.passdata.data:
            file = passportsave(form.passdata.data)
            user_reg = User(firname=form.firname.data, secname=form.secname.data,
                             email=form.email.data, psw=form.psw.data, country=form.country.data,city=form.city.data ,
                            passdata=file)
            recmes = Message(subject='Обратная Сообщение для Гостья',
            body='Вы успешно зарегистривовались. Перейти обратно на сайт: http://127.0.0.1:5000/ ',
            recipients=[form.email.data])
            mess.send(recmes)
            db.session.add(user_reg)
            db.session.commit()
            return redirect('/')
    return render_template('Registration.html', form=form)

@app.route('/signIn', methods=['GET', 'POST'])
def sign():
    form = SignIn()
    if form.validate_on_submit():
        user_signin = User.query.filter_by(email=form.email.data).first()
        if user_signin.psw == form.psw.data:
            session['id'] = user_signin.id
            return redirect('/')
    return render_template('SignIn.html', form=form)

@app.route('/signInman', methods=['GET', 'POST'])
def signman():
    form = ManSign()
    if form.validate_on_submit():
        man_signin = Manager.query.filter_by(email=form.email.data , extrapass=form.extrapass.data).first()
        if man_signin.psw == form.psw.data:
            session['id'] = man_signin.id
            return redirect('/main')
    return render_template('ManSign.html', form=form)

@app.route('/infoupdate', methods=['GET', 'POST'])
def UPDATE():
        infoupdate = User.query.filter_by(id=session.get('id')).first()
        form = InfoUpdate()
        if form.validate_on_submit():
            infoupdate.firname = form.firname.data
            infoupdate.secname = form.secname.data
            infoupdate.email = form.email.data
            infoupdate.country = form.country.data
            infoupdate.city = form.city.data
            db.session.commit()
            return redirect('/guest_table')
        elif request.method == 'GET':
            form.firname.data =  infoupdate.firname
            form.secname.data =  infoupdate.secname
            form.email.data =  infoupdate.email
            form.country.data =  infoupdate.country
            form.city.data =  infoupdate.city
        return render_template('InfoUpdate.html', form=form)


#####   PASSWORD RECOVER OPTIONS / TOKENS FOR USER PASSWORD RECOVER #######################

def gettingrespswtoken(user):
    token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def validrespswtoken(token):
    user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
    user = User.query.filter_by(id=user_id.get('id')).first()
    return user

def pasrec_email(user):
    token = gettingrespswtoken(user)
    mesg = Message(subject='Востоновление Пароля', recipients=[user.email])
    mesg.html = render_template('MessEmail_PassRec.html', user=user, token=token)
    mess.send(mesg)





########################   PASSWORD RECOVER OPTIONS #######################

@app.route('/passwordrec', methods=['GET', 'POST'])
def pasrec():
    if 'id' in session:
        return redirect('/')
    form = PasswordRec()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            pasrec_email(user)
        return redirect('/checkout')
    return render_template('PasswordRec.html', form=form)

@app.route('/newpasw/<token>', methods=['GET', 'POST'])
def newpasw(token):
    if 'id' in session:
        return redirect('/')
    user = validrespswtoken(token)
    if user:
        form = NewPasswordRec()
        if form.validate_on_submit():
            user_email_rec = User.query.filter_by(email=form.email.data).first()
            if  user_email_rec:
                user_email_rec.psw = form.psw.data
                db.session.commit()
                return redirect('/')
    return render_template('NewPassword.html', form=form)




@app.route('/guest_table')
def data():

        manager = User.query.all()
        return render_template('Guests_Table.html', guests=manager)



@app.route('/logout')
def logOut2():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

