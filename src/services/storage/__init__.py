
class StorageBackend:
  '''Universal interface for any storage system.'''

  def save(self, file_obj, path, content_type = None):
    '''Save a file-like object to storage. Must return public URL or path.'''
    raise NotImplementedError

  def url(self, path):
    '''Return a publicly accessible URL (if storage supports it).'''
    raise NotImplementedError
