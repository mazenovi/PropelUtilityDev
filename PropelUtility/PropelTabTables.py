from PropelTabGrid import *

from PropelTable import *
import mforms
import re

__all__ = ["PropelTabGrid"]

VERSION = "1.0.0"

class PropelTabTables(PropelTabGrid):

  fields_list = [
    'name',
    'export',
    'idMethod',
    'phpName',
    'package',
    'schema',
    'namespace',
    'skipSql',
    'abstract',
    'isCrossRef',
    'phpNamingMethod',
    'baseClass',
    'basePeer',
    'description',
    'heavyIndexing',
    'readOnly',
    'treeMode',
    'reloadOnInsert',
    'reloadOnUpdate',
    'allowPkInsert'
  ]

  def __init__(self, bool, name, db):
    self.db = db
    self.fields = PropelTable.fields
    super(PropelTabTables, self).__init__(bool, name)
    self.widgets['tables'] = mforms.newTreeView(1)
    self.search('tables')
    self.colmuns_name('tables')
    self.add_end(self.widgets['tables'], True, True)

  def find_rows(self, selected_row):
    candidates = []
    for table in self.db.tables:
      if self.widgets['tables_search_pattern'].get_string_value() == "" or re.search(self.widgets['tables_search_pattern'].get_string_value(), table.get_name):
        candidates.append(table)
    self.widgets['tables'].clear_rows()
    self.widgets['tables_search_match_count'].set_text("%i table(s) found" % len(candidates))
    for table in candidates:
      row = self.widgets['tables'].add_row()
      for lineNumber, fieldName in enumerate(self.fields_list):
        if self.fields[fieldName]['type'] == mforms.StringColumnType:
          self.widgets['tables'].set_string(row, lineNumber, str(getattr(table, 'get_' + fieldName)))
        elif self.fields[fieldName]['type'] == mforms.CheckColumnType:
          self.widgets['tables'].set_bool(row, lineNumber, int(getattr(table, 'get_' + fieldName)))
    self.widgets['tables'].set_selected(selected_row)    

  def activate_field(self, edited_row, edited_col):
    fieldName = self.fields_list[edited_col]
    if self.fields[fieldName].has_key('items') and len(self.fields[fieldName]['items']) > 0:
      self.select_box('tables', edited_row, edited_col, fieldName)

  def edit_field(self, edited_row, edited_col, value):
    fieldName = self.fields_list[edited_col]
    tableName = self.widgets['tables'].get_string(edited_row, self.fields_list.index('name'))
    for table in self.db.tables:
      if table.get_name == tableName:
        t = table
        break
    setattr(t, 'set_' + fieldName, value)
    self.find_rows(self.widgets['tables'].get_selected())
    