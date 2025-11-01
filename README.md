# Nombre de proyecto y breve descripcion.
KinergiaRoyale es un proyecto destinado para el uso docente y educacional para los alumnos de Kinesiologia de la Universidad Catolica Del Norte. 
La funcion que tiene esta plataforma es la de brindar un experiencia educativa, en la cual los estudiantes podran realizar consultas clinicas simulando casos de la vida real.
# ntegrantes y roles.
Los integrantes del equipo con sus respectivos roles son los siguientes:
⦁	Gabriel Tenorio (Rol: Product Owner)
⦁	Jorge Aguilar
⦁	Manuel Rey (Rol: Scrum Master)
⦁	Danitza Ogas
⦁	Valentina Carvajal
⦁	Benjamin Moyano
⦁	Cristopher Meza

# Instrucciones de instalacion y ejecucion.
Para poder usar esta plataforma, usted debe de tener instalados en su computador Django, Python, PostgreSQL, Pandas, Jazminn. Estos componentes son fundamentales para el correcto funcionamiento de la plataforma.
Ya con la carpeta descargada, usted debera crear primero su entorno dentro de la CMD de Windows:
1.	Seleccionar la ruta donde se encuentra ubicada la carpeta instalada, luego dentro del CMD colocar (ejemplo de ruta):
cd C:\Users\danit\Documents\Kinergia Royale (Carpeta de todo el proyecto)\KinergiaRoyale
2.	Luego de ingresar a la carpeta se debe crear el entorno, por lo que se debe colocar:
python -m venv entorno
3.	Al crear el entorno luego dentro de este se debe ingresar a los Scripts para luego activar el entorno:
cd Scripts
4.	Ya estando dentro de los Scripts se debe activar el entorno, por lo tanto solo debe escribir:
activate
5.	El entorno si esta correctamente activado aparecera al inicio, algo asi:
(entorno) C:\Users\danit\Documents\Kinergia Royale (Carpeta de todo el proyecto)\KinergiaRoyale\entorno\Scripts>
6.	Luego nos debemos devolver donde nos encontrabamos antes dentro de la carpeta que contiene nuestro README.md, esto se realiza con:
cd.. (repetir hasta llegar a la altura de KinergiaRoyale)
7.	Para poder verificar que es lo que se encuentra dentro de una carpeta debe colocar:
dir
8.	Luego de verificar que nos encontramos en la carpeta correcta, la cual contiene el archivo README.md se deben instalar los requerimientos, de esta forma:
pip install -r requirements.txt
9.	Al finalizar la instalacion, al colocar dir aparecera una lista con distintos nombres, para poder llegar al manage.py debemos ingresar al que dice Proyecto_KineAPP, esto se realiza de la siguiente forma:
cd Proyecto_KineAPP
10.	Ya dentro de esta carpeta nos encontramos con el archivo manage.py, para poder utilizarlo correctamente primero se deben generar las migraciones:
python manage.py makemigrations
11.	Luego de que se realice esto, se deben ejecutar los archivos de migracion con:
python manage.py migrate
12.	Ya con el entorno creado correctamente y los componentes requeridos instalados, debe escribir lo siguiente:
python manage.py runserver
13.	Al correrlo correctamente, se le generara un texto, en este se encuentra una direccion http://127.0.0.1:8000/, en la cual debe ingresar y verificar que django este funcionando correctamente
14.	Al verificar que Django se instalo y funciono exitosamente, debe modificar el http dentro de la misma pagina en google y agregarle /admin, por lo que quedaria asi:
127.0.0.1:8000/admin o ingresar a http://127.0.0.1:8000/admin
15.	Encontrandose ya dentro de la plataforma se debera poner su usuario y contrasena, los cuales provisionalmente son Usuario: admin y Contrasena: admin112233
