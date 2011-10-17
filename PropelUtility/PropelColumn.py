from PropelObject import *
import mforms
import pickle
import re

__all__ = ["PropelColumn"]

VERSION = "1.0.0"

class PropelColumn(PropelObject):

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
      'label':'column',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'phpName':{
      'label':'phpName',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'type':{
      'label':'type',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'size':{
      'label':'size',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'primaryKey':{
      'label':'PK',
      'type':mforms.CheckColumnType,
      'default':0,
      'editable':False,
      'width':20,
      'optional':True
    },
    'autoIncrement':{
      'label':'AI',
      'type':mforms.CheckColumnType,
      'default':0,
      'editable':True,
      'width':20,
      'optional':True
    },
    'required':{
      'label':'NN',
      'type':mforms.CheckColumnType,
      'default':0,
      'editable':False,
      'width':20,
      'optional':True
    }
  }
  
  def __init__(self, column, propelTable):
    self.wbObject = column
    self.propelTable = propelTable
    if self.propelTable.wbObject.customData.has_key('columns'):
      self.propelTable.cache['columns'] = pickle.loads(self.propelTable.wbObject.customData['columns'])
    else:
      self.propelTable.cache['columns'] = {}
    # load column data
    if not self.propelTable.cache['columns'].has_key(column.name):
      self.propelTable.cache['columns'][column.name] = {}
    self.cache = self.propelTable.cache['columns'][column.name]

  def wbType2PropelDatatype(self):
    if self.wbObject.userType:
      if self.wbObject.userType.name == 'BOOL':
        return 'BOOLEAN'
      if self.wbObject.userType.name == 'BOOLEAN':
        return 'BOOLEAN'
      # if you have custom mappings you could add cases for them here:
      return self.wbObject.userType.name
    elif self.wbObject.simpleType:
      if self.wbObject.simpleType.name == 'INT' or self.wbObject.simpleType.name == 'MEDIUMINT':
        return 'INTEGER'
      if self.wbObject.simpleType.name == 'TINYTEXT':
        return 'VARCHAR'
      if self.wbObject.simpleType.name == 'TEXT':
       return 'LONGVARCHAR'
      if self.wbObject.simpleType.name == 'MEDIUMTEXT':
        return 'CLOB'
      if self.wbObject.simpleType.name == 'LONGTEXT':
        return 'CLOB'
      if self.wbObject.simpleType.name == 'DATETIME':
        return 'TIMESTAMP'
      return self.wbObject.simpleType.name
    elif self.wbObject.structuredType:
      return self.wbObject.structuredType.name

  def wbLength2PropelSize(self):
    if self.wbObject.length != -1:
      return str(self.wbObject.length)
    if self.wbObject.simpleType and self.wbObject.simpleType.name == 'TINYTEXT':
      return 16777215
    if self.wbObject.simpleType and self.wbObject.simpleType.name == 'MEDIUMTEXT':
      return 4294967295
    if self.wbObject.simpleType and self.wbObject.simpleType.name == 'DECIMAL':
      return self.wbObject.precision
    else:
      return ''
  
  def __getattr__(self, name):
    if re.search('get_', name):
      if name[4:] == 'table':
        return str(self.wbObject.owner.name)
      elif name[4:] == 'type':
        return self.wbType2PropelDatatype()
      elif name[4:] == 'size':
        return self.wbLength2PropelSize()
      elif name[4:] == 'primaryKey':
        for c in self.wbObject.owner.primaryKey.columns:
          if c.referencedColumn.name == self.wbObject.name:  
            return 1
        return 0
      elif name[4:] == 'autoIncrement':
        if self.cache.has_key('autoIncrement'):
          return self.cache['autoIncrement']
        elif hasattr(self.wbObject, 'autoIncrement'):
          return self.wbObject.autoIncrement
        else:
          return 0
      elif name[4:] == 'required':
        return self.wbObject.isNotNull
    return super(PropelColumn, self).__getattr__(name)

  def save(self):
    for k, v in self.fields.iteritems():
      self.propelTable.cache['columns'][self.wbObject.name] = self.cache
  