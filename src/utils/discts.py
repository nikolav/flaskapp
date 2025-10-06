
import dpath
from dpath import PathNotFound

from src.utils.merge_strategies import dict_deepmerger_extend_lists as merger


class Dicts:

  @staticmethod
  def merge(target, *sources):
    for node in sources:
      merger.merge(target, node)
    
  @staticmethod
  def get(node, path, *, DEFAULT = None):
    return dpath.get(node, path, default = DEFAULT)
  
  @staticmethod
  def set(node, path, value):
    dpath.new(node, path, value)

  @staticmethod
  def exists(node, path):
    return 0 < len(dpath.search(node, path))
  
  @staticmethod
  def rm(node, path):
    try:
      dpath.delete(node, path)
    except PathNotFound:
      pass
