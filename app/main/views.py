from flask import render_template,request,redirect,url_for,abort,flash
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
    return render_template('all_blogs.html', title = title,blogs=blogs)

@main.route('/update_blog/<int:id>',methods = ['GET','POST'])
@login_required
def update_blog(id):
    blog = Blog.query.get(id)
    if blog.user.id != current_user.id:
        abort(403)

    form = BlogForm()

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.blog = form.blog.data
        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('main.blogs'))

    return render_template('update_blog.html',form =form)


@main.route('/delete_blog/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blog(id):
    blog = Blog.query.get(id)
    if blog.user.id != current_user.id:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
 
    return redirect(url_for('main.blogs'))


@main.route('/view_comments/<id>')
@login_required
def view_comments(id):
    comment = Comment.get_comments(id)
    title = 'View Comments'
    return render_template('comment.html', comment=comment, title=title)

@main.route('/comment/<int:blog_id>', methods=['GET','POST'])
@login_required
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.filter_by(id=blog_id).first()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment, user_id = current_user.id, blog_id=blog_id)
        new_comment.save_comment()
        return redirect(url_for('main.blogs'))
    return render_template('new_comment.html', form=form, blog_id=blog_id)

@main.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment =Comment.query.get(comment_id)
    if comment.user.id != current_user.id:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
   
    return redirect (url_for('main.blogs'))

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
        user_photo = PhotoProfile(pic_path = path,user= user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))