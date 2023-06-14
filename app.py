from flask import Flask
from dotenv import load_dotenv
from api.views import api_bp
from payments.views import payments_bp
import os
import sys

# Add configuration for the application
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
app = Flask(__name__)
load_dotenv()

# Register Blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(payments_bp, url_prefix='/payments')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'), debug=os.environ["DEBUG"])