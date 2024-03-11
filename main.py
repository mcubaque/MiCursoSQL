from flask import Flask, render_template
import markdown
import mysql.connector
from config import Config  # Importa la clase Config desde el archivo config.py

app = Flask(__name__)
app.config.from_object(Config)  # Configura la aplicación Flask con la clase Config

# Conexión a la base de datos
db = mysql.connector.connect(
    host=app.config['DB_SERVER'],
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    database=app.config['DB_NAME']
)

# Ruta para el index
@app.route('/')
def index():
    # Consultar las categorías desde la base de datos
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Categorias")
    categorias = cursor.fetchall()
    cursor.close()

    # Renderizar el template del index con las categorías obtenidas
    return render_template('index.html', categorias=categorias)

# Ruta para los temas
@app.route('/temas_categoria/<int:categoria_id>')
def mostrar_temas_categoria(categoria_id):
    # Consultar los temas relacionados con la categoría desde la base de datos
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Temas WHERE categoria_id = %s", (categoria_id,))
    temas = cursor.fetchall()
    cursor.close()

    # Renderizar la plantilla temas_categoria.html con los temas obtenidos
    return render_template('temas_categoria.html', temas=temas)

# Ruta para descripciones de temas
@app.route('/descripcion_tema/<int:tema_id>')
def mostrar_descripcion_tema(tema_id):
    # Realizar la consulta a la base de datos para obtener la descripción del tema y su nombre
    cursor = db.cursor()
    cursor.execute("SELECT t.nombre, dt.descripcion FROM descripcion_tema dt JOIN temas t ON dt.id = t.id WHERE dt.tema_id = %s", (tema_id,))
    descripcion_tema = cursor.fetchone()
    cursor.close()

    # Verificar si se encontró la descripción del tema
    if descripcion_tema:
        nombre_tema, descripcion = descripcion_tema
        # Convertir la descripción Markdown a HTML
        descripcion_html = markdown.markdown(descripcion)
        # Renderizar la plantilla descripcion_tema.html con la descripción del tema obtenida
        return render_template('descripcion_tema.html', nombre_tema=nombre_tema, descripcion=descripcion_html)
    else:
        # Si no se encuentra la descripción, mostrar un mensaje de error o redireccionar a otra página
        return "Descripción no encontrada para el tema con ID {}".format(tema_id), 404



if __name__ == '__main__':
    app.run(debug=True)
