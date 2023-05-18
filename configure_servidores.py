import sys
import subprocess
import logging
import pickle

nom_imagen = "image_server"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
	vm = sys.argv[1]
	ip = sys.argv[2]
	
	with open("numero.txt", "rb") as fich:
		numero = pickle.load(fich)
	with open("ip_db.txt", "rb") as ipdb:
		ip = pickle.load(ipdb)
		
	#determinar el ip de la DB en app
	lines = list()
	with open("/home/c.mbarros/Práctica_2/app/md-seed-config.js", "r+") as fichero:
		lines = fichero.readlines()
		lines[3-1]="const mongoURL = process.env.MONGO_URL || 'mongodb://"+ip+":27017/bio_bbdd';\n"
	fichero.close()
	with open("/home/c.mbarros/Práctica_2/app/md-seed-config.js", "w") as files:
		files.writelines(lines)
	files.close()
	with open("/home/c.mbarros/Práctica_2/app/rest_server.js", "r+") as fichero:
		lines = fichero.readlines()
		lines[12-1]="    await mongoose.connect('mongodb://"+ip+"/bio_bbdd',{ useNewUrlParser: true, useUnifiedTopology: true })\n"
	with open("/home/c.mbarros/Práctica_2/app/rest_server.js", "w") as files:
		files.writelines(lines)

	#configuración de servidores
	for i in range(int(numero)):
		nombre = vm + str(i)
		subprocess.run(["lxc", "start", nombre])		
		subprocess.run(["lxc", "file", "push", "install.sh", nombre+"/root/install.sh"])
		subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "install.sh"])
		subprocess.run(["lxc", "file", "push", "-r", "app", nombre+"/root"])
		subprocess.run(["lxc", "exec", nombre, "--", "./install.sh"])
		subprocess.run(["lxc", "restart", nombre])
		subprocess.run(["lxc", "stop", nombre])
		
	#subprocess.run(["python3", "crear.py", vm, "1"])
	#subprocess.run(["python3", "networkconfig.py", vm, "1"])
	#nombre = vm + str(0)
	#subprocess.run(["lxc", "start", nombre])		
	#subprocess.run(["lxc", "file", "push", "install.sh", nombre+"/root/install.sh"])
	#subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "install.sh"])
	#subprocess.run(["lxc", "file", "push", "-r", "app", nombre+"/root"])
	#subprocess.run(["lxc", "exec", nombre, "--", "./install.sh"])
	#subprocess.run(["lxc", "restart", nombre])
	#subprocess.run(["lxc", "publish", nombre, "--alias", nom_imagen])
	#subprocess.run(["python3", "crear.py", s, nom_imagen, numero])
	#subprocess.run(["python3", "networkconfig.py", s, numero, ip1])
	
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
