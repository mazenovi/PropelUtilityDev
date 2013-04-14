from PropelObject import *
import mforms
import pickle
import re

__all__ = ["PropelBehavior"]

VERSION = "1.0.0"

class PropelBehavior(PropelObject):

  behaviors =  {
    'aggregate_column':('name','foreign_table','expression'),
    'alternative_coding_standards':('brackets_newline','remove_closing_comments','use_whitespace','tab_size','strip_comments'),
    'archivable':('archive_on_insert','archive_on_update','archive_on_delete','archive_class','archive_table','archived_at_column','log_archived_at'),
    'auto_add_pk':('name','autoIncrement', 'type'),
    'concrete_inheritance':('extends',),
    'delegate':('to',),
    'i18n':('i18n_columns', 'default_locale', 'locale_column', 'i18n_table', 'i18n_phpname'),
    'nested_set':('left_column', 'right_column', 'level_column', 'use_scope', 'scope_column','method_proxies'),
    'query_cache':('backend', 'lifetime'),
    'sluggable':('slug_column', 'slug_pattern', 'replace_pattern', 'replacement', 'separator', 'permanent'),
    'sortable':('rank_column', 'use_scope', 'scope_column'),
    'timestampable':('create_column', 'update_column'),
    'versionable':('version_table', 'version_column', 'log_created_at', 'log_created_by', 'log_comment')
  }
  
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
      'label':'behavior',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'items': [
        'aggregate_column',
        'alternative_coding_standards',
        'archivable',
        'auto_add_pk',
        'concrete_inheritance',
        'delegate',
        'i18n',
        'nested_set',
        'query_cache',
        'sluggable',
        'sortable',
        'timestampable',
        'versionable'
    ],
      'optional':False
    },
    'parameter':{
      'label':'param',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':False,
      'width':100,
      'optional':False
    },
    'value':{
      'label':'value',
      'type':mforms.StringColumnType,
      'default':'',
      'editable':True,
      'width':100,
      'optional':False
    }
  }

  def __init__(self, behavior, propelTable):
    self.propelTable = propelTable
    if not behavior.has_key('parameters'):
      behavior['parameters'] = {}
    self.cache = behavior
  
  def __getattr__(self, name):
    if name[:14] == 'get_parameter_':
      if self.cache['parameters'].has_key(name[14:]):
        return str(self.cache['parameters'][name[14:]])
      else:
        return ''
    return super(PropelBehavior, self).__getattr__(name)

  def __setattr__(self, name, value):
    if name[:14] == 'set_parameter_':
      self.__dict__['cache']['parameters'][name[14:]] = value
    else:
      return super(PropelBehavior, self).__setattr__(name, value)

  def save(self):
    if not self.propelTable.cache.has_key('behaviors'):
      self.propelTable.cache['behaviors'] = []
    self.propelTable.cache['behaviors'].append(self.cache)
