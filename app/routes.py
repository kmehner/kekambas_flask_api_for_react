from app import app
from flask import render_template
from app.forms import UserInfoForm

@app.route('/')
def index():
    name = 'Brian'
    title = 'Coding Temple Flask'
    return render_template('index.html', name_of_user=name, title=title)



@app.route('/products')
def test():
    title = 'Coding Temple Products'
    products = ['apple', 'orange', 'banana', 'peach']
    return render_template('products.html', title=title, products=products)


@app.route('/register', methods=["GET", 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        print('Hello this form has been submitted correctly')
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        print(username, email, password)
        
    return render_template('register.html', form=register_form)