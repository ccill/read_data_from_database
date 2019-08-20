# Author:Sarah Shi
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
import os
import json

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shi'
db=SQLAlchemy(app)

class File(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    created_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('Category',backref='files')
    content=db.Column(db.Text)

    def __repr__(self):
        return '<File : {}>'.format(self.title)

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))

    def __repr__(self):
        return '<Category :{}>'.format(self.name)

@app.route('/')
def index():
    return render_template('index.html',file1=db.session.query(File).all())
    # ??? /home/shiyanlou/files/ ????? json ???? `title` ????


@app.route('/files/<file_id>')
def file(file_id):
    file_id=int(file_id)
    fileid=[]
    for i in db.session.query(File.id).all():
        fileid.append(i.id)
    if file_id not in fileid:
        abort(404)   #??404???flask???????
    print(file_id)
    return render_template('file.html',item=db.session.query(File).filter(File.id==file_id).first())

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
    # ????? filename.json ??????
    # ?? filename='helloshiyanlou' ????? helloshiyanlou.json ????
    # ?? filename ???????????? `shiyanlou 404` 404 ????



if __name__=='__main__':
    app.run(host='127.0.0.1',port=3000,debug=True)
    #flask run --port 3000
