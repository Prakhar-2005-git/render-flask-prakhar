from flask import Flask, render_template,request,redirect
# importing Flask class and render_template function from flask module

from flask_sqlalchemy import SQLAlchemy  
# importing SQLAlchemy class from flask_sqlalchemy module

from datetime import datetime
# importing datetime class from datetime module

app = Flask(__name__,template_folder='templates')  # creating an instance of the Flask class 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'# setting the URI for the SQLite database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # setting to False to disable modification tracking

db = SQLAlchemy(app)  # creating an instance of SQLAlchemy class with the Flask app as an argument  

class User(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # setting the default value to the current UTC date and time

    def __repr__(self):
        return f"{self.Sno} - {self.title}"  # __repr__ method to return a string representation of the object
        


@app.route('/delete/<int:Sno>')  # route() decorator to tell Flask what URL should trigger our function
def delete(Sno):
    user = User.query.filter_by(Sno=Sno).first()
    db.session.delete(user)
    db.session.commit()
    print(user)
    return redirect('/')

@app.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update(Sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        user = User.query.filter_by(Sno=Sno).first()
        user.title = title
        user.desc = desc
        db.session.add(user)
        db.session.commit()
        return redirect('/')  # Redirect to the home page after updating
    user = User.query.filter_by(Sno=Sno).first()
    return render_template('update.html', user=user)

@app.route('/',methods = ['GET','POST'])  # route() decorator to tell Flask what URL should trigger our function    
def home():
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        user = User(title=title, desc=desc)
        db.session.add(user)
        db.session.commit()
    alluser = User.query.all()
    print(alluser)
    return render_template('index.html',alluser=alluser)  # render_template() function to render HTML templates

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)  # run() method of Flask class runs the application on the local development server