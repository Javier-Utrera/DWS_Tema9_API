curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=javier&password=javier&client_id=mi_aplicacion&client_secret=mi_clave_secreta"

curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=cliente1&password=contraseña1&client_id=mi_aplicacion&client_secret=mi_clave_secreta"

curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=trabajador1&password=contraseña1&client_id=mi_aplicacion&client_secret=mi_clave_secreta"

curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=cliente4&password=contraseña1&client_id=mi_aplicacion&client_secret=mi_clave_secreta"

Descargar proyecto con GIT
sudo apt-get install python3-venv  -> Sino está instalado ya
No situamos en la carpeta 2daw
python3 -m venv myvenv -> Creamos el entorno
source myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate -> Creamos base de datos
python manage.py loaddata ITV/fixtures/data.json
python manage.py loaddata ITV/fixtures/datos2.json
python manage.py loaddata ITV/fixtures/oauth_fixture.json
python manage.py runserver 0.0.0.0:8080 -> Lanzamos el servidor

curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "javier", "password": "javier"}' \
  http://localhost:8000/api/token/

curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "cliente1", "password": "contraseña1"}' \
  http://localhost:8000/api/token/

curl \
-X POST \
-H "Content-Type: application/json" \
-d '{"username": "trabajador1", "password": "contraseña1"}' \
http://localhost:8000/api/token/

curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4MDU2Mjc2LCJpYXQiOjE3MzgwNTU5NzYsImp0aSI6ImE5ZTIxMzBhNGUwZTQ5NmQ5NmU3NjY5NDVmNTAxMjQ2IiwidXNlcl9pZCI6MTZ9.Ss3pYfIqH0EqkllMFaYjMUkCLXHgcSwcpoQEr5kSbb8" \
  http://localhost:8000/api/inspecciones/listar_inspecciones

curl -X POST http://127.0.0.1:8000/api/token/verify/ -d "token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5NzkzNDczLCJpYXQiOjE3MzgwNjU0NzMsImp0aSI6IjlkMTZhYTU2MDE5ZjQ2YzA5ZWQ5ZThhOTI1MTJmODJiIiwidXNlcl9pZCI6MTZ9.GR5XuBpzFXqldMfgIszUUE1tFalknf0BeI52mNfvPAE"

curl -X POST http://127.0.0.1:8000/api/token/verify/ -d "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5NzkzNDczLCJpYXQiOjE3MzgwNjU0NzMsImp0aSI6IjlkMTZhYTU2MDE5ZjQ2YzA5ZWQ5ZThhOTI1MTJmODJiIiwidXNlcl9pZCI6MTZ9.GR5XuBpzFXqldMfgIszUUE1tFalknf0BeI52mNfvPAE"

SECRET_KEY=s$14&p!shywfap)=@xqn&wpwu^8@v5-jjqufn2^l5#f@(t&g-&

