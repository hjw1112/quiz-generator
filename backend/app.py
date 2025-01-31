from flask import Flask, session, redirect, url_for, render_template
from backend.route import routes
from dotenv import load_dotenv
import os


# create the flask app
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.register_blueprint(routes)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route('/')
def landing():
    if "token_info" in session:
        return redirect(url_for("routes.index"))
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)


app.run("0.0.0.0")


#ngrok http --url=lobster-alert-cleanly.ngrok-free.app 5000