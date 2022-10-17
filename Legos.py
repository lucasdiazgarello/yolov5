import subprocess
import sys
import subprocess

import detect as det

#print(det.x)

#proc = subprocess.Popen(['detect.py',  ''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#print (proc.communicate()[0])


s2_out = subprocess.check_output([sys.executable, "detect.py"])
print(s2_out)
