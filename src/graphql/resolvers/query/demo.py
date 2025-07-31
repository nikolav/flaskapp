import base64
from flask import render_template

from src.graphql.setup import query
from src.services.pdf import printHtmlToPDF


@query.field('demo')
def resolve_demo(_o, _i):
  file = printHtmlToPDF(render_template('pdf/blank-a4.html', content = 'FOO:BAR'))
  return base64.b64encode(file).decode('utf-8')

