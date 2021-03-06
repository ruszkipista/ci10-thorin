import os
import json
from flask import Flask, render_template, request, flash
if os.path.exists("env.py"):
    import env

# name of the application module or package (="__main__")
# where should Flask look for templates and static files
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_FLASH_KEY")

@app.route("/")  # trigger point through webserver: "/"= root directory
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    with open("./data/company.json", "r", encoding="UTF-8") as json_data:
        data = json.load(json_data)
    return render_template("about.html", page_title="About", page_url=request.path, company=data)

@app.route("/about/<member_url>")
def member(member_url):
    with open("./data/company.json", "r", encoding="UTF-8") as json_data:
        data = json.load(json_data)
        member_data = list(filter(lambda x: x['url']==member_url, data))
    return render_template("member.html", member=member_data[0])

@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        flash(f"Thanks {request.form.get('name')}, we have received your message!")

    return render_template("contact.html", page_title="Contact")

@app.route("/careers")
def careers():
    return render_template("careers.html", page_title="Careers")    

# script runs as main, not as imported code
if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_IP", "0.0.0.0"),  #get value or use given default
        port=int(os.environ.get("PORT", "443")),#get value or use given default
        # allow debugging, only for development phase
        debug = True if os.environ.get("FLASK_DEBUG", '').lower() == 'true' else False)