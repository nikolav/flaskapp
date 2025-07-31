from src.graphql.setup import mutation


@mutation.field('test')
def resolve_test(_o, _i):  
  print('test')
  return 'test'

