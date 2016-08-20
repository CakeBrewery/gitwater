from flask import Flask
from jinja2 import Environment, FileSystemLoader
from git import Repo

JINJA = Environment(loader=FileSystemLoader('templates'))

TITLE = 'GitWater'

REPO = Repo('/Users/samueln/Projects/Synth-Brewery')



app = Flask(__name__)



def render(filename, *args, **kwargs):
    return JINJA.get_template(filename).render(*args, **kwargs)

def fetch_file(filepath):
    commit = REPO.head.commit
    tree = commit.tree

    for node in tree:
        if node.path == filepath:
            return node

def blob_to_string(blob):
    bytes_ = blob.data_stream.read()
    return '{}'.format(bytes_.decode('utf-8').replace('\n', '<br />'))


@app.route('/')
def main():
    return render('main.html', title=TITLE)


@app.route('/<filepath>')
def filename(filepath):
    file_ = fetch_file(filepath)

    if not file_:
        raise ValueError('Could not find such file')


    return render('main.html', title=TITLE, file_contents=blob_to_string(file_))
