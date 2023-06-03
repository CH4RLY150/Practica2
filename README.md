# Practica2
práctica 2 de ARSO

## COMANDOS AL INICIO DE LA PRÁCTICA
Sudo usermod –a –G lxd $USER

Newgrp lxd

Lxd init –auto

Cat pfinal2.py 
## EXPLICACIÓN DEL DOCUMENTO PFINAL2.PY
Logging.error --> es un módulo que funciona como un print, solo que nos permite filtrar según los niveles de interés del mensaje (debug, info, warning, error and critical). A partir de los logs estamos constantemente informados sobre los procesos que se están ejecutando en nuestro programa junto a los posibles fallos que pueda llegar a tener. 
### Create
Init --> crea la instancia de un contenedor Linux

Network --> configuramos para cada bridge la dirección ip de cada subred en el protocolo de red IPv4

The bridge network type allows to create a virtual L2 Ethernet switch that connects the instances that use it together into a single network L2 segment. Bridges created by LXD are managed, which means that in addition to creating the bridge interface itself, LXD also sets up a local dnsmasq process to provide DHCP, IPv6 route announcements and DNS services to the network.

Set eth0 --> asignamos a la(s) tarjeta(s) de conexión de red de cada contenedor un bridge con una dirección ip 
### Configure
Db --> ejecutamos el “-apt update” que busca actualizaciones del SO y luego descargamos el código de mongodb para poder almacenar datos en con un tipo de base de datos no relacional
Servidores --> pasamos el fichero install.sh al contenedor + Chmod +x --> cambia los permisos de acceso a un fichero (en este caso añade un permiso de fichero ejecutable) + ejecutamos su código, donde tenemos un update y una descarga de los ficheros en la carpeta app que también hemos transferido al contenedor (con un push). Ahí están todos los documentos necesarios para el correcto funcionamiento de la aplicación, además de hacer un dump de todos los pacientes semilla a la base de datos ya configurada.

Balanceador (lb) --> ejecutamos el “-apt update” que busca actualizaciones del SO y luego descargamos el código de la aplicación haproxy que se encargará de proporcionarnos un punto único de entrada de peticiones a la aplicación, además de redirigir todo el tráfico de peticiones HTTP de manera efectiva entre los servidores. Al modificar el documento de haproxy.cfg estamos especificando que en el puerto 8001 (preestablecido por el código de la "app") están conectados los puertos 8000 de cada servidor, diferenciables por su dirección IP. 
### Configure Remoto 
Hay una función definida en un fichero "ipremoto.py", que nos dice cúal es la IP de un ordenador del laboratorio a partir de su puesto de laboratorio (por ejemplo "ipremoto.guess_ip("l212")")

configuración de acceso remoto a servicios desplegados mediante lxd en un ordenador ajeno.

   	#db$ ip addr show
	
	#db$ lxc config set core.https_address IP-B:8443
	
	#db$ lxc config set core.trust_password mypass
Todo esto está resumido en un programa dentro del fichero "remoto.py", que podemos ejecutar mediante el comando "python3 remoto.py lb mypass", donde lb puede ser "l212" y mypass puede ser "contraseña", con eso ya tendríamos configurado el acceso remoto al programa LXD en el computador "lb" (NO OLVIDAR EJECUTAR LOS COMANDOS INICIALES DE USERRMOD, NEWGRP Y INIT).

	Ordenador_Principal$ lxc config set core.https address :8443 --> configura la dirección y puerto de acceso remoto al servidor LXD

	Ordenador_Principal$ lxc config set core.trust password mypass --> define contraseña de acceso

	Ordenador_Principal$ lxc remote add remotodb IP-B:8443 --password mypass --accept-certificate --> Acreditarse en el sistema remoto que ejecuta el servicio LXD del equipo lB

	Ordenador_Principal$ lxc network set remoto:lxdbr0 ipv4.address 134.3.0.1/24

	Ordenador_Principal$ lxc network set remoto:lxdbr0 ipv4.nat true --> Configurar un bridge remoto

Después a partir del remoto conseguimos crear, actualizar y configurar nuestro contenedor db, además de añadirle un proxy (asociación de "138.4.31.132:27017" = dirección máquina física, en este caso lB, a "138.3.0.20:27017" = dirección contenedor db) para que todas las consultas que lleguen al puerto 27017 de la máquina física remota sean redirigidos al contenedor db.

	Ordenador_Remoto$ lxc config device add remotodb:db miproxy proxy listen=tcp:IP_B:27017 connect=tcp:ip_db:27017
### Start
Start --> arranca un contenedor linux

Forever --> ejecuta de manera indefinida el código del documento rest_server.js que le hace estar escuchando constantemente a posibles solicitudes remotas.

service haproxy start --> inicializamos la aplicación haproxy en el contenedor de balanceador
### Delete
Delete --> elimina las instancias de contenedores Linux (una vez parados)
### List
List --> listea los contenedores mostrados 
### Pause
Stop <%nombre de contenedor%> --force --> para de ejecutar todos los contenedores creados
### Pauseone
Stop <%nombre de contenedor%> --force --> para de ejecutar un contenedor especificado en la consulta inicial
## COMANDOS PARA COMPROBAR EL FUNCIONAMIENTO DE LA APLICACIÓN WEB DESPLEGADA
Curl lb --> se trata de un interprete de comandos que soporta diferentes protocolos, simulando las acciones de un usuario en un navegador web (en este caso es una petición al balanceador)

while true; do curl 134.3.1.10; sleep 0.1; done --> es un bucle en el que se realizan consultas al balanceador constantemente

curl -v http://134.3.1.10:8001 --> petición HTTP a una URL

## DOCKER
Cp --> copiamos el fichero de virtualbox descargado en el centro de cálculo a una carpeta de nuestro disco físico (para no estar todo el rato accediendo al centro de cálculo cada vez que ejecutemos dicho programa).

Virtualbox --> importamos la imagen de una máquina virtual que alojaremos en una carpeta del disco (físico). Ejecutamos la máquina virtual Ubuntu, dentro del terminal podemos ejecutar comandos docker

Docker images / curl -XGET --unix-socket /run/docker.sock http://localhost/images/json --> listar imagines importadas (la última es una consulta HTTP al servidor dockerd con interfaz API-REST, que es lo que hace el cliente docker cuando ejecutamos el comando docker images, solo que este hace una representación más "limpia" del json que recibe)

Docker ps / curl -XGET --unix-socket /run/docker.sock http://localhost/containers/json --> listar contenedores docker corriendo 

generamos en una carpeta de una de las máquinas virtuales del virtualbox un DOCKERFILE (imagen de un contenedor Docker con cada una de las acciones que debe realizar el dockerdemon al geenerar un contenedor docker), y donde en nuestro caso debe estar descargado el código fuente de la aplicación a desplegar...

	FROM openjdk:8 --> indica la imagen de la que partimos para generar el contenedor docker
	
	RUN mkdir -p /root/ARSO-lab72/es/upm/dit/arso/lab2 --> especificamos la carpeta en la que se va a desplegar nuestra aplicación (si no existe se crea)
	
	COPY Application.java /root/ARSO-lab72/es/upm/dit/arso/lab2/Application.java --> copiamos el código fuente de nuestra aplicación en la dirección de destino especificada
	
	EXPOSE 8000 --> asignamos el puerto 8000 de nuestra máquina a nuestro contenedor para estar esuchando las posibles peticiones que le lleguen a la aplicacion web
	
	5 WORKDIR /root/ARSO-lab72 --> fijamos una carpeta de trabajo (carpeta donde se despliega toda la aplicación)
	
	RUN javac es/upm/dit/arso/lab2/Application.java --> compilamos el código del documento de nuestra aplicación 
	
	ENTRYPOINT java es.upm.dit.arso.lab2.Application --> cuando se cree el contenedor de docker se debe ejecutar por defecto el código de la aplicación

docker build -t imagenarso . --> Desde la misma carpeta donde hemos guardado todo (DockerFile y Application.java) creamos la imagen 

docker swarm init --> inicializamos el cluster encargado de la distribución de carga entre las replicas del stack que vamos a generar

docker stack deploy -c docker-compose.yml apparso --> desplegamos el stack (conjunto de replicas de una imagen, que está especificada en el documento docker-compose.yml), que nos permite atender a todas las consultas posibles distribuyendo dicho tráfico entre un número de replicas (viene determinada en el código del docker-compose.yml). Al final le asignamos un nombre al stack = "apparso".

código de configuración del stack en el fichero docker.compose.yml:
	version: "3"
	
	services:
	
		servicioarso1:
		
			image: imagenarso:latest
			
			deploy:
			
				replicas: 5
				
				resources:
				
					limits:
					
						cpus: "0.1"
						
						memory: 50M
						
				restart_policy:
				
					condition: on-failure
					
			ports:
			
				- "8000:8000" --> creamos y arrancamos un contenedor Dockerdemon (estamos especificando que el puerto 8000 del contenedor se asocie/resuelva al puerto 8000 de la máquina física)
				
			networks:
			
				- webnet
				
	networks:
	
	webnet:
	
Esto que hay especificado en el documento docker.compose.yml es lo mismo qe hacer 5 veces seguidas --> docker run -it --rm -p 8000:8000 imagenarso

Para cerrarlo todo tendríamos que: "$docker stack rm apparso" y "docker swarm leave --force"

Aunque, en vez de haberlo hecho por medio de un SWARM y un STACK, podríamos haber ejecutado en la misma carpeta que el docker.compose.yml el comando de "$docker-compose up", que en base al fichero mencionado antes despliega una apliación con varios servicios relacionados sobre un sistema de servidores docker. Luego para cerrarlo tendríamos que hacer: "$docker-compose down"
