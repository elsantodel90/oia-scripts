import psycopg2
import os
import sys

query = """SELECT submissions.id, username, tasks.name, loid , language
                   FROM fsobjects, files, submissions, participations, users, tasks 
                   WHERE files.submission_id = submissions.id 
                   AND   participations.contest_id = tasks.contest_id 
                   AND   participations.user_id = users.id 
                   AND   submissions.task_id = tasks.id 
                   AND   submissions.participation_id = participations.id
                   AND   fsobjects.digest = files.digest
                   AND   tasks.contest_id = %(contestId)s;
        """

def fullyCreateFile(filename):
        if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        return open(filename, "w")

def printHelp():
        def line(l):
                print >>sys.stderr, l
        line("Parameters:")
        line("contestId     : Entero con el contestId")
        line("outputDirname : Nombre del directorio donde se creara el output")

def parseParams():
        try:
                return {"contestId" : int(sys.argv[1]),
                        "outputDirname" : sys.argv[2]}
        except:
                printHelp()
                exit()
def run(contestId, outputDirname):
        try:
                conn=psycopg2.connect("dbname='cmsdb' user='cmsuser' host='localhost' password='oiadbpass'")
        except:
                print "I am unable to connect to the database."
                return
        cur = conn.cursor()
        cur.execute(query, {"contestId" : contestId})
        rows = cur.fetchall()
        cur.close()
        languageFileExtension = {
					"C++11 / g++" : "cpp",
					"Java / JDK" : "java",
			}
        for submissionId, username, taskName, loid, language in rows:
                filename = os.path.join(outputDirname, username, taskName, "{0}.{1}".format(submissionId, languageFileExtension[language]))
                print submissionId, username, taskName, loid,filename
                with fullyCreateFile(filename) as f:
                        lobject = conn.lobject(oid=loid, mode="r")
                        f.write(lobject.read())
                        lobject.close()

if __name__ == "__main__":
        run(**parseParams())


