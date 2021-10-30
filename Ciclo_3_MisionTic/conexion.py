import sqlite3

database='/home/arussill/Ciclo_3_MisionTic/DB.db'

def conectar():
    con=sqlite3.connect(database)
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    return cur,con

#Consultar todos los registros de una tabla
#Consultar productos
def consultar(tabla):
    cur,con= conectar()
    sql="SELECT * FROM " + tabla
    cur.execute(sql)
    row=cur.fetchall()
    con.close()
    return row

# Consultar un producto
def consultarUno(tabla,cod):
    cur,con= conectar()
    sql="SELECT * FROM " + tabla + " WHERE codigo= ? "
    cur.execute(sql,[cod])
    row=cur.fetchone()
    con.close()
    return row

# Llevar los comentarios al template producto
def consultarVarios(tabla,cod):
    cur,con= conectar()
    sql="SELECT * FROM " + tabla + " WHERE producto= ? "
    cur.execute(sql,[cod])
    row=cur.fetchall()
    con.close()
    return row



# Consultar un usuario en login/val
def consultarDos(tabla,usu,contr):
    cur,con= conectar()
    sql="SELECT * FROM " + tabla + " WHERE nombre= ? and contra=? "
    cur.execute(sql,[usu,contr])
    row=cur.fetchone()
    con.close()
    return row

# Consultar un usuario en editar usuario
def consultarCuatro(tabla,usu):
    cur,con= conectar()
    sql="SELECT * FROM " + tabla + " WHERE nombre= ?"
    cur.execute(sql,[usu])
    row=cur.fetchone()
    con.close()
    return row

#Agregar comentario
def agregarComentario(usuario,producto,comentario,fecha):
    cur,con= conectar()
    sql="INSERT INTO comentarios (usuario,producto,comentario,fecha) VALUES(?,?,?,?)"
    cur.execute(sql,[usuario,producto,comentario,fecha])
    con.commit()
    con.close()


# Consultar lista de deseos
def consultarTres(tabla,usu,pro):
    cur,con= conectar()
    sql="SELECT * FROM " + tabla + " WHERE usuario= ? and producto=? "
    cur.execute(sql,[usu,pro])
    row=cur.fetchone()
    con.close()
    return row

#Agregar listadeseos
def agregarlistadeseos(usuario,producto):
    cur,con= conectar()
    sql="INSERT INTO lista_deseos (usuario,producto) VALUES(?,?)"
    cur.execute(sql,[usuario,producto])
    con.commit()
    con.close()

#Consultar lista de deseos
def consultarlistadeseos(usu):
    cur,con= conectar()
    sql="SELECT productos.img,productos.nombre,productos.precio,productos.des,productos.codigo FROM productos INNER JOIN lista_deseos ON productos.codigo=lista_deseos.producto WHERE lista_deseos.usuario=?"
    cur.execute(sql,[usu])
    row=cur.fetchall()
    con.close()
    return row

#EliminarListaDeseos
def eliminarlistadeseos(cod,usuario):
    cur,con= conectar()
    sql="DELETE FROM lista_deseos WHERE usuario=? and producto=? "
    cur.execute(sql,[usuario,cod])
    con.commit()
    con.close()

#EliminarImagenUsuario
#CambiarImagen de Usuario
def eliminarimgusuario(img,usuario):
    cur,con= conectar()
    sql="UPDATE usuarios SET picture=? WHERE nombre= ?"
    cur.execute(sql,[img,usuario])
    con.commit()
    con.close()

#Actualizar datos usuario
def actualizadatosusuario(nombre,email,fecha,contra,usuario):
    cur,con= conectar()
    sql="UPDATE usuarios SET nombre=?,email=?,fecha=?,contra=? WHERE id= ?"
    cur.execute(sql,[nombre,email,fecha,contra,usuario])
    con.commit()
    con.close()

#Actualizar datos usuario
def actualizadatosusuarioadmin(nombre,email,rol,usuario):
    cur,con= conectar()
    sql="UPDATE usuarios SET nombre=?,email=?,rol=? WHERE id= ?"
    cur.execute(sql,[nombre,email,rol,usuario])
    con.commit()
    con.close()

#Registrar Usuario
def agregarusuario(nombre,contra,correo):
    cur,con= conectar()
    sql="INSERT INTO usuarios (nombre,contra,email) VALUES(?,?,?)"
    cur.execute(sql,[nombre,contra,correo])
    con.commit()
    con.close()


#busqueda producto
def busquedaProduto(busqueda):
    cur,con=conectar()
    sql="SELECT * FROM productos WHERE nombre LIKE ? "
    cur.execute(sql,["%" + busqueda + "%"])
    row=cur.fetchall()
    con.close()
    return row

#Consultar comentarios Admin
def consultarcomentariosAdmin():
    cur,con= conectar()
    sql="SELECT comentarios.fecha, comentarios.id, comentarios.comentario, comentarios.usuario, productos.codigo, productos.nombre FROM comentarios INNER JOIN productos ON productos.codigo=comentarios.producto "
    cur.execute(sql)
    row=cur.fetchall()
    con.close()
    return row

#Actualizar-Editar comentario
def actualizacomentario(id,mensaje):
    cur,con= conectar()
    sql="UPDATE comentarios SET comentario=? WHERE id= ?"
    cur.execute(sql,[mensaje,id])
    con.commit()
    con.close()

#EliminarComentario
def eliminarComentario(cod):
    cur,con= conectar()
    sql="DELETE FROM comentarios WHERE id=? "
    cur.execute(sql,[cod])
    con.commit()
    con.close()

#EliminarUsuario
def eliminarUsuario(cod):
    cur,con= conectar()
    sql="DELETE FROM usuarios WHERE id=? "
    cur.execute(sql,[cod])
    con.commit()
    con.close()

# Consultar lista de deseos
def consultarcalifi(usu,pro):
    cur,con= conectar()
    sql="SELECT * FROM calificacion WHERE usuario= ? and producto=? "
    cur.execute(sql,[usu,pro])
    row=cur.fetchone()
    con.close()
    return row

#Registrar Calificacion
def agregarcalificacion(usuario,producto,puntuacion):
    cur,con= conectar()
    sql="INSERT INTO calificacion (usuario,producto,puntuacion) VALUES(?,?,?)"
    cur.execute(sql,[usuario,producto,puntuacion])
    con.commit()
    con.close()

#-------------------------------------

#Actualizar producto
def actualizarproducto(nombre,precio,des,codigo):
    cur,con= conectar()
    sql="UPDATE productos SET nombre=?,precio=?,des=? WHERE codigo= ?"
    cur.execute(sql,[nombre,precio,des,codigo])
    con.commit()
    con.close()

#Eliminar Producto
def eliminarProducto(cod):
    cur,con= conectar()
    sql="DELETE FROM productos WHERE codigo=?"
    cur.execute(sql,[cod])
    con.commit()
    con.close()

#Agregar producto
def agregarProducto(nombre,precio,des):
    cur,con= conectar()
    sql="INSERT INTO productos (nombre,precio,des) VALUES(?,?,?)"
    cur.execute(sql,[nombre,precio,des])
    con.commit()
    con.close()

#Consultar codigo
def consultarcodigo(nombre,precio,des):
    cur,con= conectar()
    sql="SELECT codigo FROM productos WHERE nombre= ? and precio=? and des=? "
    cur.execute(sql,[nombre,precio,des])
    row=cur.fetchone()
    con.close()
    return row

#Buscar productos
def Buscarproductos(nombre):

    cur,con= conectar()
    if nombre.isalpha():
        sql="SELECT * FROM  productos  where nombre=?"
    elif nombre.isnumeric():
        sql="SELECT * FROM  productos  where precio<?"
    cur.execute(sql,[nombre])
    row=cur.fetchall()
    con.close()
    return row

def cambiarcontrgusuario(contra):
    cur,con= conectar()
    sql="UPDATE usuarios SET contra=?"
    cur.execute(sql,[contra])
    con.commit()
    con.close()

#CambiarImagen de producto
def cambiarimgpro(img,pro):
    cur,con= conectar()
    sql="UPDATE productos SET img=? WHERE codigo= ?"
    cur.execute(sql,[img,pro])
    con.commit()
    con.close()
