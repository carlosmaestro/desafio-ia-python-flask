from flask import Flask, render_template, request, make_response
from flask_pymongo import PyMongo
import json
import io
import csv

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'funcionario'
# app.config['MONGO_URI'] = 'mongodb://funcionarios:funcionarios123@ds259154.mlab.com:59154/funcionarios'
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/funcionario"

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign')
def sign():
    return render_template('sign.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    links = ['https://www.youtube.com', 'https://www.bing.com',
             'https://www.python.org', 'https://www.enkato.com']
    return render_template('example.html', links=links, myvar=451)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

@app.route('/funcionario', methods=['POST'])
def funcionario():
    user = mongo.db.users
    user.insert({
        'nome': request.form["nome"],
        'sexo': request.form["sexo"],
        'uf': request.form["uf"],
        'cpf': request.form["cpf"],
        'idade': request.form["idade"],
    })
    return "usuario inserido"

@app.route('/funcionario-book-load', methods=['POST'])
def funcionario_book_load():
    print(json.dumps(request.form, ensure_ascii=False))
    f = request.files['book_load_file']
    if not f:
        return "No file"
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    # lista de dicionarios de funcionarios
    list_funcionario = []

    user = mongo.db.users
    print(csv_input)
    for row in csv_input:
        if row[0] == '':
            continue
        funcionario = {
            'nome': row[1],
            'sexo': row[2],
            'uf': row[3],
            'cpf': row[4],
            'idade': row[5],
        }
        list_funcionario.append(funcionario)
        user.insert(funcionario)
        print(row)

    # stream.seek(0)
    # result = transform(stream.read())
    #
    # response = make_response(result)
    # response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    # return response
    # if id:
    #     print(id)
    return 'Usuario adicionado'


if __name__ == '__main__':
    app.run(debug=True)
