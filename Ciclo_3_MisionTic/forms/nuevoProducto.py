from wtforms import Form, StringField, SubmitField, FileField, TextAreaField
from flask_wtf.file import FileField, FileRequired


class NuevoProducto (Form):
    imagen=FileField(FileRequired())
    nom= StringField("Nombre del Producto: ")
    pre= StringField("Precio del Producto: ")
    des= TextAreaField("Descripción del Producto: ")
    cod= StringField("Código del Producto: ")
    delete= SubmitField("Delete")
    save= SubmitField("Save")