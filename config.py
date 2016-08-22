from jinja2 import Environment, FileSystemLoader
from git import Repo


JINJA = Environment(loader=FileSystemLoader('gitwater/templates'))

TITLE = 'GitWater'

REPO = Repo('/Users/samueln/Projects/Synth-Brewery')
