import subprocess
import sys
import subprocess
import csv
import detect as det


def detectar():
    det.run()


# print(det.x)
def contar():
    blancog = ""
    blancoc = ""
    amarillog = ""
    amarilloc = ""
    azulg = ""
    azulc = ""
    rojog = ""
    rojoc = ""
    negrog = ""
    negroc = ""
    results = ["0 DETECTADOS","0 DETECTADOS","0 DETECTADOS","0 DETECTADOS","0 DETECTADOS","0 DETECTADOS","0 DETECTADOS","0 DETECTADOS","0 DETECTADOS","0 DETECTADOS"]
    with open("datos.csv", "r") as f:
        for row in csv.reader(f):
            for i in range(len(row)):

                if "T1 BLACK" in row[i]:
                    results.pop(0)
                    results.insert(0,row[i])
                if "T2 BLACK" in row[i]:
                    results.pop(1)
                    results.insert(1,row[i])
                if "T1 WHITE" in row[i]:
                    results.pop(2)
                    results.insert(2,row[i])
                if "T2 WHITE" in row[i]:
                    results.pop(3)
                    results.insert(3,row[i])
                if "T1 RED" in row[i]:
                    results.pop(4)
                    results.insert(4, row[i])
                if "T2 RED" in row[i]:
                    results.pop(5)
                    results.insert(5, row[i])
                if "T1 BLUE" in row[i]:
                    results.pop(6)
                    results.insert(6,row[i])
                if "T2 BLUE" in row[i]:
                    results.pop(7)
                    results.insert(7, row[i])
                if "T1 YELLOW" in row[i]:
                    results.pop(8)
                    results.insert(8, row[i])
                if "T2 YELLOW" in row[i]:
                    results.pop(9)
                    results.insert(9, row[i])
    return results
    #print(results)

ja=contar()

#black white red blue yellow

# proc = subprocess.Popen(['/home/ldiaz/Desktop/Custom/Mio/yolov5/detect.py','detect',  ''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)#
# print (proc.communicate()[0])
# Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])

# s2_out = subprocess.check_output([sys.executable, "detect.py"])
# print(s2_out)
