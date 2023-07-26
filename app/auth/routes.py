from flask import render_template,url_for,request,redirect,flash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, ResetEmailForm,EditProfileForm
from app.models import User, Address
from app.auth.email import send_password_reset_email
from flask_bootstrap import Bootstrap


@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.useremail.data).first()
        if user is None  or not  user.verify_password(form.password.data) :
            flash('Invalid User Email or Password')
            return redirect(url_for('auth.login'))
        login_user(user,remember=form.rememberme.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=('Sign In'), form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
       return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.useremail.data).first()
        if user:
            flash('user email used')
            return redirect(url_for('auth.login'))
        user = User(email=form.useremail.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        address = Address(email=form.useremail.data,firstname=form.firstname.data, lastname=form.lastname.data,
                          address1=form.address1.data,address2=form.address2.data, city=form.city.data, state=form.state.data,
                          zipcode=form.zipcode.data, user_id=user.id)
        db.session.add(address)
        db.session.commit()
        flash('You have registered')
    return render_template('auth/register.html', title=('Register'),
                           form=form)

@auth.route('/reset_password_request', methods=['GET', 'POST'])
@login_required
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.useremail.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            'Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

@auth.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    useremail=current_user.email
    address=Address.query.filter_by(email=useremail,user_id=current_user.id).first_or_404()
    return render_template('auth/profile.html',address=address)

@auth.route('/editprofile',methods=['GET','POST'])
@login_required
def edit_profile():
      #  if current_user.is_authenticated:
        address=Address.query.filter_by(email=current_user.email , user_id=current_user.id).first_or_404()
        form = EditProfileForm()
        if form.validate_on_submit():
            address.email=current_user.email
            address.user_id=current_user.id
            address.firstname=form.firstname.data
            address.lastname=form.lastname.data
            address.address1=form.address1.data
            address.address2=form.address2.data
            address.city=form.city.data
            address.state=form.state.data
            address.zipcode=form.zipcode.data
            db.session.add(address)
            db.session.commit()
            flash('You have updated profile')
            return redirect(url_for('auth.profile'))
        form.email.data=address.email
        form.firstname.data=address.firstname
        form.lastname.data=address.lastname
        form.address1.data=address.address1
        form.address2.data=address.address2
        form.city.data=address.city
        form.state.data=address.state
        form.zipcode.data=address.zipcode
        return render_template('auth/editprofile.html', form=form)




@auth.route('/reset_email',methods=['GET','POST'])
@login_required
def reset_email():
    #if current_user.is_authenticated:
    form = ResetEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.oldEmail.data).first()
        if user is not None:
          user.email=form.newEmail.data
          db.session.add(user)
          db.session.commit()
          flash('your email address has been updated')
          return redirect(url_for('auth.login'))
    elif request.method=='GET':
      return render_template('auth/reset_email.html', form=form)
    return "wrong"

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
