from flask import Flask, render_template, redirect, url_for, flash,request,send_from_directory,jsonify
from flask_bootstrap import Bootstrap 
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from functools import wraps
from flask import abort
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, URL,Email
from flask_ckeditor import CKEditorField
import math

UPLOAD_FOLDER = 'static/user/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "shopdodoododdododoododoo234o354"
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///nayana.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class LoginForm(FlaskForm):
	email    = StringField("Email",validators=[DataRequired(),Email()])
	password = PasswordField("Password",validators=[DataRequired()])
	submit   = SubmitField("Let me in!")


class RegistrationForm(FlaskForm):
    email    = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    name     = StringField("Name",validators=[DataRequired()])
    submit   = SubmitField("Sign up")

class Product(FlaskForm):
    title 	 = StringField("Product Name", validators=[DataRequired()])
    cost = StringField("Cost(No money symbol)", validators=[DataRequired()])
    img    = FileField('Image',validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    in_stock = StringField("Stock", validators=[DataRequired()])
    submit 	 = SubmitField("Submit Post")

class Products(db.Model):
	__tablename__='Products'
	id = db.Column(db.Integer,primary_key=True)
	product_name = db.Column(db.String(500),nullable=False)
	img_url = db.Column(db.String(500))
	description = db.Column(db.Text)
	cost = db.Column(db.Float(10),nullable=False)
	stock = db.Column(db.Float(10),nullable=True)
	importer = db.Column(db.String(500),nullable=True)
	exporter = db.Column(db.String(500),nullable=True)
	carts = relationship('Cart',back_populates='product')
	productorder = relationship('ProductOrder',back_populates='product')


class Users(UserMixin,db.Model):
	__tablename__="Users"
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(500),nullable=False,unique=True)
	name = db.Column(db.String(500),nullable=False)
	password = db.Column(db.String(1000),nullable=False)
	rating = db.Column(db.Float(3),nullable=True)
	cart = relationship('Cart',back_populates='created')
	address = db.Column(db.Text,nullable=True)
	order = relationship('Orders',back_populates='ordered')
	city = db.Column(db.Text,nullable=True)
	state = db.Column(db.Text,nullable=True)
	country = db.Column(db.Text,nullable=True)
	

class Cart(db.Model):
	__tablename__="Cart"
	id = db.Column(db.Integer,primary_key=True)
	created_by =  db.Column(db.Integer,db.ForeignKey('Users.id'))
	created  = relationship('Users',back_populates='cart')
	product_id = db.Column(db.Integer,db.ForeignKey('Products.id'))
	product    = relationship('Products',back_populates='carts')
	number_of_products = db.Column(db.Float(3),nullable=False)
		
class Orders(db.Model):
	__tablename__ = "Orders"
	id = db.Column(db.Integer,primary_key=True)
	ordered_by =  db.Column(db.Integer,db.ForeignKey('Users.id'))
	ordered  = relationship('Users',back_populates='order')
	cost = db.Column(db.Float(10),nullable=False)
	address = db.Column(db.Text,nullable=False)
	city = db.Column(db.Text,nullable=False)
	state = db.Column(db.Text,nullable=False)
	country = db.Column(db.Text,nullable=False)
	is_paid = db.Column(db.Boolean())
	is_delivered = db.Column(db.Boolean())
	productandorder = relationship('ProductOrder',back_populates='order')

class ProductOrder(db.Model):
	__tablename__ = 'ProductOrder'
	id = db.Column(db.Integer,primary_key=True)
	order_id = db.Column(db.Integer,db.ForeignKey('Orders.id'))
	order = relationship('Orders',back_populates='productandorder')
	product_id =  db.Column(db.Integer,db.ForeignKey('Products.id'))
	product = relationship('Products',back_populates='productorder')
	number_of_products = db.Column(db.Float(3),nullable=False)
		

db.create_all()

def admin_only(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if current_user.id != 1:
            return abort(404)
        return f(*args,*kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

QTY = 0



@app.route('/')
def home():
	return render_template('index.html')

@app.route('/demo')
def demo():
	return render_template('trial.html')

@app.route('/scroller')
def scroller():
	return render_template('screenscroll.html',x=range(1,290,1))	

@app.route('/shop')
def shop():
	products = Products.query.all()
	return render_template('shop-list.html',products=products,qty=q_calculator())

@app.route('/shop/<int:id>',methods=['GET','POST'])
def items(id):
	product = Products.query.get(id)
	if request.method == 'POST':
		qty = request.form['qty']
		try:
			cart = Cart(created = current_user ,product=product,number_of_products=qty)
			db.session.add(cart)
			db.session.commit()
		except AttributeError:
			return redirect('/login')
		
		else:
			count = cart_cleaner()
			products = list(count.keys())
			number_of_products = list(count.values())
			for i in Cart.query.filter_by(created =current_user).all():
				db.session.delete(i)
				db.session.commit()

			for n,i in enumerate(products):
				cart = Cart(created = current_user ,product=i,number_of_products=number_of_products[n])
				if number_of_products[n]!=0:
					print('Not xero')
					db.session.add(cart)
					db.session.commit()

			return render_template('shop-item.html',product=product,qty=q_calculator(),len=len)

	return render_template('shop-item.html',product=product,qty=q_calculator(),len=len)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin/add-products', methods=['GET', 'POST'])
@login_required
@admin_only
def add_file():
	form = Product()
	if form.validate_on_submit():
		file = form.img.data
		print(file)
		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			print('success')
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			new_product = Products(
            product_name=form.title.data,
            cost=form.cost.data,
            description=form.description.data,
            img_url=url_for('static',filename=f"user/uploads/{filename}"),
            stock = form.in_stock.data
		        )
			db.session.add(new_product)
			db.session.commit()
			return redirect(url_for('view_products'))

	return render_template('add-item.html',form=form)

@app.route('/cart',methods=['GET','POST'])
@login_required
def cart():
	count=cart_cleaner()
	print(count)
	return render_template('cart.html',items=list(count.keys()),count=list(count.values()),enumerate=enumerate,qty=q_calculator())

@app.route('/order_change',methods=['POST'])
def update_cart():
	if request.method == "POST":
		user_cart = Cart.query.filter_by(created_by=current_user.id).all()
		for i in user_cart:
			i.number_of_products =  request.form[f"product[{str(i.product_id)}]"]
			db.session.commit()
		return redirect(url_for('cart'))



@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		name = form.name.data
		if Users.query.filter_by(email = email).first():
			flash("This email already exist")
			return redirect(url_for('login'))
		else:
			hash_and_salted_password = generate_password_hash(
				password,
				method='pbkdf2:sha256',
				salt_length=8
				)
			new_user = Users(email = email,password=hash_and_salted_password,name=name)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user)
		return redirect('/shop')
	return render_template("register.html",form = form,logged_in=current_user.is_authenticated)


@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect('/')
            else:
                flash("Incorrect Username or password")
        else:
            flash("This Email doesn't Exist")


    return render_template("login.html",form = form ,logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def cart_cleaner():
	cartu = Cart.query.all()
	for cart in cartu:
		if cart.number_of_products == 0 or cart.number_of_products==0.0:
			db.session.delete(cart)
			db.session.commit()
	items = Cart.query.filter_by(created_by=current_user.id).all()
	names = [Products.query.get(item.product_id) for item in items]
	names = list(set(names))
	count = dict(zip(names,[0 for name in names]))
	print(count)
	for item in items:
		x = Products.query.get(item.product_id)
		for j in names:
			if x == j:
				count[x]+=item.number_of_products
	return count

@app.route('/buy-more',methods=['GET','POST'])
def buy_many():
	products = Cart.query.filter_by(created_by=current_user.id).all()
	if request.method == "POST":
		current_user.address = request.form['address']
		current_user.state = request.form['state']
		current_user.city = request.form['city']
		current_user.country = request.form['country']
		db.session.commit()
		return redirect('/confirmed')

	items = []
	cost = 0
	for product in products:
		product_details = Products.query.get(product.product_id)
		total_cost = float(float(product.number_of_products)*float(product_details.cost))
		item = (product_details.product_name,product.number_of_products,product_details.cost,total_cost,product_details.img_url)
		items.append(item)
		cost+=float(total_cost)
	return render_template('confiramtion.html',items=items,cost=cost)

@app.route('/confirmed')
def bought_many():
	cost = 0
	products = list(Cart.query.filter_by(created_by=current_user.id).all())
	for product in products:
		product_details = Products.query.get(product.product_id)
		total_cost = float(float(product.number_of_products)*float(product_details.cost))
		cost+=float(total_cost)
	
	for product in products:
		product_details = Products.query.get(product.product_id)
		product_details.stock -= int(product.number_of_products)
		db.session.commit()

	ordered_details = Orders(ordered=current_user,
		cost=cost,
		is_delivered=False,
		is_paid=False,
		address=current_user.address,
		city=current_user.city,
		state=current_user.state,
		country=current_user.country)
	db.session.add(ordered_details)
	db.session.commit()
	for product in products:
		Product_of_order = ProductOrder(order=ordered_details,product=Products.query.get(product.product_id),number_of_products=float(product.number_of_products))
		db.session.add(Product_of_order)
		db.session.commit()

	cart_of_user = Cart.query.filter_by(created_by=current_user.id)
	for item in cart_of_user:
		db.session.delete(item)
		db.session.commit()

	return render_template('confirmed.html')

@app.route('/admin',methods=['GET','POST'])
@login_required
@admin_only
def admin():
	order_not_delivered = Orders.query.filter_by(is_delivered=False).all()
	customers = Users.query.all()
	if request.method == "POST":
		print(request.method)
		for order in order_not_delivered:
			value = {
			'on':True,
			'off':False,
			}
			try:
				order.is_paid = value.get(request.form[f'is_paid{order.id}'])
			except KeyError:
				order.is_paid = False
			try:
				order.is_delivered = value.get(request.form[f'is_delivered{order.id}'])
			except KeyError:
				order.is_delivered = False
			db.session.commit()
			print("working")
		return redirect('/admin')
	return render_template('admin-dash.html',ordered=order_not_delivered,User=Users)

@app.route('/admin/delivered')
@login_required
@admin_only
def admin_delivered():
	order_not_delivered = Orders.query.filter_by(is_delivered=True).all()
	customers = Users.query.all()
	return render_template('admin-dash.html',ordered=order_not_delivered,User=Users,x=True)

@app.route('/admin/view-products')
@login_required
@admin_only
def view_products():
	products = Products.query.all()
	return render_template('admin-dash-pro.html',products=products,data={'name':[product.product_name for product in products],'stock':[product.stock for product in products]})

@app.route('/stock-count')
def stock():
	products = Products.query.all()
	return jsonify({'name':[product.product_name for product in products],'stock':[product.stock for product in products],'cost':[product.cost for product in products]})

@app.route('/product-value')
def product_value():
	order_delivered = Orders.query.filter_by(is_delivered=False)
	return jsonify({'name':[product.id for product in order_delivered],'cost':[order.cost for order in order_delivered]})


@login_required
@admin_only
@app.route('/delete/<int:id>')
def delete_product(id):
	product = Products.query.get(id)
	db.session.delete(product)
	db.session.commit()
	return redirect('/admin/view-products')

@login_required
@admin_only
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_product(id):
	product = Products.query.get(id)
	print(product)
	form = Product(title=product.product_name,cost=product.cost,in_stock=product.stock,description=product.description)
	if form.validate_on_submit():
		file = form.img.data
		print(file)
		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			print('success')
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			product.product_name=form.title.data
			product.cost=form.cost.data
			product.description=form.description.data
			product.img_url=url_for('static',filename=f"user/uploads/{filename}")
			product.stock = form.in_stock.data
			db.session.commit()
		return redirect('/admin/view-products')
	return render_template('add-item.html',form=form)


def q_calculator():
	try:
		QTY = 0
		for i in Cart.query.filter_by(created_by=current_user.id).all():
			QTY+=i.number_of_products
	except Exception as e:
		print(e)
		QTY = 0
	return QTY

if __name__ == '__main__':
	app.run(debug=True)
