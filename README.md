# Instalación de repositorio para trabajo de desarrollo

Tutorial de adecuación de entorno de desarrollo para proyecto BodaKaos Ingeniería de Software IIi

## Requerimientos de instalación
  - Python 3.6+
  - Windows/Linux

## Pasos de instalación
  - Instalación Python 3.6+
  - Instalación pip
  - Instalación virtualenv 
  - Generación de entorno virtual con virtualenv
  - Activación de entorno virtual
  - Clonación de repositorio
  - Instalación de requerimientos del repositorio
  - Cambiar de rama del repositorio al respectivo modulo
  - Ejecución de proyecto

### Instalación Python 3.6+
##### Windows
  - Descargar instalador y ejecutador como administrador de la [página oficial](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe)
##### Linux (Ubuntu 16.04 LTS+)
Linux ya trae por defecto una instalación de Python3

### Instalación pip
##### Windows
Al instalar Python3, pip viene instalado, se puede comprobar ejecutando:
```sh
$ python -m pip
```
  
##### Linux (Ubuntu 16.04 LTS+)
  - Ingresar a terminar
  - Ejecutar los siguientes comandos con permisos de superusuario
```sh
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev libpq-dev
```
- Se puede validar la instalación ejecutando el siguiente comando
```sh
$ pip -h
```

### Instalación virtualenv
##### Windows
- Ejecutar el siguiente comando con permisos de superusuario:
```sh
$ python -m pip install --upgrade pip
$ python -m pip install virtualenv
```
  
##### Linux (Ubuntu 16.04 LTS+)
  - Ingresar a terminar
  - Ejecutar los siguientes comandos con permisos de superusuario
```sh
$ sudo -H pip install --upgrade pip
$ sudo -H pip install virtualenv
```


### Generación de entorno virtual con virtualenv
##### Windows/Linux
  - Ingresar a terminar
  - Ejecutar el siguiente comando:
```sh
$ virtualenv <nombre_del_entorno>
```

### Activación de entorno virtual
##### Windows
- Ejecutar los siguientes comandos
```sh
$ cd path/to/environment
$ cd Scripts
$ activate
$ cd ..
```
- El resultado correcto será el siguiente:
```sh
(nombre_del_entorno) $ 
```
  
##### Linux (Ubuntu 16.04 LTS+)
  - Ingresar a terminar
  - Ejecutar los siguientes comandos
```sh
$ cd path/to/environment
$ source bin/activate
```
- El resultado correcto será el siguiente:
```sh
(nombre_del_entorno) $ 
```

### Clonación de repositorio
  - Ingresar a terminar
  - Ejecutar los siguientes comandos (El repositorio quedará descargado dentro de la carpeta _site_
```sh
$ cd path/to/environment
$ git clone https://github.com/SeekingAura/ingesoft3Boda.git site
```

### Instalación de requerimientos del repositorio
  - Ingresar a terminar
  - Ejecutar los siguientes comandos
```sh
$ cd path/to/environment
$ <Activar entorno virtual>
(nombre_del_entorno) $ cd site
(nombre_del_entorno) $ pip install -r requirements.txt
```

### Cambiar de rama del repositorio al respectivo modulo
  - Ingresar a terminar
  - Ejecutar los siguientes comandos
```sh
$ cd path/to/environment
$ <Activar entorno virtual>
(nombre_del_entorno) $ cd site
(nombre_del_entorno) $ git branch
(nombre_del_entorno) $ git checkout <branch_name>
```

- _git branch__ permite revisar la rama en la que se encuentra el repositorio
- _git checkout <branch_name>_ cambia la rama en la cual se encuentra el repositorio, las ramas que se encuentran activas son:
-- master
-- Pareja
-- Fiesta
-- LunaMiel
-- Ceremonia

### Ejecución de proyecto
  - Ingresar a terminar
  - Ejecutar los siguientes comandos
```sh
$ cd path/to/environment
$ <Activar entorno virtual>
(nombre_del_entorno) $ cd site
(nombre_del_entorno) $ cd BodaKaoz
(nombre_del_entorno) $ python manage.py runserver
```

El resultado correcto de este comando será de la siguiente forma:
```sh
(nombre_del_entorno) $ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
Django version 2.0.4, using settings 'BodaKaoz.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### License
----

MIT