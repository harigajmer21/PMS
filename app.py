from setting import *
from pms_table import Legacyapp

# route to add new movie
@app.route('/addlegacyapp', methods=['POST'])
def add_legacy_app():
    '''Function to add new legacyapp to our database'''
    request_data = request.get_json()  # getting data from client
    Legacyapp.addlegacyapp(request_data["appname"], request_data["description"],
                    request_data["url"])
    response = Response("Success! New Legacy Application added", 201, mimetype='application/json')
    return response



if __name__ == "__main__":
    app.run(debug=True)