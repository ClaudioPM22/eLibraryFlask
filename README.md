# API RESTful de microservicios para una E-Library

### Funcionalidades Clave:
  - Autenticación con JWT (JSON Web Tokens).
  - Búsqueda avanzada con filtros.
  - Sistema de préstamos con fechas de vencimiento.
  - Documentación automatizada con Swagger/OpenAPI.


### Reglas de negocio:

#### Para los prestamos:
  - Un libro solo puede prestarse su su estado es "ACTIVE".
  - Un usuario no puede tener más de 3 libros prestados.
  - Los prestamos son persistentes, solo se cambia la fecha de devolución por la fecha donde se devolvio y el libro debe volver a estar "ACTIVE"
  - El sistema calcula la fecha de entrega en función del número de paginas que posea el libro.

#### Para los usuarios:
  - No pueden existir dos usuarios con el mismo correo ni nombre de usuario.

#### Para los libros:
  - No se puede eliminar un libro si tiene prestamos activos