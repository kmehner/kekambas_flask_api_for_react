from app import app, db, mail
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from app.forms import UserInfoForm, PostForm, LoginForm
from app.models import User, Post


@app.route('/')
def index():
    title = 'Coding Temple Flask'
    posts = Post.query.all()
    return render_template('index.html', title=title, posts=posts)


@app.route('/products')
def products():
    title = 'Coding Temple Products'
    products = ['apple', 'orange', 'banana', 'peach']
    return render_template('products.html', title=title, products=products)


@app.route('/register', methods=["GET", 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        # Grab Data from form
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        # Check if the username from the form already exists in the User table
        existing_user = User.query.filter_by(username=username).all()
        # If there is a user with that username message them asking them to try again
        if existing_user:
            # Flash a warning message
            flash(f'The username {username} is already registered. Please try again.', 'danger')
            # Redirect back to the register page
            return redirect(url_for('register'))

        # Create a new user instance
        new_user = User(username, email, password)
        # Add that user to the database
        db.session.add(new_user)
        db.session.commit()
        # Flash a success message thanking them for signing up
        flash(f'Thank you {username}, you have succesfully registered!', 'success')

        # Create Welcome Email to new user
        welcome_message = Message('Welcome to the Kekambas Blog!', [email])
        welcome_message.body = f'Dear {username}, Thank you for signing up for our blog. We are so excited to have you.'

        # Send Welcome Email
        mail.send(welcome_message)

        # Redirecting to the home page
        return redirect(url_for('index'))
        
    return render_template('register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab data from form
        username = form.username.data
        password = form.password.data

        # Query our User table for a user with username
        user = User.query.filter_by(username=username).first()

        # Check if the user is None or if password is incorrect
        if user is None or not user.check_password(password):
            flash('Your username or password is incorrect', 'danger')
            return redirect(url_for('login'))
        
        login_user(user)

        flash(f'Welcome {user.username}. You have succesfully logged in.', 'success')

        return redirect(url_for('index'))
        

    return render_template('login.html', login_form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/createpost', methods=['GET', 'POST'])
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


@app.route('/my-account')
@login_required
def my_account():
    return render_template('my_account.html')


@app.route('/my-posts')
@login_required
def my_posts():
    posts = current_user.posts
    return render_template('my_posts.html', posts=posts)
