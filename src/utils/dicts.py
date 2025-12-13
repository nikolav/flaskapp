
import shlex

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

  
  @staticmethod
  def dotted(d, prefix = ''):
    dd = {}
    for k, v in (d or {}).items():
      path = f'{prefix}.{k}' if prefix else k
      if isinstance(v, dict):
        dd.update(Dicts.dotted(v, path))
      else:
        dd[path] = v
    return dd

  
  @staticmethod
  def to_bash(cmd):
    '''
    Convert a dict into a bash-safe command string.

    Special key:
      '_' -> positional args (str | list)

    Rules:
      - single-char True flags are grouped: -xy
      - True  -> flag
      - False / None -> skipped
      - other -> --key value
      - values are shell-quoted
    '''

    parts       = []
    short_flags = []
    long_flags  = []
    values      = []

    # Positional arguments
    positional = cmd.get('_')
    if positional:
      if isinstance(positional, (list, tuple)):
        parts.extend(shlex.quote(str(x)) for x in positional)
      else:
        parts.append(shlex.quote(str(positional)))


    # Options / flags
    for key, value in cmd.items():      
      if key == '_':
        continue
      if value is False or value is None:
        continue

      # Boolean flags
      if value is True:
        if 1 == len(key):
          short_flags.append(key)
        else:
          long_flags.append(f'--{key}')
        continue

      # Options with values
      opt = f'-{key}' if 1 == len(key) else f'--{key}'
      values.append(opt)
      values.append(shlex.quote(str(value)))
    
    # Append grouped short flags at once
    if short_flags:
      parts.append(f'-{''.join(short_flags)}')
    
    # Append grouped long flags at once
    if long_flags:
      parts.append(' '.join(long_flags))
    
    # Append values last
    if values:
      parts.append(' '.join(values))

    return ' '.join(parts)


