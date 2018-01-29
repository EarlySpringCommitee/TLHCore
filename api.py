import TLHCore
from flask import Flask, request
import json
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini',encoding="utf8")
host = config.get('General', 'host')
port = config.getint('General', 'port')

@app.route('/', methods=['GET'])
def api():
    client_data = request.form
    try:
        server_data = TLHCore.get(client_data['account'], client_data['password'], client_data['mode'])
    except ValueError:
        return 'Account or password Error!'
    return server_data if isinstance(server_data, str) else json.dumps(server_data, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host=host, port=port)