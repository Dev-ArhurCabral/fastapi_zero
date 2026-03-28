from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from fastapi_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/exercicio-html', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def exercicio_aula_02():
    return """
        <html>
          <head>
            <title>Nosso olá mundo!</title>
          </head>
          <body>
            <h1> Olá Mundo </h1>
          </body>
        </html>"""
