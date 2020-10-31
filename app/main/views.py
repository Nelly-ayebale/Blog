from flask import render_template,request,redirect,url_for,abort
from ..models import User,PhotoProfile
from . import main
from ..request import get_quotes
from .. import db,photos
from .forms import BlogForm
from flask_login import login_required, current_user

@main.route('/')
def index():
    '''
    View root page that returns the index page and its data
    '''
    quotes = get_quotes()
    
    title = 'MyBlog.com'

    return render_template('index.html', title=title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path, user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))