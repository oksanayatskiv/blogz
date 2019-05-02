from flask import Flask, request, redirect,render_template,session
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
@app.before_request
def require_login():
        allowed_routes = ['login', 'signup','index','blog']
        if request.endpoint not in allowed_routes  and 'username' not in session:
                return redirect('/login')
#redirectt to home
@app.route("/")
def index():
        all_users = User.query.all()
        return render_template('index.html', all_users=all_users)

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
                        if password == "" :
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
                        return render_template('login.html', username=username, username_error=username_error )

        #not login return back to form
        return render_template('login.html', username_error=username_error,password_error=password_error)
        
#ask about session in log in and registration
#ask about login function redirect on /login should be present or it will do it automaticaly
    
        

@app.route("/signup", methods=['GET', 'POST'])
def signup():
        if request.method == 'GET':
                return render_template("signup.html")
        else:
                username = request.form['username']
                password = request.form['password']
                verify = request.form['verify']
                name_error = ''
                password_error= ''
                verify_error='' 
                #validation user name
                #no user name was entered or length user name less than 3
                existing_user = User.query.filter_by(username=username).all()

                if username == "" or len(username) < 3:
                        name_error = "Enter user name. It should be at least 3 chararcters"
                #validaion password
                #no password was entered or length of password less than 3
                if password == "" or len(password)< 3:
                        password_error = "Password cannot be blank. It should be at least 3 chararcters"
                        
                if password != verify:
                        password_error ="Passwords must match"      
                        verify_error = "Passwords must match"
                
                if existing_user:
                        name_error = "There is already somebody with that username"

                if not name_error and not password_error and not verify_error:
                #create new user
                        new_user = User(username, password)
                #add it in db
                        db.session.add(new_user)
                        db.session.commit()
                #add new_user to session(user login)

                        session['username'] = username
                        return redirect("/newpost")
                else:
                        return render_template("signup.html",username=username, name_error= name_error, password_error= password_error,verify_error= verify_error)



@app.route("/logout")
def logout():
    del session['username']
    return redirect("/blog")
"""
#display Each Blog Post
@app.route('/blog')
def blog():
        blog_id = request.args.get('id')
        user_name_id = request.args.get('owner_id')

        if blog_id:
        #get request with query parameters return
                blog = Blog.query.get(blog_id)
                return render_template('individual_blogs.html',blog=blog)
        else:
                if user_name_id:
                        ind_user_blog_posts = Blog.query.filter_by(owner_id=user_name_id)
                        return render_template('userposts.html', posts=ind_user_blog_posts)
                else:
        #get all blogs from db
                        posted_blogs = Blog.query.all()
        # first of the pair matches to {{}} in for loop in the .html template, second of the pair matches to variable declared above
                        return render_template('main_form.html', blogs=posted_blogs, title='Build-a-blog')
"""

@app.route('/blog', methods = ['POST', 'GET'])
def blog():
        blog_id = request.args.get('id')
        user_id = request.args.get('userid')
                 

# if we select blog
        if blog_id:
                blog = Blog.query.filter_by(id=blog_id).first()
                return render_template('individual_blogs.html', title=blog.title, body=blog.body,blog = blog, user=user_id)
#if we select user 
        else:
                if user_id:
                        user_blogs = Blog.query.filter_by(owner_id=user_id).all()
                        return render_template('userposts.html', user_blogs = user_blogs )
                else: 
                        all_blogs = Blog.query.all()
                        return render_template('main_form.html', blogs=all_blogs)

@app.route('/newpost', methods = ['GET','POST'] )
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
    #create object
        #new_blogs = Blog(blog_title,blog_body)
        owner = User.query.filter_by(username=session['username']).first()
        
        
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
                new_blogs = Blog(blog_title,blog_body, owner)
                db.session.add(new_blogs)
                db.session.commit()
                return redirect ('/blog?id={}'.format(new_blogs.id))
            
    else:
        return render_template('new_post.html')    

    
if  __name__ == "__main__":
    app.run()