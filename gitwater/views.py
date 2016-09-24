from gitwater import app

from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

import git


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
    commit = app.config['REPO'].head.commit
    tree = commit.tree

    file_list = map(lambda x: x.path, filter(lambda x: isinstance(x, git.objects.blob.Blob), tree))
    folder_list = map(lambda x: x.path, filter(lambda x: isinstance(x, git.objects.tree.Tree), tree))

    return render('/main.html', title=app.config['TITLE'], file_list=file_list, folder_list=folder_list)



@app.route('/<filepath>')
def filename(filepath):
    file_ = fetch_file(filepath)

    if not file_:
        raise ValueError('Could not find such file')

    file_string = blob_to_string(file_)
    try:
        lexer = guess_lexer_for_filename(filepath, file_string)
        file_contents_html = highlight(file_string, lexer, HtmlFormatter())
    except ClassNotFound:
        file_contents_html = file_string
        
    return render('main.html', title=app.config['TITLE'], file_contents=file_contents_html)
