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


## Conversores de URL

Pode ser conveniente converter os parâmetros recebidos na URL, pois por padrão o Flask deixa eles como string. 

Para converter para inteiro por exemplo, podemos usar algo como o código abaixo:

```python
@app.route('/user/<username>/<int:quote_id>/')
def quote(username, quote_id):
    user = db.users.get(username, {})
    ...
```

Perceba que o tipo foi passando na seguinte estrutura: `<tipo>:<nome_parametro>`. Além de converter para o tipo apropriado, o match na rota só ocorre quando o tipo é o correto, entrando assim na view.

Temos muitos outros conversores que podem ajudar na hora do desenvolvimento, como podemos inspecionar:

```python
In [1]: app.url_map.converters
Out[1]: 
{'default': werkzeug.routing.UnicodeConverter,
 'string': werkzeug.routing.UnicodeConverter,
 'any': werkzeug.routing.AnyConverter,
 'path': werkzeug.routing.PathConverter,
 'int': werkzeug.routing.IntegerConverter,
 'float': werkzeug.routing.FloatConverter,
 'uuid': werkzeug.routing.UUIDConverter}

```

Outro exemplo é o conversor `path`, que permite receber caminhos de arquivo completos:

```python
@app.route('/file/<path:filename>/')
def filepath(filename):
    return f"Argumento recebido: {filename}"
```

Apesar dos conversores já existentes, é possível criar conversores adicionais. Suponhamos que queremos criar um conversor que capture a URL a partir de uma regex, como abaixo:

```python
@app.route('/reg/<regex("a.*"):name>/')
def reg(name):
    return f"Argumento iniciado com a letra a: {name}"
```

Para implementarmos este converter é necessário que extendamos a classe BaseConverter do Flask e registremos ela no app:

```python
# Converter
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# Registrando no app
app.url_map.converters['regex'] = RegexConverter
```

Também é possível criar um conversor para receber listar de parâmetros, para isto sobrescrevemos dois métodos do BaseConverter:

```python
class ListConverter(BaseConverter):
    """nome+nome2+nome3+nome..."""

    def to_python(self, value):
        """
            Método reponsável para converter um tipo do Python
        """
        return value.split('+')


    def to_url(self, values):
        """
            Método responsável para converter tipo Python para URL.
            Caso seja uma string ele irá manter, senão irá fazer o join colocando '+' entre os parâmetros
        """
        return '+'.join(
            BaseConverter.to_url(self, item) for item in values
        ) if not isinstance(values, str) else BaseConverter.to_url(self,values)

```

Basta registrar o novo converter e utilizar normalmente, recuperando assim uma lista de parâmetros agora:

```python
app.url_map.converters['list'] = ListConverter

def profile(usernames):

    html = ""

    for username in set(usernames):
        user = db.users.get(username, {})

        if user:
            html += f"""
                <h1>{user['name']}</h1>
                <img src="{user['image']}"/><br/>
                Telefone: {user['tel']}<br/>
                <a href="{url_for('index')}">Voltar</a>
                <hr />
            """
    return html or abort(404, "Users not fount")
```

## Novidades do Flask 1.x

Primeiramente, o suporte para Python 2.6 foi removido, permitindo assim rodar apenas em Python >= 2.7.

### App Flask

Agora o app criado a partir do objeto Flask permite receber mais dois parâmetros:

```python
app = Flask(
    __name__,
    host_matching = True, # Permite fazer matching também no host, padrão (False) é considerar apenas o que está depois de '/'
    static_host = "cdn.x.com" # Onde buscar arquivos estásticos.
)
```

Considerando o segundo parâmetro, quando usarmos `url_for('static', filename=...)` ele irá considerar a URL apontada em `static_host`.

### Blueprint

A classe Blueprint, que permite criar um modelo de aplicação conhecido como um módulo para ser reutilizado, agora recebe opicinalmente dois parâmetros:

```python
mod = Blueprint(
    'mymod',
    __name__,
    json_encode = MyJSON,
    json_decoder = MyJSON,
)
```

Assim é possível alterar o JSONEnconder sem afetar o padrão.

### Servidor de testes multi-thread

O servidor de teste, rodado em `flask run`, agora é multi-thread por padrão, permitindo atender mais de um request.

### Extensões

Agora as extensões do Flask precisam referênciar diretamente na hora do import:

```python
# Depreciado
from flask.ext.admin import Admin

# Nova forma
from flask_admin import Admin
```

### Logger

O logger padrão do Flask teve melhorias e por padrão o handler será Flask.App

### cli_test_runner & json_security_fix

Agora é possível invocar o comando `cli` programaticamente, permitindo assim testar melhor comandos `cli` do Flask (ex: `flask run`)

Para não abrir brechas de segurança, agora o Flask sempre retorne "UTF-8" a não ser que seja explicitamente informado para outro enconding. Anteriormente ele retornava o mesmo enconding da requisição, abrindo brechas de segurança.

### Documentação

A documentação foi atualizada, o tutorial também.

### Principais comando novos para o flask cli

Agora não é recomendado dar um `app.run()` na aplicação programaticamente. Assim devemos rodar direto pela linha de comando. 

Primeiro exportamos a variável de ambiente indicando onde está a aplicação principal e depois `flask run`:

```bash
export FLASK_APP=app.py # A extensão é opcional
flask run
```

Agora é mais fácil verificar as rotas da aplicação:

```bash
$ flask routes
Endpoint  Methods  Rule
--------  -------  --------------------------------
filepath  GET      /file/<path:filename>/
index     GET      /
quote     GET      /user/<username>/<int:quote_id>/
reg       GET      /reg/<regex("a.*"):name>/
reg_b     GET      /reg/<regex("b.*"):name>/
static    GET      /static/<path:filename>
user      GET      /user/<list:usernames>/
```

Para o app discovery também é opicional o nome `app`, antes era obrigatório na declaração da app:

```python
# Anteriormente
app = Flask(__name__)

# Agora
qualquer_nome = Flask(__name__)

```

Outra recomendação é sobre a application factory, que retorna a aplicação registrada e organizando melhor o código.

```python
def create_app():

    app = Flask(__name__)
    ...
```

Anteriormente o app discovery não conseguia iniciar a aplicação, porém agora é possíve pela variável de ambiente:

```bash
export FLASK_APP=app:create_app
```

Ele irá invocar a função para pegar o app criado. O `create_app` e `make_app` são reconhecidos por padrão, não sendo necessário específicar eles na variável de ambientes, outros nomes precisam ser específicados.

### Flask .env

Para facilitar a vida, agora o Flask suporta os arquivos .env, assim não é necessário ficar declarando variável de ambiente manualmente:

```bash
FLASK_APP=app
```
É necessário instalar o módulo `python-dotenv` para que o arquivo seja carregado.

Para definir o tipo de ambiente use `FLASK_ENV`:

```python
export FLASK_ENV=[production|development]
```

Assim já carregará com o auto-reloader, em debug e com enviroment de development.

### Test Client

Ao fazer requisições pelo test client era necessário específicar o `data` e o `header`, mesmo para conteúdo json. Agora quando for testar APIs com Json, pode-se enviar diretamente a requisição com o atributo json:

```python
client = app.test_client()
client.post('/', json={'a': '1', 'b': '2'})
```

Agilizando assim o teste de APIs.
