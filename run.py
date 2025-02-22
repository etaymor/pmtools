from app import create_app
from config.settings import FLASK_DEBUG, FLASK_PORT

app = create_app()

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT) 