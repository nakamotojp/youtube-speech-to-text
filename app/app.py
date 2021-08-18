from flask import Flask, render_template, request
from src.main import main


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process')
def process():
    url = request.args.get('url')
    is_finish = main(url)
    return render_template('finish.html', result=is_finish[0], contents=is_finish[1])


if __name__ == '__main__':
    app.run()
