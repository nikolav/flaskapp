
from src.graphql.setup import mutation

from flask_app import db
# from src.models.docs   import Docs
# from src.models.tags   import Tags
from src.models.assets import Assets

from src.schemas.serialization import SchemaSerializeAssets


@mutation.field('test')
def resolve_test(_o, _i):  
  _err, cli = db  

  a1 = cli.session.scalar(
    cli.select(
      Assets
    ).where(
      1 == Assets.id
    ))
  
  # a2 = Assets(name = 'foo:a2')
  # a3 = Assets(name = 'foo:a3')
  # a1.assets_has.append(a2)
  # a2.assets_has.append(a3)
  # cli.session.add_all((a1, a2, a3,))
  # cli.session.commit()
  
  return SchemaSerializeAssets(many = True, exclude = ('assets_has',)).dump(a1.assets_has)

