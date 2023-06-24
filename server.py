from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from views import app
from model import connect_to_db



app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
app.debug = True
 
connect_to_db(app)


toolbar = DebugToolbarExtension(app)
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)