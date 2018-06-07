

def index():
    return dict()
def mostrar():
    return locals()    
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def consulta1():
   
    form=SQLFORM.factory(Field('dni','integer',length=12,requires=IS_NOT_EMPTY()))
    if form.accepts(request.vars,session):
        response.flash="formulario  aceptado"
        redirect(URL('proceso_consul1', args=[form.vars.dni]))
    elif form.errors:
            response.flash="formulario inválido"
    else:
        response.flash="por favor complete el formulario"
    return dict(form=form) 
 


def proceso_consul1():
    atrapa = request.args[0]
    
    consulta = (db.deteni2.dni==atrapa)
    miset = db(consulta)
    registros = miset.select()
    




    a = miset.count() 

    if a == 0:
         redirect(URL('sin_dni', args=[atrapa]))
    



    return dict(a=a, atrapa=atrapa, registros=registros)

    
def proceso_consul2():
    #atrapo el id
    id_detenido = request.args[0]
    atrapa = request.args[1]
   



    
    consulta = (db.deteni2.dni==atrapa)
    miset = db(consulta)
    registros = miset.select()
    for i in registros:
        print i.id
    
    crud.settings.update_next = URL(f='proceso_consul1', args=[atrapa])
    
    form = crud.update(db.deteni2, id_detenido) #esto me permite  modificar un row pero antes hay importar un crud en db.py en gluon
    

    if form.accepts(request.vars,session):
        response.flash="formulario aceptado"

        redirect(URL('proceso_consul1', args=[form.vars.dni,request.args[1]]))
    
    


    return dict(atrapa=atrapa,consulta=consulta,registros=registros,miset=miset, form=form)
def sin_dni():
    atrapa= request.args[0]
 
    return dict(atrapa=atrapa)


                                        
                    

def deteni2():
    
    
    atrapa=request.args[0]
    #poner un valor por defecto a un campo del formulario
    db.deteni2.dni.default=request.args[0]

    form = SQLFORM(db.deteni2)

    
    
    
    


    
    
        
      
    if form.process().accepted:
        
    

       


      
      
      

        
        
        response.flash = 'Formulario Aceptado'
        #envio nombre apellido dni  y id
        redirect(URL(c='default', f='ingreso',args=[form.vars.id,form.vars.nombre,form.vars.apellido,form.vars.dni]))
    elif form.errors:
        response.flash = 'El formulario es inválido verifique'
    return dict(form=form,atrapa=atrapa,)



def ingreso():

    


    #atrapo el argumento id
    atrapa =request.args[0]
    #atrapo el nombre, apellido , dni
    atrapa_nombre=request.args[1]
    atrapa_apellido=request.args[2]
    atrapa_dni=request.args[3]
    consulta = (db.deteni2.id==atrapa)
    miset = db(consulta)
    registros = miset.select()
    i=registros

    # atrapo el nombre y apellido

    #atrapo el dia de hoy
    ed=datetime.date.today()
    edad=0
    
    

    #capturo la fecha de nacimiento
    for x in i:
        fecha=x.fecha_naci
    #calculo la edad
    edad=(ed.year)-(fecha.year)


    


    

    db.ingreso.persona.default = request.args[0] #-- Coloco el nombre de la agencia ya en el campo correspondiente
    db.ingreso.nombre.default = request.args[1]
    db.ingreso.apellido.default = request.args[2]


    
    form = SQLFORM(db.ingreso)
    c=form.vars.id
    
    form.add_button('agregar nuevos valores', URL('nuevas_dependencias',args=[atrapa]))
    #realizo la consulta del id de la persona para mandar la edad
    d=db(db.deteni2.id==atrapa).select().first()
    
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'

        

        #envio la edad a la persona
        d.update_record(edad=edad)
        #actualizo el ultimo registro


       
        db.historial.insert(persona=atrapa,comisaria=form.vars.comisaria,organismos=form.vars.organismos,delitos=form.vars.delitos,comentario=form.vars.comentario,calidad=form.vars.calidad,comentarios=form.vars.comentarios,trasladado=form.vars.trasladado,horario=form.vars.horario)
        
        
        redirect(URL(c='default', f='index'))



     


        
         
    
    
   






    
    return dict(form=form,ed=ed, atrapa=atrapa,miset=miset,registros=registros,consulta=consulta,i=i,x=x,fecha=fecha,edad=edad,d=d)




def nuevas_dependencias():
    

    
    atrapa=request.args[0]
   
    
    


        
    return dict(atrapa=atrapa)
def nueva_comisaria():
    form = SQLFORM(db.dependencias_polciales)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
        redirect(URL(c='default', f='index'))

        
    

    return dict(form=form)
def nueva_judicial():
    form = SQLFORM(db.dependencias_organismos)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
        redirect(URL(c='default', f='index'))


    return dict(form=form)
    
def nuevos_delitos():
    form = SQLFORM(db.delito)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
        redirect(URL(c='default', f='index'))
    return dict(form=form)




    



def nuevas_dep_pol():
    form = SQLFORM(db.dependencias_polciales)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
    elif form.errors:
        response.flash = 'El formulario es inválido verifique'
    return dict(form=form)

def nuevas_dep_judi():
    form = SQLFORM(db.dependencias_organismos)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
    elif form.errors:
        response.flash = 'El formulario es inválido verifique'
    return dict(form=form)
    
def nuevos_delitos():
    form = SQLFORM(db.delito)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
    elif form.errors:
        response.flash = 'El formulario es inválido verifique'
    return dict(form=form)

 






def proceso_consul3():
    atrapa = request.args[0]
    query=db(db.deteni2.dni==atrapa).select().first()
    
    consulta = (db.deteni2.dni==atrapa)
    miset = db(consulta)
    registros = miset.select()
    form=SQLFORM.grid(db.registros)
    




    a = miset.count() 
    if a == 0:

    
        redirect(URL('sin_dni', args=[atrapa]))
        
        



   

    return dict(query=query,miset=miset,a=a,consulta=consulta,atrapa=atrapa,registros=registros,grid=grid)




def sin2_dni():
    atrapa=request.args[0]
    redirect(URL('ingreso', args=[atrapa]))


    
    
        
  

       
   
     
 
   
    return dict(atrapa=atrapa) 

def consulta4():
   
       
     
                    
    return dict()

def consulta():
    fields=[db.ingreso.apellido,db.ingreso.nombre,db.ingreso.comisaria,db.ingreso.organismos,db.ingreso.trasladado]

    query=db((db.ingreso.calidad != "LIBERTAD")&(db.ingreso.trasladado!="7"))#&(db.ingreso.horario==hora_max))

    #row= db(db.deteni2.id==db.query.persona).select().first()
    db(db.ingreso)
    


   
   
    
                    

    


    grid = SQLFORM.grid(query,deletable=False,paginate=20,sortable=True,editable=False,csv=False,searchable=True,fields=fields,
    links=[lambda r: editar_expediente(r)])
   

    
    
    return locals()
def consulte():
    lid=[]
    lnom=[]
    lape=[]
    dicto={}

    b=0
    dato=db(db.deteni2.id>0).select()
    #for x in dato:
    # selecciono las id del campo persona y las meto detro de una lista
    reg=db(db.ingreso.calidad!="LIBERTAD").select()
    for i in reg:

        lid.append(i.persona)
        


    
       






   
    
   

        
    






        return dict(reg=reg,i=i,lid=lid,lape=lape,lnom=lnom,x=x)


   
     

    
    

        
    

   

def search_form(self,url): 
    form = FORM('',
    INPUT(_name='keywords',_value=request.get_vars.keywords, 
               _style='width:200px;', 
               _id='keywords'), 


         INPUT(_type='submit',_value=T('Search')), 
         INPUT(_type='submit',_value=T('Clear'),

         _onclick="jQuery('#keywords').val('');"), 
         _method="GET",_action=url) 
    return form 
def search_query(tableid,search_text,fields): 
    words= search_text.split(' ') if search_text else [] 
    query=tableid<0#empty query 
    for field in fields: 
        new_query=tableid>0 
        for word in words: 
            new_query=new_query&field.contains(word) 
        query=query|new_query 
    return query


def historial():
    

    
    
    fields=[db.deteni2.apellido,db.deteni2.nombre,db.deteni2.edad,db.deteni2.domicilio,db.historial.persona,db.historial.comisaria,db.historial.organismos,db.historial.delitos,db.historial.comentario,db.historial.calidad,db.historial.trasladado,db.historial.comentarios,db.historial.horario]
    grid = SQLFORM.smartgrid(db.deteni2, linked_tables=['historial'],
        
        fields=fields,
        deletable=False,    
        paginate=20,editable=False,
        create=False,
        csv=False,
        searchable=True,
        search_widget=search_form,
        user_signature=False,

       
        selectable=None,
        upload='<default>')
    # Cambiando la clase para el botón submit.
    if grid.element('input', _type='submit'):
        grid.element('input', _type='submit')['_class'] = 'btn btn-primary'
    
     
    return dict(grid = grid)


       
        
        



    

    
    

    
#agregar boton al grid
#creando el boton    
def editar_expediente(row):
        btn = A(I(_class='icon-thumbs-up'),
                    ' CAMBIAR ESTADO',
                    _href=URL(c='default', f='libertad', args=[row.id]),
                    _class='btn btn-primary')
        return btn     


  

def libertad():
     #atrapo argumento
    atrapa =request.args[0]

    #saco los datos para cargar los datos que necesito
    v = db(db.ingreso.id == atrapa).select(db.ingreso.ALL)
    for a in v: 
        p=a.persona
        c=a.comisaria
        o=a.organismos
        d=a.delitos
        co=a.comentario
        
        ca=a.calidad
        cos=a.comentarios
        
       
                  
   

        #cologo con valores rescatados en los campos del formulario
        db.ingreso.persona.default = p         #-- Coloco el nombre de la agencia ya en el campo correspondiente
        db.ingreso.comisaria.default = c
        db.ingreso.organismos.default = o
        db.ingreso.delitos.default = d
        db.ingreso.comentario.default= co
        
        db.ingreso.calidad.default = ca

        
        
           
            
    
    
  
   

    
    
    #re

    
    registro = db(db.ingreso.id==atrapa).select().first() or redirect(URL('index'))


   
   
    form=SQLFORM(db.ingreso,registro)

    


  



    z=db(db.ingreso.id==atrapa).select().first()
    
    
    
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'

        

        
        
        #z.update_record(comisaria=form.vars.comisaria,organismos=form.vars.organismos,comentario=form.vars.comentario,es=form.vars.es,calidad=form.vars.calidad,horario=form.vars.horario)
        
        db.historial.insert(persona=p,comisaria=form.vars.comisaria,
                            organismos=form.vars.organismos,
                            comentario=form.vars.comentario,
                            calidad=form.vars.calidad,
                            horario=form.vars.horario,
                            trasladado=form.vars.trasladado)
            
        
         


        redirect(URL('index'))

    

        
        
    elif form.errors:
        response.flash = 'El formulario es inválido verifique'   
                               
                 
                                  
         
    return dict(form=form,atrapa=atrapa,v=v,a=a,p=p,c=c,o=o,ca=ca,cos=cos,d=d,z=z,registro=registro)

def filtro1():
    
    
    variable_unica = ""
    color_piel= ""
    color_pelo= ""
    alias= ""
    ape=""
    nom=""
    adesde=""
    ahasta=""
    delito=""
   
    if request.get_vars['nom']:
        nom = request.get_vars['nom']
    if request.get_vars['ape']:
        ape = request.get_vars['ape']
    if request.get_vars['alias']:
        alias = request.get_vars['alias']
    if request.get_vars['variable_unica']:
        variable_unica = request.get_vars['variable_unica']
    if request.get_vars['color_piel']:
        color_piel = request.get_vars['color_piel']
    if request.get_vars['color_pelo']:  
        color_pelo = request.get_vars['color_pelo']
    if request.get_vars['adesde']:  
        adesde = request.get_vars['adesde']
        adesde =float(adesde)
    if request.get_vars['ahasta']:  
        ahasta = request.get_vars['ahasta']
      
    if request.get_vars['delito']:  
       delito = request.get_vars['delito']    

      
       
       
               
       
        




    form = ' '
    fields=[db.deteni2.nombre,db.deteni2.apellido,db.deteni2.foto]
    if (nom!="")|(ape!="")|(alias!="")|(variable_unica!="")|(color_piel!="")|(color_pelo!="")|(delito!=""):#|(adesde!="")|(ahasta!=""):

   
           
        form = SQLFORM.grid((db.deteni2.detalle_tatu.upper().like('%'+variable_unica+'%'))&(db.deteni2.color_piel.upper().like('%'+color_piel+'%'))&(db.deteni2.color_pelo.upper().like('%'+color_pelo+'%'))&(db.deteni2.aliass.upper().like('%'+alias+'%'))&(db.deteni2.apellido.upper().like('%'+ape+'%'))&(db.deteni2.nombre.upper().like('%'+nom+'%'))&(db.deteni2.comentario.upper().like('%'+delito+'%')),#&(db.deteni2.altura>=ahasta)&(db.deteni2.altura<=adesde),
            
        csv=False,
        create=False,
        searchable=False,
        editable=False,
        deletable=False,
        details=True,
        selectable=None,
               
        fields=fields)

    

    return dict(form=form, variable_unica=variable_unica,color_piel=color_piel,color_pelo=color_pelo,alias=alias,ape=ape,nom=nom,adesde=adesde,ahasta=ahasta,delito=delito)

    

    




        
    
    
   
    

    
    

    
    
    



