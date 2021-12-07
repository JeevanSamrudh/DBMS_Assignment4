from io import RawIOBase
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

detail = ""
result = ""

app = Flask(__name__)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

#print(db['mysql_db'])

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    global result
    result = ""
    if request.method == 'POST':
        global detail
        detail = request.form['user']
        return redirect('/homepage')
    else:
        return render_template("login.html")

@app.route('/homepage',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        var = request.form["tables"]
        return redirect('/{0}'.format(var))
    if detail == "Public":
        return render_template("homepage_public.html")
    if detail == "FIA":
        return render_template("homepage_fia.html",result=result)

@app.route('/<variable>',methods=['GET','POST'])
def open_pages(variable):
    det = []
    cur = mysql.connection.cursor()
    if variable == 'drivers':
        cur.execute("SELECT * from new_record")
        det = list(cur.fetchall())
        #print("det:",det)
        cur.execute("SHOW COLUMNS FROM new_record")
        col = cur.fetchall()
        column = tuple([i[0] for i in col])
        #print("col:",col)
        det.insert(0,column)
    if variable == 'constructors':
        cur.execute("select * from new_constructor")
        det = list(cur.fetchall())
        #print("det:",det)
        cur.execute("SHOW COLUMNS FROM new_constructor")
        col = cur.fetchall()
        column = tuple([i[0] for i in col])
        #print("col:",col)
        det.insert(0,column)
    if variable == 'wdc':
        cur.execute("select * from new_wdc")
        det = list(cur.fetchall())
        #print("det:",det)
        cur.execute("SHOW COLUMNS FROM new_wdc")
        col = cur.fetchall()
        column = tuple([i[0] for i in col])
        #print("col:",col)
        det.insert(0,column)
    if variable == 'engine_manufacturer':
        cur.execute("select * from engine_manufacturer")
        det = list(cur.fetchall())
        #print("det:",det)
        cur.execute("SHOW COLUMNS FROM engine_manufacturer")
        col = cur.fetchall()
        column = tuple([i[0] for i in col])
        #print("col:",col)
        det.insert(0,column)
    if variable == 'wcc':
        cur.execute("select * from new_wcc")
        det = list(cur.fetchall())
        #print("det:",det)
        cur.execute("SHOW COLUMNS FROM new_wcc")
        col = cur.fetchall()
        column = tuple([i[0] for i in col])
        #print("col:",col)
        det.insert(0,column)
    if variable == 'employee':
        cur.execute("select * from new_employee")
        det = list(cur.fetchall())
        #print("det:",det)
        cur.execute("SHOW COLUMNS FROM new_employee")
        col = cur.fetchall()
        column = tuple([i[0] for i in col])
        #print("col:",col)
        det.insert(0,column)
    if variable == "edit":
        if request.method == "GET":
            return render_template("edit.html")
        if request.method == "POST":
            script_sql= request.form['command']
            try:
                global result
                result = ""
                cur.execute(script_sql)
                #cur.commit()
                result = "Edit Successful."
            except:
                result = "Incorrect Command. Database rolled back."
            #return script_sql
            return redirect('/homepage')
    if variable == 'race_starts':
        code =  """ 
                start transaction;
                update driver_stats set d_starts = d_starts + 1; 
                update new_record set d_starts = d_starts + 1;
                commit;
                """
        cur.execute(code)
        '''
        det = list(cur.fetchall())
        #print("det:",det)
        cur.execute("SHOW COLUMNS FROM new_record")
        col = cur.fetchall()
        column = tuple([i[0] for i in col])
        #print("col:",col)
        det.insert(0,column)
        '''
        result = "Races Incremented."
        return redirect('/homepage')
    return render_template("stats.html", result=det)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)