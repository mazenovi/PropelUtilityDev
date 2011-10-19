from PropelObject import *
import mforms
import pickle
import re

__all__ = ["PropelForeignKey"]

VERSION = "1.0.0"

class PropelForeignKey(PropelObject):

  fields = {
    'table':{
      'label':'local table',
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
    'foreignTable':{
      'label':'foreign table',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'localColumn':{
      'label':'local column',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'foreignColumn':{
      'label':'foreign column',
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
    'refPhpName':{
      'label':'refPhpName',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'onDelete':{
      'label':'onDelete',
      'type':mforms.StringColumnType,
      'default':'NO ACTION',
      'editable':False,
      'width':100,
      'optional':True
    },
    'onUpdate':{
      'label':'onUpdate',
      'type':mforms.StringColumnType,
      'default':'NO ACTION',
      'editable':False,
      'width':100,
      'optional':True
    },
    'skipSql':{
      'label':'skipSql',
      'type':mforms.CheckColumnType,
      'default':0,
      'editable':True,
      'width':100,
      'optional':True
    },
    'defaultJoin':{
      'label':'defaultJoin',
      'type':mforms.StringColumnType,
      'items': ['Criteria::INNER_JOIN', 'Criteria::LEFT_JOIN'],
      'default':'',
      'editable':False,
      'width':100,
      'optional':True
    }
  }

  def __init__(self, foreignKey, propelTable):
    self.wbObject = foreignKey
    self.propelTable = propelTable
    if self.propelTable.wbObject.customData.has_key('foreign_keys'):
      self.propelTable.cache['foreign_keys'] = pickle.loads(self.propelTable.wbObject.customData['foreign_keys'])
    else:
      self.propelTable.cache['foreign_keys'] = {}
    # load column data
    if not self.propelTable.cache['foreign_keys'].has_key(foreignKey.name):
      self.propelTable.cache['foreign_keys'][foreignKey.name] = {}
    self.cache = self.propelTable.cache['foreign_keys'][foreignKey.name]
    
  def __getattr__(self, name):
    if re.search('get_', name):
      if name[4:] == 'table':
        return str(self.wbObject.owner.name)
      elif name[4:] == 'onUpdate':
        return str(self.wbObject.updateRule)
      elif name[4:] == 'onDelete':
        return str(self.wbObject.deleteRule)
      elif name[4:] == 'foreignTable':
        return str(self.wbObject.referencedTable.name)
      elif name[4:15] == 'localColumn':
        return str(self.wbObject.columns[int(name[16:])].name)
      elif name[4:17] == 'foreignColumn':
        return str(self.wbObject.referencedColumns[int(name[18:])].name)
    return super(PropelForeignKey, self).__getattr__(name)

  def save(self):
    for k, v in self.fields.iteritems():
      self.propelTable.cache['foreign_keys'][self.wbObject.name] = self.cache
