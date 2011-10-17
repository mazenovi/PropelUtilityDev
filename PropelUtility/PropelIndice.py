from PropelObject import *
import mforms
import pickle
import re

__all__ = ["PropelIndice"]

VERSION = "1.0.0"

class PropelIndice(PropelObject):

  fields = {
    'table':{
      'label':'table',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'name':{
      'label':'name',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'indexType':{
      'label':'type',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'columnName':{
      'label':'colum',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    }
  }

  def __init__(self, indice, propelTable):
    self.wbObject = indice
    self.propelTable = propelTable
    if self.propelTable.wbObject.customData.has_key('indices'):
      self.propelTable.cache['indices'] = pickle.loads(self.propelTable.wbObject.customData['indices'])
    else:
      self.propelTable.cache['indices'] = {}
    # load column data
    if not self.propelTable.cache['indices'].has_key(indice.name):
      self.propelTable.cache['indices'][indice.name] = {}
    self.cache = self.propelTable.cache['indices'][indice.name]

  def __getattr__(self, name):
    if re.search('get_', name):
      if name[4:] == 'table':
        return str(self.wbObject.owner.name)
      elif re.search('columnsName', name):
        tmp = []
        for column in self.wbObject.columns:
          tmp.append(column.referencedColumn.name)
        return tmp
    return super(PropelIndice, self).__getattr__(name)

  def save(self):
    for k, v in self.fields.iteritems():
      self.propelTable.cache['indices'][self.wbObject.name] = self.cache
