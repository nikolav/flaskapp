from src.graphql.setup import query


@query.field('status')
def resolve_status(_o, _i):
  return 'ok:7f304074-ba4e-5c75-8db4-faad5328589d'
