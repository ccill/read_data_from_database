# Author:Sarah Shi
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD']=True
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shi'
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='mysql://root@localhost/shi',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
))
db=SQLAlchemy(app)

class File(db.Model):
    __tablename__='files'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80),unique=True)
    created_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('Category',uselist=False)
    content=db.Column(db.Text)

    def __init(self,title,created_time,category,content):
        self.title=title
        self.created_time=created_time
        self.category=category
        self.content=content

    def __repr__(self):
        return '<File : {}>'.format(self.title)

class Category(db.Model):
    __tablename__='category'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    files=db.relationship('File')

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<Category :{}>'.format(self.name)

def insert_datas():
    java=Category('Java')        #?????init????????????????????????????
    python = Category('Python')
    file1=File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2=File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()


@app.route('/')
def index():
    # return render_template('index.html',file1=db.session.query(File).all())
    return render_template('index.html', file1=File.query.all())
    # ??? /home/shiyanlou/files/ ????? json ???? `title` ????


@app.route('/files/<int:file_id>')
def file(file_id):
    #file_id=int(file_id)
    # fileid=[]
    # for i in db.session.query(File.id).all():
    #     fileid.append(i.id)
    # if file_id not in fileid:
    #     abort(404)   #??404???flask???????
    # print(file_id)
    # return render_template('file.html',item=db.session.query(File).filter(File.id==file_id).first())
    file_item=File.query.get_or_404(file_id)
    return render_template('file.html',item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
    # ????? filename.json ??????
    # ?? filename='helloshiyanlou' ????? helloshiyanlou.json ????
    # ?? filename ???????????? `shiyanlou 404` 404 ????



if __name__=='__main__':
    app.run(host='127.0.0.1',port=3000,debug=True)
    #flask run --port 3000
