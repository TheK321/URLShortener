from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Start flask app automatically when run with python
if __name__ == '__main__':
    app.run(host='0.0.0.0')
