# Practica2
práctica 2 de ARSO
## COMANDOS AL INICIO DE LA PRÁCTICA
Sudo usermod –a –G lxd $USER
Newgrp lxd
Lxd init –auto
Cat pfinal2.py 
## EXPLICACIÓN DEL DOCUMENTO PFINAL2.PY
Logging.error  es un módulo que funciona como un print, solo que nos permite filtrar según los niveles de interés del mensaje (debug, info, warning, error and critical). Este nos permite mantenernos constantemente informados sobre los procesos que se están ejecutando en nuestro programa junto a los posibles fallos que pueda llegar a tener. 
### Create
Init --> crea la instancia de un contenedor Linux
Network --> configuramos para cada bridge la dirección ip de cada subred en el protocolo de red IPv4
Set eth0 --> asignamos a la(s) tarjeta(s) de conexión de red de cada contenedor un bridge con una dirección ip 
### Configure
Db --> ejecutamos el “-apt update” para actualizar __?__ y luego descargamos el código de mongodb para poder almacenar datos en con un tipo de base de datos no relacional
Servidores --> pasamos el fichero install.sh al contenedor + Chmod +x --> cambia los permisos de acceso a un fichero (en este caso añade un permiso de fichero ejecutable) + ejecutamos su código, donde tenemos un update y una descarga de los ficheros en la carpeta app que también hemos transferido al contenedor (con un push). Ahí están todos los documentos necesarios para el correcto funcionamiento de la aplicación, además de hacer un dump de todos los pacientes semilla a la base de datos ya configurada.
Balanceador (lb) --> ejecutamos el “-apt update” para actualizar __?__ y luego descargamos el código de la aplicación haproxy que se encargará de redirigir todo el tráfico de peticiones HTTP a los servidores. Al modificar el documento de haproxy.cfg estamos especificando que en el puerto 8001 están conectados los puertos 8000 de cada servidor, diferenciables por su dirección IP. 
### Start
Start --> arranca un contenedor linux
Forever --> ejecuta de manera indefinida el código del documento rest_server.js que le hace estar escuchando constantemente a posibles solicitudes remotas.
service haproxy start --> inicializamos la aplicación haproxy en el contenedor de balanceador
### Delete
Delete --> elimina las instancias de contenedores Linux (una vez parados)
### List
List --> listea los contenedores mostrados 
### Pause
Stop <%> --force --> para de ejecutar un contenedor
### Pauseone

## COMANDOS PARA COMPROBAR EL FUNCIONAMIENTO DE LA APLICACIÓN WEB DESPLEGADA
Curl lb
while true; do curl 134.3.1.10; sleep 0.1; done

## DOCKER
Cp --> copiamos el fichero de virtualbox descargado en el centro de cálculo a una carpeta de nuestro disco físico (para no estar todo el rato accediendo al centro de cálculo cada vez que ejecutemos dicho programa). 
Virtualbox --> importamos la imagen de una máquina virtual que alojaremos en una carpeta del disco (físico). Ejecutamos la máquina virtual Ubuntu, dentro del terminal podemos ejecutar comandos docker
Docker Pull Ubuntu --> importamos una imagen de Ubuntu 
Docker images / curl -XGET --unix-socket /run/docker.sock http://localhost/images/json --> listar imagines importadas (la última es una consulta HTTP al servidor dockerd, que es lo que hace el cliente docker cunado ejecutamos el comando docker images)
Docker ps / curl -XGET --unix-socket /run/docker.sock http://localhost/containers/json --> listar contenedores docker corriendo o 
