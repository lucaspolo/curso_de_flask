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

