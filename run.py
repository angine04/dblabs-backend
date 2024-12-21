import logging
from app import create_app

# Enable CORS debugging
logging.getLogger('flask_cors').level = logging.DEBUG

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)