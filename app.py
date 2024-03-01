from flask import Flask, render_template, request, redirect

import pymysql as p

def getconnect():
    return p.connect (host="localhost", user="root", password="", database="demo")


def getdata():
    db = getconnect()
    cr = db.cursor()

    sql ="select username, password from demouser"
    cr.execute(sql)
    data = cr.fetchall()

    db.commit()
    db.close()
    return data

def insertdata(t):
    db = getconnect()
    cr = db.cursor()

    sql = "insert into demouser (username,email,password) values (%s, %s, %s)"
    cr.execute(sql, t)
    

    db.commit()
    db.close()





#=========================== Flask =======================================================

app = Flask(__name__)

@app.route("/")
def login():
	return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register")
def signup():
	return render_template("signup.html")

@app.route("/insertrec", methods=["POST"])
def signingup():
    usernm = request.form["uname"]
    email = request.form["email"]
    pasw = request.form["pin"]
    
    t = (usernm, email, pasw)
    insertdata(t)
    return render_template("login.html")

@app.route("/validateuser", methods=["POST"])
def valid_user():
    usern = request.form["uname"]
    passw = request.form["pin"]

    data = (usern, passw)
    database = getdata()

    if(data in database):
        return render_template("home.html")
    else:
        return render_template("signup.html")
    
@app.route("/flowers")
def flwrs():
    photos = ["himalayanabelia.jpg","okra.jpg","SweetHibiscus.jpg","sikkimfir.jpg","showyrosarypea.jpg","stickyindianmallow.jpg","Acacia_auriculiformis.jpeg","HickoryWattle.jpg"]
    import csv
    csv_file_path = 'flowers1.csv'
    data_list = []
    with open(csv_file_path, 'r', encoding="UTF-8") as file:
          csv_reader = csv.reader(file)
          for row in csv_reader:
               data_list.append(row)
        
    d = data_list[1:200]
    return render_template("that.html", da = d,ph = photos )

@app.route("/plants")
def plnt():
    import pandas as pd
    d_list = []
    data = pd.read_excel(io="C:/Users/hally/OneDrive/Desktop/python programms/demo/wikiplant_final edited.xlsx")
    cname = data["Names_Common_name"].iloc[:50].tolist()
    scname = data["Name"].iloc[:50].tolist()
    fam = data["Taxon_Family"].iloc[:50].tolist()
    desc = data["Plant_Descr"].iloc[:50].tolist()
    hab = data["Habitat"].iloc[:50].tolist()
    return render_template("plants.html", cnm = cname, scnm = scname, fm = fam, des = desc, hb = hab)

@app.route("/shop")
def shp():
    return render_template("shop.html")

if (__name__=="__main__"):
	app.run(debug=True)
