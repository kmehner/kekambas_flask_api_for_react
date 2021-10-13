from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import UserInfoForm, PostForm
from app.models import User, Post


@app.route('/')
def index():
    name = 'Brian'
    title = 'Coding Temple Flask'
    return render_template('index.html', name_of_user=name, title=title)


@app.route('/products')
def products():
    title = 'Coding Temple Products'
    products = ['apple', 'orange', 'banana', 'peach']
    return render_template('products.html', title=title, products=products)


@app.route('/register', methods=["GET", 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).all()
        if existing_user:
            # Flash a warning message
            flash(f'The username {username} is already registered. Please try again.', 'danger')
            # Redirect back to the register page
            return redirect(url_for('register'))

        new_user = User(username, email, password)

        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username}, you have succesfully registered!', 'success')
    
        return redirect(url_for('index'))
        
    return render_template('register.html', form=register_form)


@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        print('Hello')
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, user_id=1)
        db.session.add(new_post)
        db.session.commit()
    return render_template('createpost.html', form=form)