from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, static_folder='static')

# Lista de quartos (inicialmente todos vazios)
quartos = ["vazio"] * 38

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SIS OCUPAÇÃO</title>
    </head>
    <body>
        <h1>Gerenciamento de Quartos</h1>
        <ul>
            <li><a href="/terreo">Térreo</a></li>
            <li><a href="/primeiro_andar">Primeiro Andar</a></li>
            <li><a href="/segundo_andar">Segundo Andar</a></li>
            <li><a href="/terceiro_andar">Terceiro Andar</a></li>
        </ul>
    </body>
    </html>
    """

@app.route("/terreo")
def terreo():
    return render_template("terreo.html", quartos=quartos)

@app.route("/primeiro_andar")
def primeiro_andar():
    return render_template("primeiro_andar.html", quartos=quartos)

@app.route("/segundo_andar")
def segundo_andar():
    return render_template("segundo_andar.html", quartos=quartos)

@app.route("/terceiro_andar")
def terceiro_andar():
    return render_template("terceiro_andar.html", quartos=quartos)

@app.route("/alterar_status/<int:quarto>")
def alterar_status(quarto):
    if 1 <= quarto <= 38:
        if quartos[quarto - 1] == "vazio":
            quartos[quarto - 1] = "ocupado"
        else:
            quartos[quarto - 1] = "vazio"
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(debug=True)
