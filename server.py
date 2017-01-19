from flask import Flask, request, abort, url_for, render_template
from flask_assets import Environment, Bundle

from config import config
from miprimer import calculate_primers


app = Flask(__name__)
assets = Environment(app)


css = Bundle(
    'styles/main.css',
    output='css/main.css'
)
assets.register('css_all', css)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', )


@app.route('/primers', methods=['POST'])
def primers():
    mirna = request.form['mirna']
    results = calculate_primers(mirna)
    return render_template('primers.html', mirna=mirna, results=results)


if __name__ == '__main__':
    app.run(host=config['HOST'], port=config['PORT'], debug=True)
