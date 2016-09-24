from jinja2 import Environment, FileSystemLoader
from git import Repo


JINJA = Environment(loader=FileSystemLoader('gitwater/templates'))

TITLE = 'GitWater'

REPO = Repo("/full/path/to/your/git/repo")  # TODO: Make interface to switch this "on the fly"
