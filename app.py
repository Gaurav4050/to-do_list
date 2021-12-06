#flask minimal templete

from flask import Flask,render_template,request,redirect
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#data base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#creaate class
class Todo(db.Model):
    Sno=db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200),  nullable=False)
    des = db.Column(db.String(200),  nullable=False)
    Date_time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self)->str:
        return f"{self.Sno}- {self.Title}"


@app.route("/",methods=['GET','POST'])
def hello_world():
    from app import db
    from app import Todo
    db.create_all()

    if request.method=='POST':
        
        todo=Todo( Title=request.form.get('title'), des=request.form.get('desc'))
        db.session.add(todo)


    # todo=Todo( Title='first to do', des='start reading the books')
    # db.session.add(todo)
    
    db.session.commit()
    todo1=Todo.query.all()
    return render_template("index.html", alltod=todo1) #this is html

@app.route("/update/<int:ssno>",methods=['GET','POST'])
def update(ssno):

    if(request.method=="POST"):
        
        title=request.form.get('title')
        dees=request.form.get('desc')
        substance=Todo.query.filter_by(Sno=ssno).first()
        substance.Title=title
        substance.des=dees
        db.session.add(substance)
        db.session.commit()
        return redirect('/')
        


    sub_to_update=Todo.query.filter_by(Sno=ssno).first()
    return render_template('update.html', transfer=sub_to_update)

#http://127.0.0.1:8000/gaurav
@app.route("/delete/<int:ssno>")
def delete(ssno):
    sub_to_delete=Todo.query.filter_by(Sno=ssno).first()
    db.session.delete(sub_to_delete)
    db.session.commit()

    # return "this is a product page"
    return redirect('/')



if __name__==('__main__'):
    app.run(debug=True,port=8000)