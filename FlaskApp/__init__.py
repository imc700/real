from flask import Flask
app = Flask(__name__)

import FlaskApp.app
try:
    import sae
    import FlaskApp.sae_py
except:
    print("no in sae.")