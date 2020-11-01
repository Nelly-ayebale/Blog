from flask import render_template,request,redirect,url_for,abort
from ..models import User,PhotoProfile,Blog,Comment
from . import main
from ..request import get_quotes
from .. import db,photos
from .forms import BlogForm,CommentForm,UpdateProfile
from flask_login import login_required, current_user

@main.route('/')
def index():
    '''
    View root page that returns the index page and its data
    '''
    quote = get_quotes()
    
    title = 'MyBlog.com'

    return render_template('index.html', title=title, quote = quote)

@main.route('/new_blog', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        user_id = current_user
        new_blog = Blog(title=title, blog=blog, user_id=current_user._get_current_object().id)
        new_blog.save_blogs()

        return redirect(url_for('main.blogs'))
    return render_template('new_blog.html', form=form)

@main.route('/blogs', methods=['GET','POST'])
@login_required
def blogs():
    blogs = Blog.query.all()
    title = 'All Blogs'
    return render_template('all_blogs.html', title = title)

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