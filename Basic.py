from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import yaml
import sqlalchemy
from yaml import full_load_all

# with open('db_config.yml', 'r') as f:
#     doc = yaml.load(f,Loader= Full_Load(f))
# txt = doc["db_usr"]
# print(txt)

a_yaml = open("db_config.yml")
parsed_yaml_file = yaml.load(a_yaml, Loader=yaml.FullLoader)

print(parsed_yaml_file["database"])
DB = parsed_yaml_file.get("database")['database_DB']
DB_user = parsed_yaml_file.get("database")['database_usr']
DB_pswd = parsed_yaml_file.get("database")['database_pswd']
DB_host = parsed_yaml_file.get("database")['database_host']
DB_name = parsed_yaml_file.get("database")['database_name']

db1 = parsed_yaml_file.get("database").get('test')
print(db1)
app = Flask(__name__)

# string interpolation
stream = open("db_config.yml", 'r')
dictionary = yaml.load(stream)
for key, value in dictionary.items():
    print(key + " : " + str(value))

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_user}:{DB_pswd}@{DB_host}/{DB_name}'

db = SQLAlchemy(app)

print(DB)
print(DB_host)
print(DB_user)


# class configs(object):
#     database_users = 'root'
#     database_pwd = 'admin123'
#     database = 'mydb'
#
# SQLAlchemy_DATABASE_URI = f'mysql://{DB_user}:{DB_pswd}@localhost/{DB_name}'
# SQLAlchemy_TRACK_MODIFICATIONS = False

class blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    auther = db.Column(db.String(20), default='N/A')
    dateposted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __rep__(self):
        return 'blogpost' + str(self.id)


all_posts = [
    {
        'title': 'POST1',
        'content': 'FIRST POSTS DISPLAY',
        'auther': 'Umair'
    },
    {
        'title': 'POST2',
        'content': 'Second post',
        'auther': 'OWAIS'
    }

]


@app.route('/', methods=['GET', 'POST'])
def form1():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_auther = request.form['auther']
        new_post = blogpost(title=post_title, content=post_content, auther=post_auther)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = blogpost.query.order_by(blogpost.dateposted).all()
        return render_template('posts.html', posts=all_posts)
        # return 'welcomeposts'


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = blogpost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.auther = request.form['auther']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('updates.html', post=post)


# @app.route('/posts/Update/<int:id>')
# def update(id):


@app.route('/home/<string:name>')
def home(name):
    return "Hello ," + name


@app.route('/onlyget', methods=['POST'])
def onlyget():
    return 'hey this your webptage'


if __name__ == '__main__':
    app.run(debug=True)
