from ast import dump

from flask import *
from datetime import *
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@127.0.0.1:8889/FlaskDB'
db=SQLAlchemy(app)
logi='0'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        # pass   ADD TO DATABASE,  SHOULD CHECK IF THIS EMAIL EXISTS
        name1=request.form['name']
        email1=request.form['email']
        confPass1=request.form['confPass']
        password1=request.form['password']
        if (confPass1!=password1):
            return "Please write again"
        else:
            user=User(name=name1,email=email1,password=password1)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/login')
            except:
                return "Try again please <a href='/'> here</a>"
    else:
        return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email1 = request.form['email']
        password1 = request.form['password']
        users=User.query.all()
        fl=0
        for user in users:
            if user.email==email1 and user.password==password1:
                login = user.email
                fl=1
                break
        if fl:
            return redirect('/all_users')
            # return login
        else:
            return "Try again please <a href='/'> here</a>"
    else:
        return render_template('login.html')

@app.route('/all_users')
def allUsers():
    return dump(logi)
    # return render_template('allUsers.html',logi=login)



if __name__=='__main__':
    app.run(debug=True)
