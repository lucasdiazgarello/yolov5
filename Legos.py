import subprocess
import sys
import subprocess
import csv
import re

import detect as det


def detectar(user,dire):
    det.run(user=user,source=dire)


def comparar(direccion, bloquesactuales):
    compatible = True

    #print(direccion)
    bloques = contar(direccion)
    print(bloques)
    print(bloquesactuales)
    for n in range(len(bloquesactuales)):
        #print("bloques actuales"+bloquesactuales[n])
        #print("bloques " + bloques[n])
        if cantidad(bloquesactuales[n]) < cantidad(bloques[n]):
            compatible = False

    return compatible


# print(det.x)
def contar(direccion):
    results = ["0 detectadas","0 detectadas","0 detectadas","0 detectadas","0 detectadas","0 detectadas","0 detectadas","0 detectadas","0 detectadas","0 detectadas"]
    if"static/static/" in direccion:
        direccion.replace('static/static/','static/')
    print(direccion)
    with open(direccion, "r") as f:
        for row in csv.reader(f):
            for i in range(len(row)):
                print(row[i])

                if "T1 BLACK" in row[i]:
                     results[0]=row[i]
                if "T2 BLACK" in row[i]:
                     results[1] = row[i]
                if "T1 WHITE" in row[i]:
                     results[2] = row[i]
                if "T2 WHITE" in row[i]:
                     results[3] = row[i]
                if "T1 RED" in row[i]:
                     results[4] = row[i]
                if "T2 RED" in row[i]:
                     results[5] = row[i]
                if "T1 BLUE" in row[i]:
                     results[6] = row[i]
                if "T2 BLUE" in row[i]:
                     results[7] = row[i]
                if "T1 YELLOW" in row[i]:
                     results[8] = row[i]
                if "T2 YELLOW" in row[i]:
                     results[9] = row[i]
    return results



def cantidad(string):
    # if re.match("[0-9]", string[0]):
    #      print("entre al sano")
    #      cantidad = int(re.match("^ *[0-9]+", string).group())
    # else:
    #     string.replace("[","")
    #     cantidad = int(re.match("^ *[0-9]+", string).group())
    string2=string.replace("[","")
    print(string)
    print(string2)
    string3=string2.replace("'","")
    print(string3)
    cantidad = int(re.match("^ *[0-9]+", string3).group())
    return cantidad


 #ja=contar()

#print(cantidad(" 17 T1 Black"))
# black white red blue yellow

# proc = subprocess.Popen(['/home/ldiaz/Desktop/Custom/Mio/yolov5/detect.py','detect',  ''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)#
# print (proc.communicate()[0])
# Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])

# s2_out = subprocess.check_output([sys.executable, "detect.py"])
# print(s2_out)
