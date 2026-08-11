from flask import render_template,url_for,flash,redirect
from flaskblog.Forms import RegistrationForm,LoginForm
from flaskblog import app

from flaskblog.models import User,Post

posts=[
    {
        'author':'John Doe',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted':'April 20,2024'
    },
    {
        'author':'Jane Smith',
        'title':'Blog Post 2',
        'content':'Second post content',
        'date_posted':'April 21,2024'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title="ABOUT"
    "")

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data=='user@gmail.com' and form.password.data=='password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        #return f'Login successful for {form.email.data}!'
    return render_template('login.html',title='Login',form=form)

