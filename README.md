
# README.md

## API de Biblioteca

Esta API sirve para administrar los prestamos de una biblioteca. Se pueden ver todos los libros disponibles, que usuarios tienen prestamos activos, crear nuevos libros y realizar prestamos.

### Configuración del Entorno

#### Requisitos Previos
- Python 3.x
- Django y Django Rest Framework
- Una base de datos Postgress funcionando.
- Un cliente API como Postman o cURL

#### Instalación y Ejecución
1. Clona el repositorio del proyecto.
2. Crea y activa el venv
3. Crear base datos "biblioteca_test"
4. crear usuario "bibliotecaAdmin" con password "123456".
5. Instala las dependencias: `pip install -r requirements.txt`.
6. cd Scripts
7. Prepara las migraciones: `python manage.py makemigrations`
8. Realiza las migraciones: `python manage.py migrate`.
9. Inicia el servidor: `python manage.py runserver`.
10. Insertar los dummy datas con el comando `python manage.py create_dummy_data.py`

### Autenticación

#### Obtener token basico
- **Endpoint**: `api/tokenBasico/`
- **Método**: POST
- **Cuerpo de la Solicitud**: `{"username": "juan", "password": "123456"}`
- **Respuesta**: `{"token": "token generado"}`.

#### Uso del Token basico
Agrega el token a la cabecera de tus solicitudes para acceder a los endpoints protegidos:
```
Authorization: Token <tu_token>
```
#### Obtener JWT
- **Endpoint**: `api/tokenJWT/`
- **Método**: POST
- **Cuerpo de la Solicitud**: `{"username": "juan", "password": "123456"}`
- **Respuesta**: `{"access": "token generado"}`.

#### Uso del Token basico
Agrega el token a la cabecera de tus solicitudes para acceder a los endpoints protegidos:
```
Authorization: Bearer <tu_token>
```

### Endpoints

#### Libros

##### Listar Libros
- **Endpoint**: `libros/todos/`
- **Método**: GET
- **Queryparam**: page
- **Permisos**: Cualquiera
- **Repuesta**: Lista de todos los libros disponibles

##### Detalles de Libro
- **Endpoint**: `libros/<int:pk>/`
- **Método**: GET
- **Permisos**: Cualquiera
- **Repuesta**: Detalles de un libro. Los campos son titulo, autor, genero, año de publicacion y estado de disponibilidad.

##### Crear/actualizar un Libro
- **Endpoint crear**: `libros/crear/`
- **Endpoint actualiar**: `libros/crear/<int:pk>`
- **Método**: POST, PUT
- **Cuerpo de la Solicitud**: `{"titulo": "El señor de los anillos", "autor": "Tolkien", "genero": "Fantasia", "year_publication": "1954-06-01"}`
- **Permisos**: Administrador

#### Prestamo

##### Listar libros prestados por usuario
- **Endpoint**: `prestamo/usuario/<int:pk>`
- **Método**: GET
- **Permisos**: Cualquiera
- **Repuesta**: Lista de libros con estado activo que tiene un usuario.

##### Crear prestamo
- **Endpoint**: `prestamo/crear/`
- **Método**: POST
- **Cuerpo de la Solicitud**: `{"libro": 600}`
- **Permisos**: Usuario normal
- **Nota**: El id del usuario se obtiene del token.


### Realizar Pruebas
Ejecutar el comando: `py manage.py test`.
Se adjunta la coleccion del postman para realizar las pruebas. Para token basicos usar el prefijo Token y para JWT utilizar bearer.
