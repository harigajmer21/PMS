from config import FLASK_DEBUG
from web import app

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)