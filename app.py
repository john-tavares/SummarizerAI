from flask import Flask
from dotenv import load_dotenv
from api.views import api_bp
import os

app = Flask(__name__)
load_dotenv()

# Register Blueprints
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=os.environ["DEBUG"])