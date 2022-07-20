from flask import render_template,flash, url_for,redirect,request
from stockchart import app,bcrypt,db
from stockchart.forms import ResgistrationForm,LoginForm,UpdateAccountForm
from stockchart.stock_data import get_stocks
from stockchart.models import User,Stock
from flask_login import login_user,current_user,logout_user,login_required
import os
import secrets
from PIL import Image
from flask import url_for,current_app


@app.route("/")
@app.route("/dashboard" )
def dashboard():
    stocks=Stock.query.all()
    return render_template('dashboard.html',stocks = stocks)

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = ResgistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data,lastname=form.lastname.data,username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}','success')
        login_user(user,remember=False)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            flash('Login Successfully','success')
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@login_required
@app.route("/account",methods=['GET','POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit() or (current_user.email==form.email.data) or (current_user.username==form.username.data):
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form = form)


@login_required
@app.route("/portfolio",methods=['GET'])
def portfolio():
    if current_user.is_authenticated:
        user_stocks = []
        if(current_user.stocks != '.'):
            user_stocks = list(int(i) for i in current_user.stocks[1:-1].split('.'))
        stocks = []
        stock_ids = set(user_stocks)
        for stock_id in stock_ids:
            map = {}
            stock = Stock.query.get_or_404(stock_id)
            map['symbol'] = stock.symbol
            map['price'] = stock.price
            map['percent_change'] = stock.percent_change
            map['count'] = user_stocks.count(stock_id)
            map['id'] = stock_id
            stocks.append(map)
        return render_template('portfolio.html',stocks=stocks)
    else:
        return "<h1> login Please</h1>"

@app.route("/stock/<stock_id>/buy",methods=['GET','POST'])
@login_required
def buy_stock(stock_id):
    updated_stock = current_user.stocks + stock_id + '.'
    current_user.stocks = updated_stock
    db.session.commit()
    flash('you have buy this stock','success')
    return redirect(url_for('portfolio'))

@app.route("/stock/<int:stock_id>/sell",methods=['GET','POST'])
@login_required
def sell_stock(stock_id):
    user_stocks = list(i for i in current_user.stocks[1:-1].split('.'))
    user_stocks.remove(str(stock_id))
    stocks = '.'
    if(len(user_stocks)>0):
        stocks = '.' + '.'.join(user_stocks) + '.'
    current_user.stocks = stocks
    db.session.commit()
    print(current_user.stocks)
    flash('you have sell this stock','success')
    return redirect(url_for('portfolio'))
