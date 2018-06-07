# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager, Crud


# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
auth.define_tables(username=True)
service = Service()
plugins = PluginManager()
crud = Crud(db)


# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
########################################

from datetime import datetime
import datetime
db.define_table('delito',
    Field('ingrese_tipo_delito',requires=IS_NOT_EMPTY(error_message='ingrese el nuevo tipo de delito')),
     format='%(ingrese_tipo_delito)s')
db.define_table('dependencias_polciales',
    Field('ingrese_nueva_dependencia_policial',requires=IS_NOT_EMPTY(error_message='ingrese la nueva dependencia policial')),
    Field('capacidad_calabozo','integer'),

    format='%(ingrese_nueva_dependencia_policial)s')
    
db.define_table('dependencias_organismos',
    Field('ingrese_nueva_dependencia_judicial',requires=IS_NOT_EMPTY(error_message='ingrese el nuevo organismo judicial')),
    format='%(ingrese_nueva_dependencia_judicial)s')
   


db.define_table('deteni2',
    Field('foto','upload'),

    Field('foto_cuerpo','upload'),
    Field('foto_perfil','upload'),  
    Field('foto_perfil2','upload',),
    Field('tatu_cicatriz','upload',),
    Field('tatu_cicatriz2','upload'),
    Field('tatu_cicatriz3','upload',),  
    Field('tatu_cicatriz4','upload'),
    Field('tatu_cicatriz5','upload'),
    Field('tatu_cicatriz6','upload'),

    Field('detalle_tatu','text'),


    Field('dni','integer',length=12,label="ingrese el dni"),
    Field('apellido','string',requires = IS_LOWER()),
   
    Field('nombre','string',length=30,requires = IS_LOWER()),
    Field('aliass','string',length=30,requires = IS_LOWER()),
    Field('sexo',requires = IS_IN_SET(['Masculino','Femenino'])),
    
    Field('fecha_naci','date',("%d/%m/%Y")),
        
    Field('edad','integer',length=3,writable=False),
    Field('altura','float',label="Ingrese La Altura ej:1.85",widget=SQLFORM.widgets.double.widget),#para que nodeje poner letras
    Field('color_piel',requires = IS_IN_SET(['negro','trigueño','blanco','amarillo'])),
    Field('color_pelo',requires = IS_IN_SET(['negro','rubio','peli rojo','sin cabello','blanco'])),
    Field('tipo_pelo',requires = IS_IN_SET(['sin cabello','corto','largo'])),
    Field('nacionalidad','string',length=30),
    Field('provincia','string',length=30,requires = IS_LOWER()),
    Field('departamento','string',length=30,requires = IS_LOWER()),
    Field('domicilio','string',length=30,requires = IS_LOWER()),
    Field('padre','string',requires = IS_LOWER()),
    Field('madre','string',requires = IS_LOWER()),
    Field('pareja','string',requires = IS_LOWER()),
    Field('hijos','string',requires = IS_LOWER()),
    





    
    
    Field('comentario','text',label='delito al q se dedica'),
    format='%(apellido)s,%(nombre)s,%(dni)s')






    

                                                                                
    
db.define_table('ingreso',
    Field('persona','reference deteni2',writable=False,requires = IS_EMPTY_OR(IS_DATE())),
    Field('apellido','string',requires = IS_LOWER(),writable=False),
    Field('nombre','string',length=30,requires = IS_LOWER(),writable=False),

    Field('comisaria','reference dependencias_polciales'),
    Field('organismos','reference dependencias_organismos',label="ingrese el organismo judicial"),
    Field('delitos','reference delito'),
    Field('comentario','text',requires = IS_LOWER()), 
    
    Field('calidad',requires=IS_IN_SET(['ARRESTADO_A_A','ARRESTADO_A_H','APRENDIDO','DEMORADO','DETENIDO','LIBERTAD','TRASLADO'])),
    Field('comentarios','text',requires = IS_LOWER() ),
    Field('trasladado','reference dependencias_polciales'),
    
    Field('horario','datetime')
    )
    
db.define_table('historial',
    Field('persona','reference deteni2', writable=False,requires = IS_EMPTY_OR(IS_DATE())),
    Field('comisaria','reference dependencias_polciales'),
    Field('organismos','reference dependencias_organismos',label="ingrese el organismo judicial"),
         
    Field('delitos','reference delito'),
    Field('comentario','text'), 
    
    Field('calidad',requires=IS_IN_SET(['ARRESTADO','DETENIDO','LIBERTAD','TRASLADO'])),
    Field('trasladado','reference dependencias_polciales'),
    Field('comentarios','text'), 
    
    Field('horario','datetime')
     
    )
    

        


db.dependencias_polciales.requires=IS_IN_DB(db,'dependencias_polciales','%(descripcion)s')
db.ingreso.trasladado.requires=IS_IN_DB(db,'dependencias_polciales','%(ingrese_nueva_dependencia_policial)s')
db.dependencias_organismos.requires=IS_IN_DB(db,'dependencias_organismos','%(descripcion)s')
db.delito.requires=IS_IN_DB(db,'delito','%(delito)s')
db.ingreso.persona.requires = IS_IN_DB(db, db.deteni2, '%(apellido)s,%(nombre)s,%(dni)s')



    
    
    
