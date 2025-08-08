
from src.graphql.setup import mutation

from flask_app import db
from src.models.docs import Docs
from src.models.tags import Tags



@mutation.field('test')
def resolve_test(_o, _i):  
  _err, cli = db
  
  t = Tags.by_name('@vars', create = True)
  d = Docs(data = { 'admin': 'nikolav' })

  t.docs.append(d)

  # cli.session.add(t)
  cli.session.add(d)

  cli.session.commit()
  
  
  return d.dump()



