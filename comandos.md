curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=javier&password=javier&client_id=mi_aplicacion&client_secret=mi_clave_secreta"

curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=cliente1&password=contraseña1&client_id=mi_aplicacion&client_secret=mi_clave_secreta"

curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=trabajador1&password=contraseña1&client_id=mi_aplicacion&client_secret=mi_clave_secreta"

Descargar proyecto con GIT
sudo apt-get install python3-venv  -> Sino está instalado ya
No situamos en la carpeta 2daw
python3 -m venv myvenv -> Creamos el entorno
source myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate -> Creamos base de datos
python manage.py runserver 0.0.0.0:8080 -> Lanzamos el servidor
