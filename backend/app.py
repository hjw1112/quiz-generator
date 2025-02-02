from flask import Flask, session, redirect, url_for, render_template
from backend.routes.route import routes
from dotenv import load_dotenv
import os
from random import random

# create the flask app
app = Flask(
    __name__,
    template_folder="../frontend/template",
    static_folder="../frontend/static"
)

app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.register_blueprint(routes)


app.config['UPLOAD_FOLDER'] = 'uploads'


if __name__ == "__main__":
    app.run(debug=True)

#ngrok http --url=lobster-alert-cleanly.ngrok-free.app 5000