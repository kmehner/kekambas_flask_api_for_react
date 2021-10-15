from . import bp as blog
from app import db
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from .forms import PostForm
from .models import Post


@blog.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        print('Hello')
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash(f'The post {title} has been created.', 'primary')
        return redirect(url_for('index'))
        
    return render_template('createpost.html', form=form)




@blog.route('/my-posts')
@login_required
def my_posts():
    posts = current_user.posts
    return render_template('my_posts.html', posts=posts)


@blog.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


@blog.route('/posts/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash('That is not your post. You may only edit posts you have created.', 'danger')
        return redirect(url_for('blog.my_posts'))
    form = PostForm()
    if form.validate_on_submit():
        new_title = form.title.data
        new_content = form.content.data
        print(new_title, new_content)
        post.title = new_title
        post.content = new_content
        db.session.commit()

        flash(f'{post.title} has been saved', 'success')
        return redirect(url_for('blog.post_detail', post_id=post.id))

    return render_template('post_update.html', post=post, form=form)


@blog.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You can only delete your own posts', 'danger')
        return redirect(url_for('blog.my_posts'))

    db.session.delete(post)
    db.session.commit()

    flash(f'{post.title} has been deleted', 'success')
    return redirect(url_for('blog.my_posts'))
