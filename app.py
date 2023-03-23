from flask import Flask, render_template, request, Markup
from Calculo_iva import liquidacion
import webbrowser
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_files', methods=['POST'])
def process_files():
    # Get the path to the selected folder from the form data
    folder_path = request.form.get('folder_path')
    file_saldos = request.form.get('file_saldos')

    folder_path = os.path.abspath(folder_path)

    # Call the calcular_iva_archivos function to process the files
    resultados = liquidacion(ruta_archivos=folder_path,
                             archivo_saldos=file_saldos)

    resultados_html = Markup(resultados.to_html(classes=['table'], index=False))

    # Pass the results to a new HTML template for displaying the output
    return render_template('results.html', resultados=resultados_html)


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == "__main__":
    # the command you want
    open_browser()
    app.run(port=5000)