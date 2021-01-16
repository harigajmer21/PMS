from setting import *

# the class MovieLegacyapp will inherit the db.Model of SQLAlchemy
class Legacyapp(db.Model):
    __tablename__ = 'tbl_legacyapp'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    appname = db.Column(db.String(255), nullable=False)
    # nullable is false so the column can't be empty
    description = db.Column(db.String, nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def addlegacyapp(_appname, _description, _url):
        # creating an instance of our Movie constructor
        new_legacyapp = Legacyapp(appname=_appname, description=_description, url=_url)
        db.session.add(new_legacyapp)  # add new movie to database session
        db.session.commit()  # commit changes to session

    def get_all_legacyapp():
        '''function to get all movies in our database'''
        return [Legacyapp.json(legacyapp) for legacyapp in Legacyapp.query.all()]
    

    def json(self):
        return {'id': self.id, 'appname': self.appname,
                'description': self.description, 'url': self.url}
        # this method we are defining will convert our output to json



class UserApp(db.Model):
    __tablename__ = 'tbl_userapp'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    username = db.Column(db.String(255), nullable=False)
    # nullable is false so the column can't be empty
    password = db.Column(db.String(255), nullable=False)

    def adduserapp(_username, _password):
        new_user = UserApp(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()
    
    def get_all_users():
        '''function to get all user in our database'''
        return [UserApp.json(userapp) for userapp in UserApp.query.all()]
    
    def json(self):
        return {'id': self.id, 'username': self.username,
                'password': self.password}
        # this method we are defining will convert our output to json

db.create_all()


password_complexity ##Json file / csv
{
    isNumber: true,
    isUpperCase : true,
    islowerCase: true
}


