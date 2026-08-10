from flask import Flask,render_template,url_for
from Forms import RegistrationForm,LoginForm
app=Flask(__name__)

app.config['SECRET_KEY']='a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'


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
        return f'Account created for {form.username.data}!'
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return f'Login successful for {form.email.data}!'
    return render_template('login.html',title='Login',form=form)

if __name__=="__main__":
    app.run(debug=True)