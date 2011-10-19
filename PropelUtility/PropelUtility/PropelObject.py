import re
import mforms

__all__ = ["PropelObject"]

VERSION = "1.0.0"

class PropelObject(object):

  def __getattr__(self, name):
    if re.search('get_', name):
      if hasattr(self.wbObject, name[4:]):
        return getattr(self.wbObject, name[4:])
      elif self.cache.has_key(name[4:]):
        return self.cache[name[4:]]
      elif self.fields.has_key(name[4:]):
        return self.fields[name[4:]]['default']
      else:
        return "unknown getter"
    else:
        return "unknown attr"

  def __setattr__(self, name, value):
    if re.search('set_', name):
      self.__dict__['cache'][name[4:]] = value
    else:
      self.__dict__[name] = value