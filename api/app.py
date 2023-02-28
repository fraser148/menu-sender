from flask import Flask, request

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "Hello World!"

app.run(debug=True)