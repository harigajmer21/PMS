from setting import *
from pms_table import Legacyapp, UserApp

from password.password import Password

# route to add new movie
@app.route('/addlegacyapp', methods=['POST'])
def add_legacy_app():
    '''Function to add new legacyapp to our database'''
    request_data = request.get_json()  # getting data from client
    Legacyapp.addlegacyapp(request_data["appname"], request_data["description"],
                    request_data["url"])
    response = Response("Success! New Legacy Application added", 201, mimetype='application/json')
    return response

# route to get all movies
@app.route('/get_legacy_app', methods=['GET'])
def get_legacy_app_list():
    '''Function to get all the get_legacy_app in the database'''
    return jsonify({'Get Legacy Application List': Legacyapp.get_all_legacyapp()})



# route to add new movie
@app.route('/adduserapp', methods=['POST'])
def add_user_app():
    '''Function to add new legacyapp to our database'''
    request_data = request.get_json()  # getting data from client
    UserApp.adduserapp(request_data["username"], request_data["password"])
    response = Response("Success! New added user", 201, mimetype='application/json')
    return response

# route to get all movies
@app.route('/get_user_app', methods=['GET'])
def get_user_app_list():
    '''Function to get all the get_legacy_app in the database'''
    return jsonify({'Get all user List': UserApp.get_all_users()})

@app.route('/add_new_password', methods=['POST'])
def create_password():
    request_data = request.get_json()
    password = request_data['password']
    response_complexity = Password.password_complexity(password)
    response_hibp  = Password.hibp(password)
    response_encrypt = Password.encrypt(password)

    if response_complexity is False:
        print("Not pass")
        return False
    elif response_hibp is False:
        print("not pass")
        return False
    else:
        ##Save the database
        


if __name__ == "__main__":
    app.run(debug=True)