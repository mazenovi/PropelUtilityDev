from PropelObject import *
from PropelColumn import *
from PropelForeignKey import *
from PropelIndice import *
from PropelBehavior import *
import mforms
import pickle

class PropelTable(PropelObject):

  fields = {
    'name':{
      'label':'table',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'idMethod':{
      'label':'idMethod',
      'type':mforms.StringColumnType,
      'default':'none',
      'items': ['native', 'none'],
      'editable':True,
      'width':100,
      'optional':True
    },
    'phpName':{
      'label':'phpname',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'package':{
      'label':'package',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'schema':{
      'label':'schema',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'namespace':{
      'label':'namespace',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'skipSql':{
      'label':'skipSql',
      'type':mforms.CheckColumnType,
      'default':'0',
      'editable':True,
      'width':100,
      'optional':True
    },
    'abstract':{
      'label':'abstract',
      'type':mforms.CheckColumnType,
      'default':'0',
      'editable':True,
      'width':100,
      'optional':True
    },
    'phpNamingMethod':{
      'label':'phpNamingMethod',
      'type':mforms.StringColumnType,
      'items': ['nochange', 'underscore','phpname', 'clean'],
      'default':'underscore',
      'editable':True,
      'width':100,
      'optional':True
    },
    'baseClass':{
      'label':'baseClass',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'basePeer':{
      'label':'basePeer',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'description':{
      'label':'description',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    },
    'heavyIndexing':{
      'label':'heavyIndexing',
      'type':mforms.CheckColumnType,
      'default':'0',
      'editable':True,
      'width':100,
      'optional':True
    },
    'readOnly':{
      'label':'readOnly',
      'type':mforms.CheckColumnType,
      'default':'0',
      'editable':True,
      'width':100,
      'optional':True
    },
    'treeMode':{
      'label':'treeMode',
      'type':mforms.StringColumnType,
      'items': ['NestedSet', 'MaterializedPath'],
      'default':'NestedSet',
      'editable':True,
      'width':100,
      'optional':True
    },
    'reloadOnInsert':{
      'label':'reloadOnInsert',
      'type':mforms.CheckColumnType,
      'default':'0',
      'editable':True,
      'width':100,
      'optional':True
    },
    'reloadOnUpdate':{
      'label':'reloadOnUpdate',
      'type':mforms.CheckColumnType,
      'default':'0',
      'editable':True,
      'width':100,
      'optional':True
    },
    'allowPkInsert':{
      'label':'allowPkInsert',
      'type':mforms.CheckColumnType,
      'default':'0',
      'editable':True,
      'width':20,
      'optional':True
    }
  }

  def __init__(self, table):
    self.wbObject = table
    # load table data
    self.cache = {}
    for k, v in self.fields.iteritems():
      if self.wbObject.customData.has_key(k):
        self.cache[k] = self.wbObject.customData[k]
    # associate Propel Columns
    self.columns = []
    for column in self.wbObject.columns:
      self.columns.append(PropelColumn(column, self))
    # associate Propel Foreign Keys
    self.foreignKeys = []
    for foreignKey in self.wbObject.foreignKeys:
      self.foreignKeys.append(PropelForeignKey(foreignKey, self))
    # associate Propel Indices
    self.indices = []
    for indice in self.wbObject.indices:
      self.indices.append(PropelIndice(indice, self))
    # associate Propel behaviors from table cahe or table customData
    self.behaviors = []
    if self.cache.has_key('behaviors'):
      behaviors = self.cache['behaviors']
    elif self.wbObject.customData.has_key('behaviors'):
      behaviors = pickle.loads(self.wbObject.customData['behaviors'])
    else:
      behaviors = []
    for behavior in behaviors:
      self.behaviors.append(PropelBehavior(behavior, self))

  def save(self):
    for k, v in self.fields.iteritems():
      if self.cache.has_key(k):
        self.wbObject.customData[k] = self.cache[k]
    # save associated Propel Columns
    for column in self.columns:
      column.save()
    if self.cache.has_key('columns'):
      self.wbObject.customData['columns'] = pickle.dumps(self.cache['columns'])
    # save associated Propel foreign Keys
    for foreignKey in self.foreignKeys:
      foreignKey.save()
    if self.cache.has_key('foreign_keys'):
      self.wbObject.customData['foreign_keys'] = pickle.dumps(self.cache['foreign_keys'])
    # save associated Propel indices
    # save associated Propel behaviors
    for behavior in self.behaviors:
      behavior.save()
    if self.cache.has_key('behaviors'):
      self.wbObject.customData['behaviors'] = pickle.dumps(self.cache['behaviors'])
    else:
      del self.wbObject.customData['behaviors']
  def erase(self):
    for k in self.cache.keys():
      del self.cache[k]
    for k in self.wbObject.customData.keys():
      del self.wbObject.customData[k]

      