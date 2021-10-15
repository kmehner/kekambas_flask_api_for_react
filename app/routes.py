from app import app
from flask import render_template
from app.blueprints.blog.models import Post


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




