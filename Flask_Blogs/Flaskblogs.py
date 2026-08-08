from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def hello():
    return "<h1>HOME PAGE</h1>"