from datetime import date
import json
from flask import Flask, render_template
import cds

app = Flask(__name__)

@app.route("/")
def landing_page():
    menu = cds.get_menu('lenoir', date.fromisoformat('2024-03-05'))
    data = json.dumps(menu, indent=4)
    return render_template("index.html", menu_data=data)
