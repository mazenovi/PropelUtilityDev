from PropelTabGrid import *
from PropelForeignKey import *
import mforms
import re

__all__ = ["PropelTabForeignKeys"]

VERSION = "1.0.0"

class PropelTabForeignKeys(PropelTabGrid):

  fields_list = [
    'table',
    'name',
    'foreignTable',
    'localColumn',    
    'foreignColumn',
    'phpName',
    'refPhpName',
    'onDelete',
    'onUpdate',
    'skipSql',
    'defaultJoin'
  ]

  def __init__(self, bool, name, db):
    self.db = db
    self.fields = PropelForeignKey.fields
    super(PropelTabForeignKeys, self).__init__(bool, name)
    self.widgets['foreign_keys'] = mforms.newTreeView(1)
    self.search()
    self.colmuns_name('foreign_keys')
    self.add_end(self.widgets['foreign_keys'], True, True)
  
  def find_rows(self, selected_row):
    candidates = []
    
    for table in self.db.tables:
      if self.widgets['search_pattern'].get_string_value() == "" or re.search(self.widgets['search_pattern'].get_string_value(), table.get_name):
        candidates.append(table)
    self.widgets['foreign_keys'].clear_rows()
    self.widgets['search_match_count'].set_text("%i table(s) found" % len(candidates))
    for table in candidates:
      for foreignKey in table.foreignKeys:
        for k, column in enumerate(foreignKey.wbObject.referencedColumns):
          row = self.widgets['foreign_keys'].add_row()
          for lineNumber, fieldName in enumerate(self.fields_list):
            if fieldName == 'localColumn' or fieldName == 'foreignColumn':
              self.widgets['foreign_keys'].set_string(row, lineNumber, str(getattr(foreignKey, 'get_' + fieldName + '_' + str(k))))
            elif self.fields[fieldName]['type'] == mforms.StringColumnType:
              self.widgets['foreign_keys'].set_string(row, lineNumber, str(getattr(foreignKey, 'get_' + fieldName)))
            elif self.fields[fieldName]['type'] == mforms.CheckColumnType:
              self.widgets['foreign_keys'].set_bool(row, lineNumber, int(getattr(foreignKey, 'get_' + fieldName)))
    self.widgets['foreign_keys'].set_selected(selected_row)

  def activate_field(self, edited_row, edited_col):
    fieldName = self.fields_list[edited_col]
    if self.fields[fieldName].has_key('items') and len(self.fields[fieldName]['items']) > 0:
      self.select_box('foreign_keys', edited_row, edited_col, fieldName)

  def edit_field(self, edited_row, edited_col, value):
    fieldName = self.fields_list[edited_col]
    if bool(self.fields[fieldName]['editable']):
      tableName = self.widgets['foreign_keys'].get_string(edited_row, self.fields_list.index('table'))
      foreignKeyName = self.widgets['foreign_keys'].get_string(edited_row, self.fields_list.index('name'))
      for table in self.db.tables:
        if table.get_name == tableName:
          for foreignKey in table.foreignKeys:
            if foreignKey.get_name == foreignKeyName:
              f = foreignKey
              break
    setattr(f, 'set_' + fieldName, value)
    self.find_rows(self.widgets['foreign_keys'].get_selected())
