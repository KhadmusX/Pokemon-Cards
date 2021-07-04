from flask import Flask
from db import initDb
import card, os

app = Flask(__name__)
app.register_blueprint(card.public)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    initDb()
    app.run(host='0.0.0.0', port=port, debug = True)

