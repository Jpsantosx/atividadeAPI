from flask import Flask, render_template, redirect, request, flash
import requests

app = Flask(__name__)
app.secret_key = "senai"


def consulta_personagem(nome):
    endpoint = f"https://dragonball-api.com/api/characters?name={nome}"

    resposta = requests.get(endpoint)

    if resposta.status_code == 200:
        personagens = resposta.json()

        if not personagens:
            return None

        p = personagens[0]

        name = p.get("name")
        ki = p.get("ki")
        maxKi = p.get("maxKi")
        race = p.get("race")
        gender = p.get("gender")
        description = p.get("description")
        image = p.get("image")

        return name, ki, maxKi, race, gender, description, image

    return None, None, None, None, None, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    nome = request.form.get("power")

    if not nome:
        flash("Digite um personagem")
        return redirect('/')

    dados = consulta_personagem(nome)

    if not dados:
        flash("Personagem não encontrado")
        return redirect('/')

    return render_template(
        "index.html",
        sucesso=True,
        name=dados[0],
        ki=dados[1],
        maxKi=dados[2],
        race=dados[3],
        gender=dados[4],
        description=dados[5],
        image=dados[6]
    )

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('erro404.html')

@app.errorhandler(500)
def pagina_nao_encontrada(e):
    return render_template('erro500.html')

if __name__ == "__main__":
    app.run(debug=True)