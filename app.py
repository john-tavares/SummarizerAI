from flask import Flask
from dotenv import load_dotenv
from api.views import api_bp
import os

app = Flask(__name__)
load_dotenv()

# Register Blueprints
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'), debug=os.environ["DEBUG"])