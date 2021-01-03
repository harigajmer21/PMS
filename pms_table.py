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

    
    def json(self):
        return {'id': self.id, 'appname': self.appname,
                'description': self.description, 'url': self.url}
        # this method we are defining will convert our output to json




db.create_all()
