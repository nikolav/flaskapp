
from src.graphql.setup import query


@query.field('demo')
def resolve_demo(_o, _i):  
  # return ''
  
  # import base64
  # from flask import render_template
  # from src.services.pdf import printHtmlToPDF
  # return printHtmlToPDF(render_template('pdf/blank-a4.html', content = 'FOO:BAR'), 
  #                       base64_encoded = True)
  
  from src.services.jwt import JWT
  # tok = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIyMzMzLCJAIjoiMjAyNS0wOC0wMSAwOTozMjo0MS4zNjQ4MjUrMDA6MDAifQ.l4i5Q-1YRvSOTSp8_owJwDdQf5v3zmfASOWeQbe4-0I'
  return JWT.encode({ 'admin@nikolav.rs': '122' })


