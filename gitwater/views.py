from gitwater import app

from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter


def render(filename, *args, **kwargs):
    return app.config['JINJA'].get_template(filename).render(*args, **kwargs)


def fetch_file(filepath):
    commit = app.config['REPO'].head.commit
    tree = commit.tree

    for node in tree:
        if node.path == filepath:
            return node


def blob_to_string(blob):
    bytes_ = blob.data_stream.read()
    return bytes_.decode('utf-8')


@app.route('/')
def main():
    return render('/main.html', title=app.config['TITLE'])


@app.route('/<filepath>')
def filename(filepath):
    file_ = fetch_file(filepath)

    if not file_:
        raise ValueError('Could not find such file')

    file_string = blob_to_string(file_)

    lexer = guess_lexer_for_filename(filepath, file_string)
    file_contents_html = highlight(file_string, lexer, HtmlFormatter())

    return render('main.html', title=app.config['TITLE'], file_contents=file_contents_html)
