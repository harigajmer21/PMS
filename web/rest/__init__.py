# from flask import Blueprint
# from flask_restplus import Api
# from sqlalchemy.orm.exc import NoResultFound
# import config

# api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# api = Api(
#     app=api_blueprint,
#     version='1.0.0',
#     title='Password management system rest api',
#     description= ''' This serves as all th api request''',
#     contact="@harisharon",
#     contact_email="gajmehr.8@gamil.com"
# )

# @api.errorhandler
# def default_error_handler(e):
#     message = 'An unhandled exception occured.'

#     if not config.FLASK_DEBUG:
#         return {'message': message}, 500

# @api.errorhandler(NoResultFound)
# def db_not_found_error_handler(e):
#     return {'message': 'A database result was required but none was found.'}, 404