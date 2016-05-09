from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['POST', 'GET'])
def post_metrics():
    app.logger.debug(request.get_json())
    return "200"

if __name__ == '__main__':
    app.run()
