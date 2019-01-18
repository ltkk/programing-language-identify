import json
import traceback

import fastText as ft
from flask import Flask, request, render_template

from data_crawler.data_prep import CodePreprocess


def rev_dict(dict):
    _dict = {}
    for key, val in dict.items():
        _dict[val] = key
    return _dict


app = Flask(__name__)


class CodeIdentify:
    def __init__(self, model_file='../classifier/model/ft.li.1701.bin',
                 code2namefile='../data_crawler/data/lang_code.json'):
        self.model = ft.load_model(model_file)
        self.code2name = rev_dict(json.load(open(code2namefile, encoding='utf8')))
        self.tp = CodePreprocess()

    def pred(self, txt):
        txt = self.tp.preprocess(txt)
        res = self.model.predict(txt)
        label = res[0][0]
        score = round(res[1][0], 2)
        language_name = self.code2name[label[6:]].upper()
        return language_name, score


ci = CodeIdentify()


@app.route('/')
def ping():
    return 'ok'


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            code = request.form['code']
            if not code or len(code) <= 20:
                return render_template('index.html', error='Please type more than 20 characters!')
            language, score = ci.pred(code)
            return render_template('index.html', language=language, score=score, code=code)
        except:
            traceback.print_exc()
            return render_template('index.html', error='Unknown error has occurred, please try again!')


if __name__ == '__main__':
    app.run(debug=True)
