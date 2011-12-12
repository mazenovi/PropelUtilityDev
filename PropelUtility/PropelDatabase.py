from PropelObject import *
from PropelTable import *
from PropelExternalSchema import *
import mforms

__all__ = ["PropelDatabase"]

VERSION = "1.0.0"

class PropelDatabase(PropelObject):

  fields = {
    'name':{
      'label':'name',
      'type':mforms.StringColumnType,
      'default':'propel',
      'editable':False,
      'width':100,
      'optional':False
    },
    'defaultIdMethod':{
      'label':'default id method',
      'type':mforms.StringColumnType,
      'items': ['native', 'none'],
      'default':'native',
      'editable':True,
      'width':100,
      'optional':False
    },
    'package':{
      'label':'package',
      'type':mforms.StringColumnType,
      'default':'lib.model',
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
    'defaultPhpNamingMethod':{
      'label':'defaultPhpNamingMethod',
      'type':mforms.StringColumnType,
      'items': ['nochange', 'underscore', 'phpname', 'clean'],
      'default':'underscore',
      'editable':True,
      'width':100,
      'optional':True
    },
    'heavyIndexing':{
      'label':'heavyIndexing',
      'type':mforms.StringColumnType,
      'items': ['True', 'False'],
      'default':'True',
      'editable':True,
      'width':100,
      'optional':True
    },
    'tablePrefix':{
      'label':'tablePrefix',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':True
    }
  }

  def __init__(self, catalog):

    self.wbObject = catalog
    self.tables = []
    self.cache = {}
    #load db data
    for k, v in self.fields.iteritems():
      if self.wbObject.customData.has_key(k):
        self.cache[k] = self.wbObject.customData[k]
    # associate Propel Tables
    for schema in catalog.schemata:
      for table in schema.tables:
        self.tables.append(PropelTable(table))
    # associate Propel External Schemas
    self.externalSchemas = []
    if self.cache.has_key('external_schemas'):
      externalSchemas = self.cache['external_schemas']
    elif self.wbObject.customData.has_key('external_schemas'):
      externalSchemas = pickle.loads(self.wbObject.customData['external_schemas'])
    else:
      externalSchemas = []
    for externalSchema in externalSchemas:
      self.externalSchemas.append(PropelExternalSchema(externalSchema, self))
  
  def __getattr__(self, name):
    if re.search('get_', name):
      if name[4:] == 'name' and self.cache.has_key('name'):
        return self.cache['name']
    return super(PropelDatabase, self).__getattr__(name)

  def save(self):
    for k, v in self.cache.iteritems():
      self.wbObject.customData[k] = v
    for t in self.tables:
      t.save()
    for external in self.externalSchemas:
      external.save()
    if self.cache.has_key('external_schemas'):
      self.wbObject.customData['external_schemas'] = pickle.dumps(self.cache['external_schemas'])

  def erase(self):
    for k in self.cache.keys():
      del self.cache[k]
    for k in self.wbObject.customData.keys():
      del self.wbObject.customData[k]
    for t in self.tables:
      t.erase()