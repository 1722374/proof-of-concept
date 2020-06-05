import subprocess
import os
#Starte die main.batch
cwd = os.getcwd()
#Working Directory wechseln
os.chdir(r'{}\Batch_Files'.format(cwd))
batch_dir = r'\Batch_Files\main.bat'

complete_path = f'{cwd}{batch_dir}'
print("Komplett: " + complete_path)
subprocess.call([complete_path])