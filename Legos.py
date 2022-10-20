import subprocess
import sys
import subprocess

import detect as det


def detectar():
    det.run()
# print(det.x)
 def contar():
     results = []
     with open("datos.txt", "r") as f:
         for line in f:
             results.append(line.strip().split(','))
             return results

# proc = subprocess.Popen(['/home/ldiaz/Desktop/Custom/Mio/yolov5/detect.py','detect',  ''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)#
# print (proc.communicate()[0])
# Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])

# s2_out = subprocess.check_output([sys.executable, "detect.py"])
# print(s2_out)
