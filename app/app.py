from flask import Flask, render_template, request
import sqlite3 as sql


app = Flask(__name__)


class Student(object):
    def __init__(self, idnum, firstname, midname,lastname, gender, course, yearlevel):
        self.idNum = idnum
        self.fstName = firstname
        self.midName = midname
        self.lstName = lastname()
        self.gender = gender
        self.course = course
        self.yrLevel = yearlevel


class Course(object):
    def __init__(self, courseid, coursedesc):
        self.courseid = courseid
        self.coursedesc= coursedesc


conn = sql.connect('dbTest.db')
conn.execute("CREATE TABLE IF NOT EXISTS courses(course_id TEXT PRIMARY KEY, coursedesc TEXT)")
cur =  conn.cursor()

conn.execute('CREATE TABLE IF NOT EXISTS studInfo(idno TEXT PRIMARY KEY , firstn TEXT, midname TEXT,lastn TEXT, gnder TEXT, crse TEXT, yrlevel TEXT, FOREIGN KEY(crse) REFERENCES courses(course_id))')
conn.execute("CREATE VIEW IF NOT EXISTS joinedInfo AS SELECT course_id, idno, firstn, midname,lastn, gnder, coursedesc, yrlevel FROM studInfo CROSS JOIN courses WHERE courses.course_id = studInfo.crse")

conn.close()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/managestud')
def managestud():
    return render_template('managestud.html')


@app.route('/managecourse')
def managecourse():
    return render_template('managecourse.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    return render_template("add_Student.html")


@app.route('/addStudent', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        try:
            print 'zzzzz'
            idNo = request.form['idNo']
            print idNo
            firstName = request.form['firstName']
            midName = request.form['middName']
            lastName = request.form['lastName']
            gender = request.form['gender']
            course = request.form['course']
            yrLevel = request.form['yrLevel']
            print course
            stud = Student(idNo,firstName,midName,lastName,gender,course, yrLevel)
            with sql.connect('dbTest.db') as conn:

                cur = conn.cursor()
                print "we have connnection"
                cur.execute("INSERT INTO studInfo(idno,firstn,midname,lastn,gnder,crse, yrlevel)VALUES(?,?,?,?,?,?,?)",
                (stud.idNum, stud.fstName,stud.midName, stud.lstName,stud.gender,stud.course, stud.yrLevel))
                print "were connected"
                conn.commit()
                mem = "Student added successfully"

        except:
            mem = "error"

        finally:
            conn = sql.connect('dbTest.db')
            conn.row_factory= sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM studInfo")
            rows = cur.fetchall()
            return render_template('upResult.html',rows= rows,mem=mem)




@app.route("/show")
def show_list():
    with sql.connect("dbTest.db") as conn:
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM studInfo")
        rows = cur.fetchall()
        return render_template("database.html", rows=rows)


@app.route('/update/', methods=['POST', 'GET'])
def update():
    conn = sql.connect('dbTest.db')
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM studInfo")
    rows=  cur.fetchall()
    return render_template("update.html", rows = rows)

@app.route('/updateStud', methods =['POST', 'GET'])
def update_stud():
    if request.method == "POST":
        try:
            idno = request.form['idNo']
            print ' id accepted'
            with sql.connect('dbTest.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM studInfo")
                for row in cur.fetchall():
                    if row[0] == idno:
                        print row
                        copied = row
                        mem = "Student found"
                        break
                    else:
                        mem = "Student not found"
                        copied = "  "

        except:
            mem = "Error"
            copied = " "
        finally:
            return render_template("fupdate.html", mem = mem, copied = copied)
            conn.close()


@app.route('/updating', methods=['POST','GET'])
def updating():
    if request.method =="POST":
        try:
            idNo = request.form['idNo']
            print idNo
            firstName = request.form['firstName']
            midName = request.form['middName']
            lastName = request.form['lastName']
            gender = request.form['gender']
            course = request.form['course']
            yrLevel = request.form['yrLevel']

            with sql.connect("dbTest.db") as conn:
                cur = conn.cursor()
                print 'print me'
                cur.execute("SELECT * FROM studInfo")
                for row in cur.fetchall():
                    print row
                    if row[0] == idNo:
                        print 'HELLO'
                        cur.execute("UPDATE studInfo SET firstn = ?, midname = ?, lastn = ?, gnder = ?, crse = ?, yrlevel = ? where idno = ?",
                             (firstName, midName, lastName, gender, course,yrLevel,idNo))
                        conn.commit()
                        mem = "UPDATED!"
                        break


        except:
            mem = "UPDATE FAILED"
        finally:
            conn = sql.connect("dbTest.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM studInfo")
            rows = cur.fetchall()
            return render_template("upResult.html", rows=rows, mem=mem)
            conn.close()


@app.route('/delete')
def delete():
    conn = sql.connect("dbTest.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM studInfo")
    rows = cur.fetchall()
    conn.close()
    return render_template("delete.html", rows=rows)


@app.route('/delStud', methods=['POST', 'GET'])
def delete_stud():
    if request.method == 'POST':
        if request.method == "POST":
            try:
                idNo = request.form['idNo']
                print idNo
                with sql.connect("dbTest.db") as conn:
                    print "connected"
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM studInfo")
                    for row in cur.fetchall():
                        print row
                        if row[0] == idNo:
                            print 'halo'
                            cur.execute("DELETE FROM studInfo WHERE idno = ?", (idNo,))
                            conn.commit()
                            mem = "Successfully Deleted"
                            break
                        else:
                            mem = "STUDENT NOT FOUND"
            except:
                mem = "DELETING FAIL"
            finally:
                conn = sql.connect("dbTest.db")
                conn.row_factory = sql.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM studInfo")
                rows = cur.fetchall()
                return render_template("upResult.html", rows=rows, mem=mem)
            conn.close()


@app.route("/CourseTable")
def CourseTable():
    conn = sql.connect("dbTest.db")

    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM joinedInfo")
    rows = cur.fetchall()
    conn.close()

    return render_template("fusion.html", rows=rows)

@app.route('/search')
def search():
    return render_template("search.html")

@app.route("/searching",methods = ['POST', 'GET'])
def searching():
    if request.method == "POST":
        try :
            target = request.form["target"]
            print target
            with sql.connect('dbTest.db') as conn:
                cur = conn.cursor()
                print 'sulod ples'
                cur.execute("SELECT * FROM joinedInfo where course_id = ? or firstn = ? "
                    "or coursedesc=? or lastn=? or midname=? or idno = ? or gnder=? or yrlevel=?",
                    (target, target, target, target, target, target, target, target))
                tab = cur.fetchall()
                print tab
                mem = "Exist"
        except:
            tab = "Empty"
            mem = "Error"
        finally:
            print tab
            return render_template("searchres.html", mem=mem, tab=tab)



@app.route('/addcourse', methods=['POST', 'GET'])
def addcourse():
    return render_template("addcourse.html")


@app.route('/courseadd', methods=['POST', 'GET'])
def add_course():
    if request.method == 'POST':
        print "post ka? "
        try:
            print 'zzzzz'
            courseid = request.form['courseID']
            print courseid
            coursedesc = request.form['courseDesc']

            course = Course(courseid, coursedesc)
            with sql.connect('dbTest.db') as conn:
                cur = conn.cursor()
                print "we have connnection"
                cur.execute("INSERT INTO courses(course_id, coursedesc)VALUES(?,?)",(course.courseid,course.coursedesc))
                conn.commit()

                print "courses connected"
                conn.commit()
                mem = "Course added successfully"

        except:
            mem = "error"

        finally:
            conn = sql.connect('dbTest.db')
            conn.row_factory= sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            return render_template('addc.html',rows= rows,mem=mem)




@app.route("/showcourse")
def show_course():
    with sql.connect("dbTest.db") as conn:
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses")
        rows = cur.fetchall()
        return render_template("databasec.html", rows=rows)


@app.route('/updatecourse/', methods=['POST', 'GET'])
def updatec():
    conn = sql.connect('dbTest.db')
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    rows=  cur.fetchall()
    return render_template("updatecourse.html", rows = rows)

@app.route('/updcourse', methods =['POST', 'GET'])
def update_course():
    if request.method == "POST":
        try:
            courseid = request.form['courseid']
            print ' id accepted'
            with sql.connect('dbTest.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                for row in cur.fetchall():
                    if row[0] == courseid:
                        print row
                        copied = row
                        mem = "Course found"
                        break
                    else:
                        mem = "Course not found"
                        copied = "  "

        except:
            mem = "Error"
            copied = " "
        finally:
            return render_template("fupdatec.html", mem = mem, copied = copied)
            conn.close()


@app.route('/updatingcourse', methods=['POST','GET'])
def updatingcourse():
    if request.method =="POST":
        try:
            courseid = request.form['courseid']
            print courseid
            coursedes = request.form['coursedesc']


            with sql.connect("dbTest.db") as conn:
                cur = conn.cursor()
                print 'print me'
                cur.execute("SELECT * FROM courses")
                for row in cur.fetchall():
                    print row
                    if row[0] == courseid:
                        print 'HELLO'
                        cur.execute("UPDATE courses SET coursedesc = ? where course_id = ?",(coursedes, courseid))
                        conn.commit()
                        mem = "UPDATED!"
                        break


        except:
            mem = "UPDATE FAILED"
        finally:
            conn = sql.connect("dbTest.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            return render_template("addc.html", rows=rows, mem=mem)
            conn.close()


@app.route('/deletecourse')
def deletecourse():
    conn = sql.connect("dbTest.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    conn.close()
    return render_template("deletecourse.html", rows=rows)


@app.route('/delCourse', methods=['POST', 'GET'])
def delete_course():
    if request.method == "POST":
        try:
            courseid = request.form['courseid']
            print courseid
            with sql.connect("dbTest.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                for row in cur.fetchall():
                    print row
                    if row[0] == courseid:
                        cur.execute("DELETE FROM courses WHERE course_id = ?", (courseid,))
                        conn.commit()
                        mem = "Successfully Deleted"
                        break
                    else:
                        mem = "COURSE NOT FOUND"
        except:
            mem = "DELETING FAIL"
        finally:
            conn = sql.connect("dbTest.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            return render_template("addc.html", rows=rows, mem=mem)
        conn.close()



if __name__ == "__main__":
    app.run(debug=True)