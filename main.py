from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env= jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True )

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
# this gives you a view into what is happening in terminal
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

 # specify the data  that go into columns
    id = db.Column(db.Integer, primary_key=True)     #  primary ID
    title = db.Column(db.Text)  # blog title
    body = db.Column(db.Text)   # blog post text

    def __init__(self, title, body):
        self.title = title
        self.body = body 
"""
# All BLOG Post
@app.route('/blog')
def all_blogs():
    # db for all blogs
    posted_blogs = Blog.query.all()
    # first of the pair matches to {{}} loop in the main_form.html template, second matches to variable post 
    return render_template('main_form.html', blogs=posted_blogs)
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
                return render_template('new_post.html', blog_title=blog_title, blog_body_error=blog_body_error)   
                
        else:
            if blog_title and blog_body:
                db.session.add(new_blogs)
                db.session.commit()
                return redirect ('/blog?id={}'.format(new_blogs.id))
            
    else:
        return render_template('new_post.html')    

    
if  __name__ == "__main__":
    app.run()