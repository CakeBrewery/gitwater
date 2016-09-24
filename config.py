from jinja2 import Environment, FileSystemLoader
from git import Repo


JINJA = Environment(loader=FileSystemLoader('gitwater/templates'))

TITLE = 'GitWater'

REPO = "/full/path/to/your/git/repo"
