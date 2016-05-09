from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def post_metrics():
  # app.logger.debug(request.form)
  return "200"

if __name__ == '__main__':
  app.run()
