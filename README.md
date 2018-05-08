# Curso de Flask

Conteúdo do [Curso de Python](https://www.youtube.com/channel/UCMre98RDRijOX_fvG1gnsYg) que estou acompanhando.

## Criação do ambiente

Crie um virtualenv e execute a instalação do Flask:

```bash
mkdir projeto
cd projeto
python -m venv venv
source venv/bin/activate

pip install flask
```

Com isto os pacotes serão instalados devidamente.


## Executando uma app Flask

Para executar uma app Flask é bem simples, basta criar algo como o arquivo abaixo:

```python
from flask import Flask

app = Flask(__name__)

app.run()
```

Para rodar a aplicação basta executar o seguinte comando:

```bash
python app.py
```

Para que a aplicação recarregue automaticamente e facilitar o desenvolvimento faça no arquivo app.py:

```python
app.run(use_reloader=True)
```

Assim toda vez que salvar o arquivo o servidor irá reiniciar.


## Definindo rotas com o Flask

Para definir rotas com o Flask utilize a estrutura a seguir:

```python
@app.route('/')
def index():
    ...
    return "Hello"
```

Essa rota estará disponível na raíz da aplicação.

Também é possível adicionar rotas programaticamente através da função `app.add_url_rule`:

```python
def profile(username):
    ...

app.add_url_rule('/user/<username>/', view_func=profile, endpoint='user')
```

Para definir dinamicamente URLs baseadas em rotas do Flask é pode-se usar `url_for`:

```python
from flask import Flask, abort, url_for

@app.route('/')
def index():
    html = ['<ul>']

    for username, user in db.users.items():
        html.append(
            f"<li><a href='{url_for('user', username=username)}'>{user['name']}</a></li>"
        )

    html.append('</ul>')

    return '\n'.join(html)
```

Com isto, o `url_for` irá buscar através do endpoint passado (no caso `user`) e irá associar com a view criada anteriormente. Caso a URL mude na view também mudará dinamicamente no `url_for`


## Shell interativo

Para interagir com o Flask é necessário usar a extensão `flask-shell-ipython` e exportar a variável de ambiente `FLASK_APP`

```bash
pip install ipython flask-shell-ipython
export FLASK_APP=app.py

flask shell
```

Será aberto um terminal onde você poderá interagir com o app Flask:

```python
>>> app
<Flask 'app'>
```

Verificar mapa de regras registradas

```python
>>> app.url_map
 
Map([<Rule '/' (HEAD, GET, OPTIONS) -> index>,
 <Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/user/<username>/' (HEAD, GET, OPTIONS) -> user>])

```

Também é possível testar as rotas sem o navegador:

```python
>>> client = app.test_client()

>>> client.get('/user/david')
<Response streamed [301 MOVED PERMANENTLY]>

>>> client.get('/user/david', follow_redirects=True)
<Response streamed [200 OK]>

>>> client.get('/user/david/').status
'200 OK'

>>> client.get('/user/david/').headers
Headers([('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', '190')])

>>> client.get('/user/david/').data
b'\n            <h1>David Brent</h1>\n            <img src="https://api.adorable.io/avatars/100/david.png"/><br/>\n            Telefone: 5555-5555<br/>\n            <a href="/">Voltar</a>\n        '
```