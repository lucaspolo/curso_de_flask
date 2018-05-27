from flask import Flask, abort, url_for

import db
from converters import RegexConverter, ListConverter

def create_app():

    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.url_map.converters['list'] = ListConverter


    @app.route('/')
    def index():
        html = ['<ul>']

        for username, user in db.users.items():
            html.append(
                f"<li><a href='{url_for('user', usernames=username)}'>{user['name']}</a></li>"
            )

        html.append('</ul>')

        return '\n'.join(html)


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


    @app.route('/user/<username>/<int:quote_id>/')
    def quote(username, quote_id):
        user = db.users.get(username, {})
        quote = user.get('quotes').get(quote_id)

        if user and quote:
            return f"""
                <h1>{user['name']}</h1>
                <img src="{user['image']}"/><br/>
                <p><q>{quote}</q></p>
            """
        else:
            return abort(404, "User or quote not fount")


    @app.route('/file/<path:filename>/')
    def filepath(filename):
        return f"Argumento recebido: {filename}"


    @app.route('/reg/<regex("a.*"):name>/')
    def reg(name):
        return f"Argumento iniciado com a letra a: {name}"


    @app.route('/reg/<regex("b.*"):name>/')
    def reg_b(name):
        return f"Argumento iniciado com a letra b: {name}"


    app.add_url_rule('/user/<list:usernames>/', view_func=profile, endpoint='user')

    return app
