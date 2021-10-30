from flask import Flask, render_template, request, redirect, url_for,session,flash
from forms.nuevoProducto import NuevoProducto
import os
from conexion import *

from config import *
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import escape, secure_filename


nombre=""
precio=""

app = Flask(__name__)
app.config.from_object(dev)
app.secret_key=os.urandom(20)


@app.route("/", methods=["GET"])
def home():

    return render_template("home.html")


@app.route("/Edit_Profile", methods=["GET", "POST"])
def EditarPerfil():

    if not session:
        return render_template('sinpermiso.html')
    else:
        usuario=consultarCuatro("usuarios",session["nomusuario"])

        return render_template("EditProfile.html",usuario=usuario)


@app.route("/Edit_Profile/ActualizarDatos", methods=["GET", "POST"])
def ActualizaDatos():

    nombre=request.form["Name"]
    email=request.form["Email"]
    fecha=request.form["Age"]
    contra=request.form["address"]
    pass_enc=generate_password_hash(contra)
    actualizadatosusuario(nombre,email,fecha,pass_enc,session["idusuario"])

    return redirect("/Edit_Profile")

@app.route("/admin/actualizausu", methods=["GET", "POST"])
def ActualizaDatosAdmin():

    nombre=request.form["nombre"]
    email=request.form["correo"]
    cod=request.form["cod"]
    rol=request.form["select"]
    actualizadatosusuarioadmin(nombre,email,rol,cod)

    return redirect("/admin")

@app.route("/admin/actualizapro", methods=["GET", "POST"])
def ActualizaProducAdmin():

    nombre=request.form["nombre"]
    precio=request.form["precio"]
    cod=request.form["codigo"]
    descripcion=request.form["descripcion"]

    actualizarproducto(nombre,precio,descripcion,cod)
    return redirect("/admin")


@app.route("/Edit_Profile/EliminarImg",methods=["GET"])
def eliminarFoto():
    img='../static/img/USERimage.png'
    eliminarimgusuario(img,session["nomusuario"])

    return redirect("/Edit_Profile")

UPLOAD_FOLDER= os.path.abspath("./Ciclo_3_MisionTic/static/img/")
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
@app.route("/Edit_Profile/SubirFoto",methods=["POST"])
def cargarfoto():
    f=request.files["fileimagen"]
    filename=secure_filename(f.filename)
    f.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
    img="../static/img/"+filename
    eliminarimgusuario(img,session["nomusuario"])

    return redirect("/Edit_Profile")

@app.route("/Edit_Producto/CambiarFoto",methods=["POST"])
def cambiarimagenpro():
    f=request.files["fileimagen"]
    cod=request.form["codigo"]
    filename=secure_filename("ImgProd"+str(cod))
    f.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
    img="../static/img/"+filename
    cambiarimgpro(img,cod)
    return redirect("/admin")

@app.route("/login", methods=["GET", "POST"])
def login():

    return render_template("Loginreal.html")


@app.route("/login/val", methods=["POST"])
def val():

    usuario = escape(request.form["usuario"])
    contra = escape(request.form["contra"])

    usu=consultarCuatro("usuarios",usuario)

    if usu:
        contr=usu["contra"]
        if check_password_hash(contr,contra):

            session["idusuario"] = usu["id"]
            session["rol"] = usu["rol"]
            session["nomusuario"]=usu["nombre"]

            return redirect("/")

        else:
            flash("Usuario o Contraseña Incorrecta")
    else:
        flash("Usuario o Contraseña Incorrecta")

    return render_template("Loginreal.html")


@app.route("/login/cerrar", methods=["GET"])
def cerrar():
    session.clear()
    return redirect("/")

@app.route("/login/Register", methods=["GET","POST"])
def Register():
    return render_template("register2.html")


@app.route("/productos", methods=["GET"])
def productos():

    productos = []
    datos=consultar("productos")
    for pro in datos:
        productos.append(pro)


    return render_template("productos.html", productos=productos)


@app.route("/productos/<cod>", methods=["GET"])
def producto(cod):

    datos=consultarUno("productos",cod)

    if datos:
        nom = datos['nombre']
        des = datos['des']
        pre = datos['precio']
        ima = datos['img']

        comentarios = []
        datos=consultarVarios("comentarios",cod)
        comentarios=datos

        calificaciones = []
        datos=consultarVarios("calificacion",cod)
        for cal in datos:
            calificaciones.append(cal["puntuacion"])
        if calificaciones:
            puntuacion = sum(calificaciones)/len(calificaciones)
        else:
            puntuacion = "N/A"

        return render_template("producto.html", cod=cod, nom=nom, des=des, pre=pre, ima=ima, comentarios=comentarios, puntuacion=puntuacion)
    else:
        return render_template("pronoexiste.html", cod=cod)


@app.route("/listadeseos", methods=["GET"])
def listadeseos():
    if not session:
        return render_template('sinpermiso.html')
    elif (session["rol"] == "UsuarioFinal"):
        deseos = consultarlistadeseos(session["nomusuario"])
        return render_template("listadeseos.html", deseos=deseos)
    else:
        return render_template('sinpermiso.html')


@app.route("/listadeseos/agregar/<pro>", methods=["GET"])
def agregarlista(pro):

    if not session:
        return render_template('sinpermiso.html')
    if not session["rol"]=="UsuarioFinal":
        return render_template('sinpermiso.html')
    else:
        deseo=consultarTres("lista_deseos",session["nomusuario"],pro)
        if deseo:
            pass
        else:
            agregarlistadeseos(session["nomusuario"],pro)
        return redirect("/productos")


@app.route("/admin", methods=["GET"])
def admin():
    if not session:
        return render_template("sinpermiso.html")

    elif session["rol"]=="Admin" or session["rol"]=="SuperAdmin":

        usuarios = consultar("usuarios")
        comentarios = consultarcomentariosAdmin()

        productos = []
        if nombre == "" and precio=="":
            datos = consultar("productos")
            for pro in datos:
                productos.append(pro)
        else:
            print(nombre,"hola",precio)
            datos = Buscarproductos(nombre)
            for pro in datos:
                productos.append(pro)
        form = NuevoProducto()

        #Apartado para reportes
        pro=[]
        tproductos=consultar("productos")
        tcalificacion=consultar("calificacion")
        tlistadeseos=consultar("lista_deseos")
        tcomentarios=consultar("comentarios")

        for prod in tproductos:
            pro.append({"producto":prod["nombre"],"idpro":prod["codigo"]})

        for prod in pro:
            calificaciones = []
            for cal in tcalificacion:
                if int(cal["producto"]) == int(prod["idpro"]):
                    calificaciones.append(cal["puntuacion"])
            if calificaciones:
                puntuacion = sum(calificaciones)/len(calificaciones)
            else:
                puntuacion = "N/A"
            prod["calificacion"]=puntuacion

        for prod in pro:
            favoritos=[]
            for fav in tlistadeseos:
                if int(fav["producto"])==int(prod["idpro"]):
                    favoritos.append(1)
            if favoritos:
                favs=sum(favoritos)
            else:
                favs=0
            prod["favs"]=favs

        for prod in pro:
            comentari=[]
            for comen in tcomentarios:
                if int(comen["producto"])==int(prod["idpro"]):
                    comentari.append(1)
            if comentari:
                comens=sum(comentari)
            else:
                comens=0
            prod["comentarios"]=comens


        return render_template("admin.html", usuarios=usuarios, comentarios=comentarios, productos=productos, form=form ,pro=pro)

    else:
        return render_template("sinpermiso.html")

@app.route("/admin/eliminaComentario/<cod>",methods=["GET","POST"])
def eliminarComen(cod):
    eliminarComentario(cod)
    return redirect("/admin")

@app.route("/admin/editaComentario/<cod>",methods=["GET","POST"])
def editarComen(cod):
    mensaje=request.form["comen"]
    actualizacomentario(cod,mensaje)
    return redirect("/admin")

@app.route("/admin/guardarProducto",methods=["POST"])
def guardarProducto():

    nombre=request.form["nom"]
    precio=request.form["pre"]
    descr=request.form["des"]
    agregarProducto(nombre,precio,descr,)
    cons=consultarcodigo(nombre,precio,descr)
    cod=cons["codigo"]
    f=request.files["imagen"]
    filename=secure_filename("ImgProd"+str(cod))
    img="../static/img/"+filename
    f.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
    cambiarimgpro(img,cod)
    return redirect("/admin")

@app.route("/admin/eliminarProducto/<cod>",methods=["GET","POST"])
def eliminarProd(cod):
    eliminarProducto(cod)
    return redirect("/admin")

@app.route("/admin/eliminarUsu/<cod>",methods=["GET","POST"])
def eliminarUsu(cod):
    eliminarUsuario(cod)
    return redirect("/admin")


@app.route("/productos/calificar/<string:cod>")
def calificar(cod):

    cal=consultarcalifi(session["nomusuario"],cod)
    if cal:
        flash("Ya calificaste este producto con "+ str(cal["puntuacion"]))
    else:
        puntaje = int(request.args.get("btnradio"))
        agregarcalificacion(session["nomusuario"],cod,puntaje)

    return redirect(url_for('producto', cod=cod))


@app.route("/login/Register/Add", methods=["GET","POST"])
def NuevoUsuario():

    nombre = escape(request.form ["address"])
    contra = escape(request.form ["password"])
    correo = escape(request.form["email"])

    pass_enc=generate_password_hash(contra)

    usuario=consultarCuatro("usuarios",nombre)
    if usuario:
        flash("Usuario ya existe")
        return render_template("register2.html")
    else:
        agregarusuario(nombre,pass_enc,correo)
        return redirect("/login")


@app.route("/comentar/<cod>", methods=["POST"])
def comentar(cod):

    comentario = request.form["comentario"]
    fecha = date.today()

    agregarComentario(session["nomusuario"],cod,comentario,fecha)

    return redirect(url_for('producto', cod=cod))

@app.route("/listadeseos/eliminar/<usu>/<deseoEliminar>", methods=["GET"])
def eliminarlista(usu,deseoEliminar):

    eliminarlistadeseos(deseoEliminar,usu)

    return redirect(url_for("listadeseos",usu=usu))

@app.route("/produtos/busqueda", methods=["GET"])
def searchProducto():
    busqueda = request.args.get("busqueda")

    productos = []
    datos=busquedaProduto(busqueda)
    if datos:
        for pro in datos:
            productos.append(pro)


    return render_template("productos.html", productos=productos)


@app.route("/admin/buscarproducto",methods=["GET","POST"])
def BuscarProd():
    global nombre
    global precio
    nombre= request.form["buscar"]
    precio= request.form["buscar"]
    return redirect("/admin")


