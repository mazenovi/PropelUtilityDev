from PropelTabGrid import *
from PropelColumn import *
import mforms
import re

__all__ = ["PropelTabGrid"]

VERSION = "1.0.0"

class PropelTabColumns(PropelTabGrid):

  fields_list = [
    'table',
    'name',
    'phpName',
    'peerName',
    'primaryKey',
    'required',
    'type',
    'phpType',
    'sqlType',
    'size',
    'scale',
    'defaultValue',
    'defaultExpr',
    'valueSet',
    'autoIncrement',
    'lazyLoad',
    'description',
    'primaryString',
    'phpNamingMethod',
    'inheritance'
  ]

  def __init__(self, bool, name, db):
    self.db = db
    self.fields = PropelColumn.fields
    super(PropelTabColumns, self).__init__(bool, name)
    self.widgets['columns'] = mforms.newTreeView(1)
    self.search('columns')
    self.colmuns_name('columns')
    self.add_end(self.widgets['columns'], True, True)
  
  def find_rows(self, selected_row):
    candidates = []
    for table in self.db.tables:
      if self.widgets['columns_search_pattern'].get_string_value() == "" or re.search(self.widgets['columns_search_pattern'].get_string_value(), table.get_name):
        candidates.append(table)
    self.widgets['columns'].clear_rows()
    self.widgets['columns_search_match_count'].set_text("%i table(s) found" % len(candidates))
    for table in candidates:
      for column in table.columns:
        row = self.widgets['columns'].add_row()
        for lineNumber, fieldName in enumerate(self.fields_list):
          if self.fields[fieldName]['type'] == mforms.StringColumnType:
            self.widgets['columns'].set_string(row, lineNumber, str(getattr(column, 'get_' + fieldName)))
          elif self.fields[fieldName]['type'] == mforms.CheckColumnType:
            self.widgets['columns'].set_bool(row, lineNumber, int(getattr(column, 'get_' + fieldName)))
    self.widgets['columns'].set_selected(selected_row)
    
  def activate_field(self, edited_row, edited_col):
    fieldName = self.fields_list[edited_col]
    if self.fields[fieldName].has_key('items') and len(self.fields[fieldName]['items']) > 0:
      self.select_box('columns', edited_row, edited_col, fieldName)

  def edit_field(self, edited_row, edited_col, value):
    fieldName = self.fields_list[edited_col]
    if bool(self.fields[fieldName]['editable']):
      tableName = self.widgets['columns'].get_string(edited_row, self.fields_list.index('table'))
      columnName = self.widgets['columns'].get_string(edited_row, self.fields_list.index('name'))
      for table in self.db.tables:
        if table.get_name == tableName:
          for column in table.columns:
            if column.get_name == columnName:
              c = column
              break
    setattr(c, 'set_' + fieldName, value)    
    self.find_rows(self.widgets['columns'].get_selected())
  