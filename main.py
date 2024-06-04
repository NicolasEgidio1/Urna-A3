from flask import Flask, render_template,request,abort,session,redirect,url_for,flash,jsonify
import dao
import requests


app = Flask(__name__)
app.secret_key = '777'



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        # Aqui você autentica o usuário e obtém o ID do usuário
        id_usuario = dao.usuario.realiza_login(email, senha)
        if id_usuario is not None:
            session['id_usuario'] = id_usuario
            # Redireciona o usuário para a página do perfil
            return redirect('/abre_urna')
        else:
            # Retorna uma mensagem de erro caso a autenticação falhe
            flash('E-mail ou senha inválidos')

    # Renderiza a página de login
    return render_template('login.html')

@app.route('/abre_urna')
def main():
    return render_template('index.html')

@app.route('/votar', methods=['POST'])
def inserir_voto():
    data = request.get_json()
    candidato_id = data['candidato_id']

    try:
        dao.Votos.votar(candidato_id)
        response = {'message': f'Voto registrado para o candidato com ID {candidato_id}'}
        return jsonify(response), 200
    except Exception as e:
        response = {'message': 'Erro ao registrar voto'}
        return jsonify(response), 500

@app.route('/entra_criar_conta')
def criar_conta():
    return render_template('criar_conta.html')

@app.route('/cadastrar',methods=['GET', 'POST'])
def salva_login():
    nome = request.form['nome']
    sexo = request.form['sexo']
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    cep = request.form['cep']
    email = request.form['email']
    senha = request.form['senha']

    # Validação dos dados do formulário
    if not nome or not sexo or not telefone or not cpf or not cep or not email or not senha:
        abort(400, 'Por favor, preencha todos os campos do formulário.')

    # Requisição à API ViaCEP
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        data = response.json()
        logradouro = data['logradouro']
        bairro = data['bairro']
        localidade = data['localidade']
        uf = data['uf']
    except requests.exceptions.RequestException as e:
        abort(500, f'Ocorreu um erro ao consultar o CEP: {e}')

    # Inserção no banco de dados
    dao.usuario.insere_usuario(nome, sexo, telefone, cpf, cep, email, senha, logradouro, bairro, localidade, uf)
        # Realiza o login do usuário recém-criado
    nome_usuario = dao.usuario.realiza_login(email, senha)

    if nome_usuario is not None:
     return redirect('abre_urna')


if __name__ == '__main__':
    app.run(debug=True)
