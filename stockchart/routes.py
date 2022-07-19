from flask import render_template,flash, url_for,redirect
from stockchart import app
from stockchart.forms import ResgistrationForm,LoginForm
from stockchart.stock_data import get_stocks
from stockchart.models import User,Stock

stocks = get_stocks()

@app.route("/")
@app.route("/dashboard" )
def dashboard():
    return render_template('dashboard.html',stocks = stocks)

@app.route("/register",methods=['GET','POST'])
def register():
    form = ResgistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')
        return redirect(url_for('dashboard'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login Successfully','success')
        return redirect(url_for('dashboard'))
    return render_template('login.html',title='Login',form=form)
