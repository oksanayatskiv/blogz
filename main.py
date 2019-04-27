from flask import Flask, request, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
# this gives you a view into what is happening in terminal
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'booboo'

class Blog(db.Model):

 # specify the data  that go into columns
    id = db.Column(db.Integer, primary_key=True)     #  primary ID
    title = db.Column(db.Text)  # blog title
    body = db.Column(db.Text)   # blog post text
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password     

"""
# All BLOG Post
@app.route('/blog')
def all_blogs():
    # db for all blogs
    posted_blogs = Blog.query.all()
    # first of the pair matches to {{}} loop in the main_form.html template, second matches to variable post 
    return render_template('main_form.html', blogs=posted_blogs)
"""
#specify all request
@app.route("/login", methods=['GET', 'POST'])
def login():
        username_error = ''
        password_error= ''      
        #to get data out of request(if somebody want to login give chance log in)
        if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                # verify users password return retrive user with given name from db()
                existing_user = User.query.filter_by(username=username).first()
                #if query not return user it will be equal NONE
                if existing_user: 
                        if password ==  "" :
                                password_error ="Don't leave empty space."
                        elif existing_user.password != password:
                                password_error = "Invalid password"
                                
                        else:
                                existing_user.password==password
                                #'remember that the user login'
                                session['username'] = username
                                #if user login
                                return redirect("/newpost")
                                 
                else:
                        username_error="Invalid username. Try again or register"

        #not login return back to form
        return render_template('login.html', username_error=username_error,password_error=password_error)
        

    
        

@app.route("/signup", methods=['GET', 'POST'])
def signup():
        name_error = ''
        password_error= ''
        verify_error='' 

        if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                verify = request.form['verify']

                if username == "":
                        name_error = "Username cannot be blank"
                if password == "":
                        password_error = "Password cannot be blank"
                else:
                if password != verify:
                        error["verify_error"] = "Pasword and Verify must match"

                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                error["name_error"] = "There is already somebody with that username"

                if error["name_error"] == "" and error["pass_error"] == "" and error["verify_error"] == "":
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['user'] = new_user.username
                return redirect("/blog")

    return render_template("register.html", title= "Register for this Blog",
        name_error= error["name_error"], pass_error= error["pass_error"],
        verify_error= error["verify_error"])

"""
@app.route("/")
def index():

@app.route("/logout", methods=['POST'])
def logout():
    del session['username']
    return redirect("/blog")
"""

#display Each Blog Post
@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('individual_blogs.html',blog=blog)
    else:
        #get all blogs from db
        posted_blogs = Blog.query.all()
        # first of the pair matches to {{}} in for loop in the .html template, second of the pair matches to variable declared above
        return render_template('main_form.html', blogs=posted_blogs, title='Build-a-blog')


    
@app.route('/newpost', methods = ['GET','POST'] )
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
    #create object
        new_blogs = Blog(blog_title,blog_body)
        
        
        blog_title_error = ""
        blog_body_error = ""
        
        if not blog_title and not blog_body:
                blog_title_error = "Enter blog title"
                blog_body_error = "Enter blog body"
                return render_template('new_post.html', blog_title_error=blog_title_error, blog_body_error=blog_body_error )
        elif not blog_title:
                blog_title_error = "Enter blog title"
                return render_template('new_post.html', blog_title_error=blog_title_error, blog_body=blog_body)
        elif not blog_body:
                blog_body_error="Enter blog body" 
                return render_template('new_post.html', blog_body_error=blog_body_error, blog_title=blog_title)   
                
        else:
            if blog_title and blog_body:
                db.session.add(new_blogs)
                db.session.commit()
                return redirect ('/blog?id={}'.format(new_blogs.id))
            
    else:
        return render_template('new_post.html')    

    
if  __name__ == "__main__":
    app.run()