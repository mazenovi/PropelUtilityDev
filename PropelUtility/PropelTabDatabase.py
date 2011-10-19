from PropelTabGrid import *
from PropelDatabase import *
from PropelForm import *
import mforms

__all__ = ["PropelTabDatabase"]

VERSION = "1.0.0"

class PropelTabDatabase(PropelTabGrid):

  fields_list = [
    'name',
    'defaultIdMethod',
    'package',
    'schema',
    'namespace',
    'baseClass',
    'basePeer',
    'defaultPhpNamingMethod',
    'heavyIndexing',
    'tablePrefix'
  ]

  def __init__(self, bool, name, db):
    self.db = db
    self.fields = PropelDatabase.fields
    super(PropelTabDatabase, self).__init__(bool, name)
    self.widgets['database'] = mforms.newTreeView(1)
    self.colmuns_name()
    self.add_end(self.widgets['database'], True, True)

  def colmuns_name(self):
    self.widgets['database'].add_column(mforms.StringColumnType, 'attribute', 350, False)
    self.widgets['database'].add_column(mforms.StringColumnType, 'value', 350, True)
    self.widgets['database'].end_columns()
    self.widgets['database'].add_activated_callback(getattr(self, 'activate_field'))
    self.widgets['database'].set_cell_edited_callback(getattr(self, 'edit_field'))
    self.find_rows(0)

  def find_rows(self, selected_row):
    self.widgets['database'].clear_rows()
    for fieldName in self.fields_list:
      row = self.widgets['database'].add_row()
      self.widgets['database'].set_string(row, 0, fieldName)
      self.widgets['database'].set_string(row, 1, str(getattr(self.db, 'get_' + fieldName)))
    self.widgets['database'].set_selected(selected_row)
    
  def activate_field(self, edited_row, edited_col):
    fieldName = self.widgets['database'].get_string(edited_row, 0)
    if self.fields[fieldName].has_key('items') and len(self.fields[fieldName]['items']) > 0:
      self.select_box('database', edited_row, edited_col, fieldName)

  def edit_field(self, edited_row, edited_col, value):
    fieldName = self.widgets['database'].get_string(edited_row, 0)
    setattr(self.db, 'set_' + fieldName, value)
    self.find_rows(self.widgets['database'].get_selected())
    