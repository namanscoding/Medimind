import sys
import scrapy
import json
import os
from subprocess import run


from flask import *
app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        global user_drug_name
        user_drug_name = request.form["Drug_name"]
        return redirect('/result')
    return render_template("home.html")


@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == "POST":
        user_drug_name = request.form["Drug_name"]
    drug_name=user_drug_name
    str1="https://go.drugbank.com/unearth/q?searcher=drugs&query="+drug_name    
    command=f'scrapy crawl drug -a start_urls="{str1}" --nolog'
    curr_dir =os.getcwd()
    os.chdir("./tutorial/tutorial/")
    os.system(command)
    with open('C://Users//U6071514//OneDrive - Clarivate Analytics//Desktop//drug_api_flask_db//tutorial//tutorial//db.json','r') as openfile:
        json_object=json.load(openfile)
    output = json_object
    print("\n\n data--", output)
    os.chdir(curr_dir)
    return jsonify(output)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=105)