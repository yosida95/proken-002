#-*- coding: utf-8 -*-

from flask import Flask, request, session, render_template, redirect, url_for
import wtforms
import fcntl

app = Flask(__name__)
app.secret_key = '0c5d3ecdf30e44f7b508b5985c5386b6'


@app.route('/')
def index():
    with open('./bbs.dat', 'r') as f:
        fcntl.fcntl(f, fcntl.LOCK_SH)
        posts = [line.strip().split('\t') for line in f]
        fcntl.fcntl(f, fcntl.LOCK_UN)

    form = PostForm(name=session.get('name', ''))

    return render_template('index.html', posts=posts, form=form)


@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        with open('bbs.dat', 'a') as f:
            fcntl.fcntl(f, fcntl.LOCK_EX)
            f.write('%s\t%s\n' % (form.name.data, form.text.data))
            fcntl.fcntl(f, fcntl.LOCK_UN)

        session['name'] = form.name.data

    return redirect(url_for('index'))


class PostForm(wtforms.Form):
    name = wtforms.TextField(u'お名前', [
        wtforms.validators.Required(),
    ])
    text = wtforms.TextField(u'投稿内容', [
        wtforms.validators.Required(),
    ])

if __name__ == '__main__':
    app.run(host='proken.ysd95.be', port=80, debug=False)
