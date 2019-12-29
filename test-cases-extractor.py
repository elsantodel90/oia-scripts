# Es python2.
# Funcionaba con una version vieeeeeja de cms, tal vez ya no funcione.
# Asi como esta, se dumpea TODOS los casos de TODOS los problemas que esten en la base (datos de conexion de la base hardcodeados)  

import psycopg2
import os
import errno

con = psycopg2.connect(database="cmsdb", user="cmsuser", password="cms", host="127.0.0.1", port="5432")

cur = con.cursor()
cur.execute("SELECT num, task_id, input, output from task_testcases")
rows = cur.fetchall()

for num, task_id, inpu, oupu in rows:
    cur = con.cursor()
    cur.execute("SELECT name from tasks where id = %s", [task_id])
    taskname = cur.fetchall()[0][0]
    print taskname, num
    try:
		os.mkdir(taskname)
    except OSError as e:
		if e.errno != errno.EEXIST:
			raise
    cur = con.cursor()
    cur.execute("SELECT loid from fsobjects where digest = %s", [inpu])
    lo = con.lobject(cur.fetchall()[0][0])  
    lo.export("{}/caso{:03}.in".format(taskname, num))

    cur = con.cursor()
    cur.execute("SELECT loid from fsobjects where digest = %s", [oupu])
    lo = con.lobject(cur.fetchall()[0][0])  
    lo.export("{}/caso{:03}.dat".format(taskname, num))


print("Operation done successfully")
con.close()
