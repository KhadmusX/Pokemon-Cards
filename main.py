from flask import Flask
from db import initDb
import card

app = Flask(__name__)
app.register_blueprint(card.public)

if __name__ == "__main__":
    initDb()
    app.run(debug=True)

