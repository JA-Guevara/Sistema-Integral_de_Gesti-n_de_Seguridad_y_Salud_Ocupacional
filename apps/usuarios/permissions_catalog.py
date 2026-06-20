"""Catálogo de permisos del sistema, agrupados por módulo.

Es la única fuente de verdad de los permisos "de negocio". A partir de
esta lista:
  1) `models.ControlAcceso.Meta.permissions` declara los permisos nativos
     de Django (auth.Permission) que se crean al migrar.
  2) El formulario de roles los muestra agrupados por módulo (Ver/Gestionar).

Convención de codename: <accion>_<modulo>  (ej. 'gestionar_usuarios').
El permiso completo se usa como 'usuarios.<codename>' (app_label 'usuarios').
"""

PERMISSION_CATALOG = [
    {'codename': 'ver_usuarios',        'modulo': 'Usuarios',          'accion': 'Ver',       'descripcion': 'Ver usuarios'},
    {'codename': 'gestionar_usuarios',  'modulo': 'Usuarios',          'accion': 'Gestionar', 'descripcion': 'Crear, editar, activar y resetear usuarios'},

    {'codename': 'ver_roles',           'modulo': 'Roles y permisos',  'accion': 'Ver',       'descripcion': 'Ver roles'},
    {'codename': 'gestionar_roles',     'modulo': 'Roles y permisos',  'accion': 'Gestionar', 'descripcion': 'Crear, editar y activar roles'},

    {'codename': 'ver_trabajadores',       'modulo': 'Trabajadores',   'accion': 'Ver',       'descripcion': 'Ver trabajadores'},
    {'codename': 'gestionar_trabajadores', 'modulo': 'Trabajadores',   'accion': 'Gestionar', 'descripcion': 'Crear, editar y administrar trabajadores'},

    {'codename': 'ver_evaluaciones',       'modulo': 'Evaluaciones',   'accion': 'Ver',       'descripcion': 'Ver evaluaciones de competencias'},
    {'codename': 'gestionar_evaluaciones', 'modulo': 'Evaluaciones',   'accion': 'Gestionar', 'descripcion': 'Crear, asignar y calificar evaluaciones'},

    {'codename': 'ver_capacitaciones',       'modulo': 'Capacitaciones', 'accion': 'Ver',       'descripcion': 'Ver capacitaciones'},
    {'codename': 'gestionar_capacitaciones', 'modulo': 'Capacitaciones', 'accion': 'Gestionar', 'descripcion': 'Registrar, asignar y dar seguimiento a capacitaciones'},

    {'codename': 'ver_reportes',        'modulo': 'Reportes',          'accion': 'Ver',       'descripcion': 'Ver reportes de cumplimiento'},
    {'codename': 'gestionar_reportes',  'modulo': 'Reportes',          'accion': 'Gestionar', 'descripcion': 'Generar y exportar reportes en PDF'},

    {'codename': 'ver_bitacora',        'modulo': 'Bitácora',          'accion': 'Ver',       'descripcion': 'Consultar la bitácora del sistema'},
]

# Lista de codenames válidos (para filtrar permisos asignables).
CODENAMES = [item['codename'] for item in PERMISSION_CATALOG]
