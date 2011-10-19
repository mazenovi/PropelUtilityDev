from PropelTabGrid import *
from PropelIndice import *
import mforms
import re

__all__ = ["PropelTabIndices"]

VERSION = "1.0.0"

class PropelTabIndices(PropelTabGrid):

  fields_list = [
    'table',
    'name',
    'indexType',
    'columnName'
  ]

  def __init__(self, bool, name, db):
    self.db = db
    self.fields = PropelIndice.fields
    super(PropelTabIndices, self).__init__(bool, name)
    self.widgets['indices'] = mforms.newTreeView(1)
    self.search()
    self.colmuns_name('indices')
    self.add_end(self.widgets['indices'], True, True)

  def find_rows(self, selected_row):
    candidates = []

    for table in self.db.tables:
      if self.widgets['search_pattern'].get_string_value() == "" or re.search(self.widgets['search_pattern'].get_string_value(), table.get_name):
        candidates.append(table)
    self.widgets['indices'].clear_rows()
    self.widgets['search_match_count'].set_text("%i table(s) found" % len(candidates))
    for table in candidates:
      for indice in table.indices:
        for column in indice.get_columnsName:
          row = self.widgets['indices'].add_row()
          for lineNumber, fieldName in enumerate(self.fields_list):
            if fieldName == 'columnName':
              self.widgets['indices'].set_string(row, lineNumber, str(column))
            elif self.fields[fieldName]['type'] == mforms.StringColumnType:
              self.widgets['indices'].set_string(row, lineNumber, str(getattr(indice, 'get_' + fieldName)))
            elif self.fields[fieldName]['type'] == mforms.CheckColumnType:
              self.widgets['indices'].set_bool(row, lineNumber, int(getattr(indice, 'get_' + fieldName)))
    self.widgets['indices'].set_selected(selected_row)

  def activate_field(self, edited_row, edited_col):
    fieldName = self.fields_list[edited_col]
    if self.fields[fieldName].has_key('items') and len(self.fields[fieldName]['items']) > 0:
      self.select_box('indices', edited_row, edited_col, fieldName)

  def edit_field(self, edited_row, edited_col, value):
    fieldName = self.fields_list[edited_col]
    if bool(self.fields[fieldName]['editable']):
      tableName = self.widgets['indices'].get_string(edited_row, self.fields_list.index('table'))
      indiceName = self.widgets['indices'].get_string(edited_row, self.fields_list.index('name'))
      for table in self.db.tables:
        if table.get_name == tableName:
          for indice in table.indices:
            if indice.get_name == indiceName:
              f = indice
              break
    setattr(f, 'set_' + fieldName, value)
    self.find_rows(self.widgets['indices'].get_selected())
