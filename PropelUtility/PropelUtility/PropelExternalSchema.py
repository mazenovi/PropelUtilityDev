from PropelObject import *
import mforms
import pickle
import re

__all__ = ["PropelExternalSchema"]

VERSION = "1.0.0"

class PropelExternalSchema(PropelObject):

  fields = {
    'filename':{
      'label':'filename',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':False
    },
    'referenceOnly':{
      'label':'referenceOnly',
      'type':mforms.CheckColumnType,
      'default':1,
      'editable':True,
      'width':20,
      'optional':False
    }
  }

  def __init__(self, externalSchema, db):
    self.db = db
    self.cache = externalSchema
  
  def save(self):
    if not self.db.cache.has_key('external_schemas'):
      self.db.cache['external_schemas'] = []
    self.db.cache['external_schemas'].append(self.cache)
