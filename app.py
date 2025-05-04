from flask import Flask, render_template, flash,request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
import os
from flask_cors import CORS

app = Flask(__name__, template_folder='WEB_Project/templates', static_folder='WEB_Project/static')
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))

username = 'root'
password = 'Hss2003HHss2003H'
database = 'moodle'

SQLALCHEMY_DATABASE_URI = f'mysql://{username}:{password}@localhost/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

with app.app_context():
    db.Model.metadata.reflect(db.engine)

class User(UserMixin, db.Model):
    _table_ = db.metadata.tables['users']  # Changed 'Users' to 'users'
    def get_id(self):
        return (self.id)

# class User(UserMixin,db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     password_hash = db.Column(db.String(500), nullable=False)
#     role = db.Column(db.Enum('student', 'teacher'), nullable=False)

# class Course(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('courses', lazy=True))

# class Enrollements(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('enrollments', lazy=True))
#     course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))
#     _table_args_ = (db.UniqueConstraint('user_id', 'course_id'),)

# class CourseMaterial(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
#     material_type = db.Column(db.Enum('pdf', 'assignment', 'exam'), nullable=False)
#     material_name = db.Column(db.String(255), nullable=False)
#     material_url = db.Column(db.String(255), nullable=False)
#     course = db.relationship('Course', backref=db.backref('course_materials', lazy=True))

# class Submission(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     course_material_id = db.Column(db.Integer, db.ForeignKey('course_material.id'), nullable=False)
#     submission_text = db.Column(db.Text)
#     submission_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
#     user = db.relationship('User', backref=db.backref('submissions', lazy=True))
#     course_material = db.relationship('CourseMaterial', backref=db.backref('submissions', lazy=True))

with app.app_context():
    db.create_all()


class Course(UserMixin, db.Model):
    _table_=db.metadata.tables['courses']

# class Course_sections(UserMixin, db.Model):
#     _table_=db.metadata.tables['course_sections']

class Enrollements(UserMixin, db.Model):
    _table_=db.metadata.tables['enrollements']

class CourseMaterials(UserMixin, db.Model):
    _table_ = db.metadata.tables['coursematerials']  

class Submissions(UserMixin, db.Model):
    _table_=db.metadata.tables['submissions']

# class User(UserMixin, db.Model):
#     _tablename_ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(500), nullable=False)
#     role = db.Column(db.Enum('student', 'instructor'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash,password):
            if check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # return "hellos"
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email'] 
        password = request.form['password']
        print(f"Username: {username}, Email: {email}, Password: {password}")
        new_user = User(username=username,email=email, password_hash=generate_password_hash(password), role="student")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('Main.html')
    else:
        flash('You are not logged in. Please log in to access this page.', 'warning')
        return redirect(url_for('login'))  # Assuming you have a route named 'login'


@app.route('/userProfile')
def user_profile():
    return render_template('profile.html')
    
# @app.route('/Courses')
# def courses():
#     return render_template('UserCourses.html')

@app.route('/profile')
@login_required
def profile():
    user_id=current_user.id
    print(user_id)
    # Retrieve user information from the database
    Users = User.query.filter_by(id=user_id)
    User_list=[]
    for user in Users:
        User_list.append({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role   
        })
    return jsonify(User_list)

@app.route('/dashboard_data')
@login_required
def dashboard_data():
    # Retrieve the user's enrolled courses
    user_id = current_user.id
    print(user_id)
    user_courses = Course.query.filter_by(UserId=user_id).all() #awl wehde shu maktube bel db

    # Retrieve course information for the enrolled courses
    courses = []
    for course in user_courses:
        courses.append({
            'id': course.id,
            'title': course.title
        })
    return jsonify(courses)

@app.route('/admin_courses')
@login_required
def admin_courses():
    courses = Course.query.all()
    
    course_list = []
    for course in courses:
        # Retrieve all materials for the current course
        materials = CourseMaterials.query.filter_by(CourseId=course.id).all()
        
        material_list = []
        
        for material in materials:
            
            material_list.append({
                'id': material.id,
                'type': material.MaterialType,
                'name': material.MaterialName,
                'url': material.MaterialUrl
            })
        
        course_list.append({
            'id': course.id,
            'title': course.title,
            'materials': material_list
        })
    
    
    return jsonify(course_list)

# @app.route('/api/user', methods=['GET'])
# @login_required
# def get_user():
#     user = User.query.filter_by(id=current_user.id).first()
#     if user:
#         return jsonify({
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'role': user.role
#         })
#     else:
#         return jsonify({'error': 'User not found'}), 404


@app.route('/usercourses')
@login_required
def user_courses():
    # Query the database to retrieve the courses the current user is enrolled in
    user_courses = Course.query \
        .join(Enrollements, Course.id == Enrollements.course_id) \
        .filter(Enrollements.user_id == current_user.id) \
        .all()
    
    # Render the template with the user's courses and related information
    return render_template('UserCourses.html', courses=user_courses)

@app.route('/add_courses')
def add_courses():
    if current_user.role == 'instructor':
        return render_template('AddCourses.html')
    else:
        return 'You are not authorized to access this page.', 403

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  
    app.run(debug=True)