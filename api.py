"""
@Author     Marco A. Gallegos Loaeza <ma_galeza@hotmail.com>
@Date       2021/02/21
@Updated    2021/02/21
@Description
    This file Implements al the components required by the proiect API.
"""
import flask

API = flask.Flask(__name__)


@API.route('/')
def hello_world():
    return flask.jsonify({'message': 'API Tipo Cambio'})


if __name__ == "__main__":
    API.run(host="0.0.0.0", port=5555)