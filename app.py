from cmath import nan
from flask import Flask, flash, request, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
api = Api(app)

class COEP_Members(db.Model):    
    name = db.Column(db.String(100))
    mis = db.Column(db.Integer(), primary_key=True, nullable=False)
    email = db.Column(db.String())
    project = db.Column(db.String(100), nullable=False)
    since = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(member, name, mis, email, project):
        member.name = name
        member.mis = mis
        member.email = email
        member.project = project

    def json(member):
        return jsonify(Name = member.name,
        MIS = member.mis,
        Email = member.email,
        Project = member.project)
    
    def __str__(member):
        return f" Name of COEP Member: {member.name}\nMIS: {member.mis}\nEmail: {member.email}"
    

class COEP_Projects(db.Model):
    # id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    projectName = db.Column(db.String(100), primary_key=True)
    projectDesc = db.Column(db.String(500))
    mis_projectHead = db.Column(db.Integer())
    email_projectHead = db.Column(db.String())
    started = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    marks = db.Column(db.Integer())

    def __init__(project, projectName, projectDesc, mis_projectHead, email_projectHead, marks = 0):
        project.projectName = projectName
        project.projectDesc = projectDesc
        project.mis_projectHead = mis_projectHead
        project.email_projectHead = email_projectHead
        project.marks = marks

    def json(project):
        return jsonify(Project_Name = project.projectName,
        MIS_Head = project.mis_projectHead,
        Email_Head = project.email_projectHead,
        Project_Desc = project.projectDesc,
        Marks = project.marks)
        # return {'Name: ': project.projectName, 'Project Description: ': project.projectDesc, 'MIS of Project Head: ': project.mis_projectHead, 'Email of Project Head: ': project.email_projectHead}

    def __str__(project):
        return f" Name of Project: {project.name}\nProject Description: {project.desc}\nMIS: {project.mis}\nEmail: {project.email}"

class COEP_API_History(db.Model):   
    id = db.Column(db.Integer(), primary_key=True) 
    operation = db.Column(db.String())
    performedOn = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(history, operation):
        history.operation = operation

    def json(history):
        return jsonify(Operation = history.operation)

    def __str__(history):
        return f" Operation Performed: {history.operation}"

db.create_all()
# member = COEP_Members(name="SHIKHAR", mis=112003005, email="agarawalsd20.comp@coep.ac.in")
# db.session.add(member)
# db.session.commit()
@app.route("/")
def HomePage():
    return render_template("home.html")

@app.route('/members/<project>', methods=['GET'])
def read_members(project):
    if request.method == 'GET':
        members = COEP_Members.query.all()
        # history = COEP_API_History(operation="Read Members")
        # db.session.add(history)
        # db.session.commit()
        return render_template("members.html", get=members, project = project)

UserName = ['112003003', '112003005', '112003006', '112003014']
PassWord = ['Kedar', 'Shikhar', 'Anshul', 'Gourav']

@app.route('/members/', methods=['GET', 'POST'])
def create_member():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        try:
            username = request.form['Username']
            Password = request.form['Password']
        except KeyError:
            return member_detail(name = request.form['Name'], mis = request.form['MIS'], email = request.form['Email'], project = request.form['Project'])
        try:
            UserIndex = UserName.index(username)
        except ValueError:
            UserIndex = -1
        try:
            PassIndex = PassWord.index(Password)
        except ValueError:
            PassIndex = -1
        if UserIndex ==  PassIndex and UserIndex != -1:
            flash('Logged in Succesfully')
            return render_template("members_form.html")
        else:
            error = "Invalid Credential"
            return render_template('login.html', error = error)

def member_detail(name, mis, email, project):
        members = COEP_Members(name, mis, email, project)
        db.session.add(members)
        db.session.commit()
        history = COEP_API_History(operation=("Created Member: " + str(mis)))
        db.session.add(history)
        db.session.commit()
        return redirect("/members/"+str(project))

@app.route('/members/<project>/delete/<mis>', methods=['GET', 'POST'])
def delete_member(project, mis):
    if request.method == 'GET':
        return render_template("login.html") 
    if request.method == 'POST':
        try:
            username = request.form['Username']
            Password = request.form['Password']
        except KeyError:
            return render_template("login.html")
        try:
            UserIndex = UserName.index(username)
        except ValueError:
            UserIndex = -1
        try:
            PassIndex = PassWord.index(Password)
        except ValueError:
            PassIndex = -1
        if UserIndex ==  PassIndex and UserIndex != -1:
            flash('Logged in Succesfully')
            return member_delete(project, mis)
        else:
            error = "Invalid Credential"
            return render_template('login.html', error = error)
def member_delete(project, mis):
        ex_member = COEP_Members.query.filter_by(mis=mis).first()
        history = COEP_API_History(operation="Deleted Member: " + str(mis))
        db.session.delete(ex_member)
        db.session.add(history)
        db.session.commit()
        return redirect("/members/"+str(project))

@app.route('/members/<project>/update/<mis>', methods=['GET', 'POST'])
def update_member(project, mis):
    member = COEP_Members.query.filter_by(mis=mis).first()
    if request.method == 'GET':
        return render_template("login.html") 
    if request.method == 'POST':
        try:
            username = request.form['Username']
            Password = request.form['Password']
        except KeyError:
            return member_update(member, project)
        try:
            UserIndex = UserName.index(username)
        except ValueError:
            UserIndex = -1
        try:
            PassIndex = PassWord.index(Password)
        except ValueError:
            PassIndex = -1
        if UserIndex ==  PassIndex and UserIndex != -1:
            flash('Logged in Succesfully')
            return render_template("members_update.html", update=member)
        else:
            error = "Invalid Credential"
            return render_template('login.html', error = error)

def member_update(member, project):
    if request.method == 'GET':
        return render_template("members_update.html", update=member)
    if request.method == 'POST':
        member.name = request.form['Name']
        member.mis = request.form['MIS']
        member.email = request.form['Email']
        member.project = request.form['Project']
        history = COEP_API_History(operation="Updated Member Info")
        db.session.add(history)
        # members = COEP_Members(member.name, member.mis, member.email, member.project)
        # db.session.update(members)
        db.session.commit()

        if not COEP_Projects.query.filter_by(projectName = member.project).first():
            project = COEP_Projects(projectName=member.project, projectDesc="Not Available", mis_projectHead=member.mis, email_projectHead=member.email)
            db.session.add(project)
            history = COEP_API_History(operation=("Created Project: " + member.project))
            db.session.add(history)
            db.session.commit()

        return redirect("/members/"+str(member.project))
        # return redirect(url_for('read_members'))

@app.route('/projects', methods=['GET'])
def read_projects():
    if request.method == 'GET':
        projects = COEP_Projects.query.all()
        db.session.commit()
        return render_template("project.html", get=projects)

@app.route('/projects/', methods=['GET', 'POST'])
def create_project():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        try:
            username = request.form['Username']
            Password = request.form['Password']
        except KeyError:
            return project_detail(projectName = request.form['projectName'], projectDesc = request.form['projectDesc'], Mis_projectHead = request.form['Mis_projectHead'], Email_projectHead = request.form['Email_projectHead'])
        try:
            UserIndex = UserName.index(username)
        except ValueError:
            UserIndex = -1
        try:
            PassIndex = PassWord.index(Password)
        except ValueError:
            PassIndex = -1
        if UserIndex ==  PassIndex and UserIndex != -1:
            flash('Logged in Succesfully')
            return render_template("projects_form.html")
        else:
            error = "Invalid Credential"
            return render_template('login.html', error = error)
def project_detail(projectName, projectDesc, Mis_projectHead, Email_projectHead):
    project = COEP_Projects(projectName=projectName, projectDesc=projectDesc, mis_projectHead=Mis_projectHead, email_projectHead=Email_projectHead)
    db.session.add(project)
    # if request.method == 'GET':
    #     return render_template("projects_form.html")
    # if request.method == 'POST':
    #     project.projectName = request.form['projectName']
    #     project.projectDesc = request.form['projectDesc']
    #     project.mis_projectHead = request.form['Mis_projectHead']
    #     project.email_projectHead = request.form['Email_projectHead']
    history = COEP_API_History(operation=("Created Project: " + project.projectName))
    db.session.add(history)
        # print(request.form['projectName'], ['projectDesc'], ['Mis_projectHead'], ['Email_projectHead'])
        # print(projectName, projectDesc, mis_projectHead, email_projectHead)
        # newProject = COEP_Projects(projectName=projectName, projectDesc=projectDesc, mis_projectHead=mis_projectHead, email_projectHead=email_projectHead)
        # db.session.add(newProject)
    db.session.commit()
    return redirect(url_for('read_projects'))

@app.route('/projects/delete/<projectName>', methods=['GET', 'POST'])
def delete_project(projectName):
    if request.method == 'GET':
        return render_template("login.html") 
    if request.method == 'POST':
        try:
            username = request.form['Username']
            Password = request.form['Password']
        except KeyError:
            return render_template("login.html")
        try:
            UserIndex = UserName.index(username)
        except ValueError:
            UserIndex = -1
        try:
            PassIndex = PassWord.index(Password)
        except ValueError:
            PassIndex = -1
        if UserIndex ==  PassIndex and UserIndex != -1:
            flash('Logged in Succesfully')
            return project_delete(projectName)
        else:
            error = "Invalid Credential"
            return render_template('login.html', error = error)
def project_delete(projectName):
    old_project = COEP_Projects.query.filter_by(projectName=projectName).first()
    history = COEP_API_History(operation=("Deleted Project: " + projectName))
    db.session.delete(old_project)
    db.session.add(history)
    db.session.commit()
    return redirect("/projects")

@app.route('/projects/update/<projectName>', methods=['GET', 'POST'])
def update_project(projectName):
    project = COEP_Projects.query.filter_by(projectName=projectName).first()
    if request.method == 'GET':
        return render_template("login.html") 
    if request.method == 'POST':
        try:
            username = request.form['Username']
            Password = request.form['Password']
        except KeyError:
            return project_update(projectName, project)
        try:
            UserIndex = UserName.index(username)
        except ValueError:
            UserIndex = -1
        try:
            PassIndex = PassWord.index(Password)
        except ValueError:
            PassIndex = -1
        if UserIndex ==  PassIndex and UserIndex != -1:
            flash('Logged in Succesfully')
            return render_template("project_update.html", update=project)
        else:
            error = "Invalid Credential"
            return render_template('login.html', error = error)

def project_update(projectName, project):
    if request.method == 'GET':
        return render_template("project_update.html", update=project)
    if request.method == 'POST':
        project.projectName = request.form['projectName']
        project.projectDesc = request.form['projectDesc']
        project.mis_projectHead = request.form['Mis_projectHead']
        project.email_projectHead = request.form['Email_projectHead']
        project.marks = request.form['Marks']
        history = COEP_API_History(operation="Updated Project Info")
        db.session.add(history)
        db.session.commit()
        # members = COEP_Members(name, mis, email)
        # db.session.update(members)
        return redirect(url_for('read_projects'))

@app.route('/history', methods=['GET'])
def read_history():
    if request.method == 'GET':
        history = COEP_API_History.query.all()
        return render_template("history.html", get=history)

class COEP_Member(Resource):
    def get(self, mis):
        check_member = db.session.query(db.exists().where(COEP_Members.mis == mis)).scalar()
        get_member_info = COEP_Members.query.filter_by(mis=mis).first()

        if check_member:
            history = COEP_API_History(operation="Read Specific Member Info")
            db.session.add(history)
            db.session.commit()
            return get_member_info.json()
        else:
            history = COEP_API_History(operation="Tried Reading Specific Member Info but Member Not Found")
            db.session.add(history)
            db.session.commit()
            return "Member not found", 404

    def post(self,name, mis, email):
        member = COEP_Members(name=name, mis=mis, email=email)
        history = COEP_API_History(operation="Created Member: " + str(mis))
        db.session.add(history)
        db.session.add(member)
        db.session.commit()
        
        return f"Member Created successfully \n{member.json()}"

    def delete(self,name, mis, email):
        check_member = db.session.query(db.exists().where(COEP_Members.mis == mis and COEP_Members.name == name and COEP_Members.email == email)).scalar()
        get_member_info = COEP_Members.query.filter_by(mis=mis).first()

        if check_member:
            history = COEP_API_History(operation="Deleted Member: " + str(mis))
            db.session.delete(get_member_info)
            db.session.add(history)
            db.session.commit()
            return "Member Deleted Successfully"
        else:
            history = COEP_API_History(operation="Tried Deleting Specific Member Info but Member Not Found")
            db.session.add(history)
            db.session.commit()
            return "Member not found", 404

class COEP_Project(Resource):
    def get(self, projectName):
        check_project = db.session.query(db.exists().where(COEP_Projects.projectName == projectName)).scalar()
        get_project_info = COEP_Projects.query.filter_by(projectName=projectName).first()
        if check_project:
            history = COEP_API_History(operation="Read Specific Project Info")
            db.session.add(history)
            db.session.commit()
            return get_project_info.json()
        else:
            history = COEP_API_History(operation="Tried Reading Specific Project Info but Project Not Found")
            db.session.add(history)
            db.session.commit()
            return "Project not found", 404

    def post(self, projectName, projectDesc, mis_projectHead, email_projectHead):
        project = COEP_Projects(projectName=projectName, projectDesc=projectDesc, mis_projectHead=mis_projectHead, email_projectHead=email_projectHead)
        history = COEP_API_History(operation="Created Project: " + projectName)
        db.session.add(history)
        db.session.add(project)
        db.session.commit()
        
        return f"Project Created successfully \n{project.json()}"

    def delete(self, projectName, projectDesc, mis_projectHead, email_projectHead):
        check_project = db.session.query(db.exists().where(COEP_Projects.mis_projectHead == mis_projectHead and COEP_Projects.projectName == projectName and COEP_Projects.email_projectHead == email_projectHead and COEP_Projects.projectDesc == projectDesc)).scalar()
        get_project_info = COEP_Projects.query.filter_by(projectName=projectName).first()

        if check_project:
            history = COEP_API_History(operation="Deleted Project: " + projectName)
            db.session.delete(get_project_info)
            db.session.add(history)
            db.session.commit()
            return "Project Deleted Successfully"
        else:
            history = COEP_API_History(operation="Tried Deleting Specific Project Info but Project Not Found")
            db.session.add(history)
            db.session.commit()
            return "Project not found", 404

# class COEP_Alldata(Resource):
#     def get(self, type):
#         if type == "members_json":
#             members = COEP_Members.query.all()
#             for member in members:
#                 return member.json()
#             history = COEP_API_History(operation="Read All Members info")
#             db.session.add(history)
#             db.session.commit()
#         elif type == "projects_json":
#             projects = COEP_Projects.query.all()
#             for project in projects:
#                 return project.json()
#             history = COEP_API_History(operation="Read All Projects info")
#             db.session.add(history)
#             db.session.commit()

#         elif type == "alldata_json":
#             members = COEP_Members.query.all()
#             for member in members:
#                 return member.json()
#             projects = COEP_Projects.query.all()
#             for project in projects:
#                 return project.json()
#             history = COEP_API_History(operation="Read All Members and Projects info")
#             db.session.add(history)
#             db.session.commit()
            
#         else:
#             history = COEP_API_History(operation="Tried Reading Info but NOT FOUND")
#             db.session.add(history)
#             db.session.commit()
#             return "Data NOT FOUND"

# class COEP_Members_Json(Resource):
#     def get(self, type):
#         if type == "members":
#             history = COEP_API_History(operation="Read All Members Info")
#             db.session.add(history)
#             db.session.commit()
#             # members =[]
#             member_all = COEP_Members.query.all()
#             # for member in member_all:
#                 # member = member.json()
#                 # members.append(member)
#             # members = jsonify(members)
#             # print (members)
#             # members = json.dumps(members)
#             return [member.json for member in member_all]
#         elif type == "projects":
#             history = COEP_API_History(operation="Read All Projects Info")
#             db.session.add(history)
#             db.session.commit()
#             projects =[]
#             project_all = COEP_Projects.query.all()
#             for project in project_all:
#                 project = project.json()
#                 projects.append(project)
#             # members = jsonify(members)
#             # print (members)
#             historys = json.dumps(projects)
#             return f"{projects}"
#         elif type == "historys":
#             historys =[]
#             history_all = COEP_API_History.query.all()
#             for history in history_all:
#                 history = history.json()
#                 historys.append(history)
#             # members = jsonify(members)
#             # print (members)
#             historys = json.dumps(historys)
#             return f"{historys}"
#         else:
#             history = COEP_API_History(operation="Tried Reading Info But Bad Request")
#             db.session.add(history)
#             db.session.commit()
#             return "Bad Request", 404

api.add_resource(COEP_Member, '/member_json/<int:mis>')
api.add_resource(COEP_Project, '/project_json/<string:projectName>')
# api.add_resource(COEP_Members_Json, '/<string:type>_json')

if __name__ == "__main__":
    app.run(debug=True)


