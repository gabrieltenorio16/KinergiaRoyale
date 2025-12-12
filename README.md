# Nombre de proyecto y breve descripcion.
KinergiaRoyale es un proyecto destinado para el uso docente y educacional para los alumnos de Kinesiologia de la Universidad Catolica Del Norte. 
La funcion que tiene esta plataforma es la de brindar un experiencia educativa, en la cual los estudiantes podran realizar consultas clinicas simulando casos de la vida real.
# Integrantes y roles.
Los integrantes del equipo con sus respectivos roles son los siguientes:
- Gabriel Tenorio (Rol: Product Owner)
- Jorge Aguilar
- Manuel Rey (Rol: Scrum Master)
- Danitza Ogas
- Valentina Carvajal
- Benjamin Moyano
- Cristopher Meza

# Instrucciones de instalacion y ejecucion.
Cómo levantar el proyecto con Docker (paso a paso)
Requisitos previos
Antes de empezar, asegúrate de tener instalado:

Docker Desktop (Windows/Mac) o Docker Engine + Docker Compose (Linux).
En Windows, Docker Desktop suele pedir:

Nota: Si se encuentra en windows, debe dejar minimizada la aplicación de Docker Desktop

1. Clonar el repositorio y entrar a la carpeta correcta

Debe descargar el archivo de codigo (.zip) y extraerlo para que se muestre la carpeta del proyecto

Luego, debe ubicarse a la altura de los archivos Docker que están dentro de Proyecto_KineAPP, puede entrar desde cmd:

cd Proyecto_KineAPP
En esa carpeta están:

docker-compose.yml → define los servicios (web y db).
Dockerfile → define cómo construir la imagen del proyecto Django.
2. (Opcional) Limpiar contenedores y base anterior
Si ya habías levantado el proyecto antes y quieres empezar “desde cero”:

docker compose down -v
Qué hace esto:

down: detiene y elimina los contenedores.
-v: elimina también el volumen postgres_data (o sea, borra la base de datos guardada).
Úsalo solo si quieres resetear la DB.
Si no quieres borrar la DB, usa solo:

docker compose down

3. Construir la imagen del proyecto
Esto instala las dependencias del requirements.txt dentro de la imagen:

docker compose build

Notas:

La primera vez puede tardar varios minutos.
Si cambias requirements.txt, debes volver a ejecutar este paso.
4. Levantar el servidor y la base de datos
Arranca todo:

docker compose up -d

Qué pasa aquí:

Se levanta PostgreSQL en el servicio db.
Se levanta Django en el servicio web.
-d significa que corre en segundo plano.
Si quieres ver los logs en vivo (útil si algo falla), ejecútalo sin -d:

docker compose up

5. Crear tablas en la base (migraciones) (en una terminal distinta)
Como la DB es nueva la primera vez, hay que aplicar migraciones:

docker compose run --rm web python manage.py makemigrations
docker compose run --rm web python manage.py migrate

6. Crear un superusuario (admin)
Necesario para entrar al panel /admin:

docker compose run --rm web python manage.py createsuperuser
Sigue los pasos que te pide (usuario, correo y contraseña).

7. Abrir el proyecto
Con todo levantado:

Sitio principal:
http://localhost:8000/
Panel admin:
http://localhost:8000/admin
Si el navegador no carga:

