from PropelTabFile import *
from PropelExternalSchema import *
from PropelForm import *
import mforms
import re

__all__ = ["PropelTabExternalSchemas"]

VERSION = "1.0.0"

class PropelTabExternalSchemas(PropelTabFile):

  fields_list = [
    'filename',
    'referenceOnly'
  ]

  def __init__(self, bool, name, db):
    self.db = db
    self.fields = PropelExternalSchema.fields
    super(PropelTabExternalSchemas, self).__init__(bool, name)
    self.widgets['external_schemas'] = mforms.newTreeView(1)
    self.browse_schema_box()
    self.colmuns_name()
    self.add_end(self.widgets['external_schemas'], True, True)


  def colmuns_name(self):
    for fieldName in self.fields_list:
      self.widgets['external_schemas'].add_column(self.fields[fieldName]['type'], self.fields[fieldName]['label'], self.fields[fieldName]['width'], self.fields[fieldName]['editable'])
    self.widgets['external_schemas'].end_columns()
    self.widgets['external_schemas'].set_cell_edited_callback(getattr(self, 'edit_field'))
    self.find_rows(0)

  def browse_schema_box(self):
    tBox = PropelForm.spaced_box(True)
    label = mforms.newLabel("external propel schema")
    tBox.add(label, False, True)
    self.widgets['external_schema_path'] = mforms.newTextEntry()
    tBox.add(self.widgets['external_schema_path'], True, True)
    self.widgets['external_schema_file'] = mforms.newFileChooser(mforms.OpenFile)
    self.widgets['external_schema_file'].set_extensions('XML files (*.xml)|*.xml','xml')
    self.widgets['external_schema_file'].set_title("external schema file")
    browse = mforms.newButton()
    browse.set_text("Browse")
    browse.add_clicked_callback(lambda: self.browse_schema())
    tBox.add(browse, False, True)
    add = mforms.newButton()
    add.set_text("Add")
    add.add_clicked_callback(lambda: self.add_schema())
    tBox.add(add, False, True)
    self.add(tBox, False, True)

  def browse_schema(self):
    self.widgets['external_schema_file'].run_modal()
    self.widgets['external_schema_path'].set_value(self.widgets['external_schema_file'].get_path())

  def add_schema(self):
    already = False
    for es in self.db.externalSchemas:
      if es['filename'] == self.widgets['external_schema_path'].get_string_value():
          already = True
    if not already:
      if self.widgets['external_schema_path'].get_string_value()!='':
        self.db.externalSchemas.append(PropelExternalSchema({ 'filename':self.widgets['external_schema_path'].get_string_value(), 'referenceOnly':self.fields['referenceOnly']['default'] }, self.db))
    self.find_rows(0)

  def find_rows(self, selected_row):
    self.widgets['external_schemas'].clear_rows()
    for schema in self.db.externalSchemas:
      row = self.widgets['external_schemas'].add_row()
      for lineNumber, fieldName in enumerate(self.fields_list):
        if self.fields[fieldName]['type'] == mforms.StringColumnType:
          self.widgets['external_schemas'].set_string(row, lineNumber, str(getattr(schema, 'get_' + fieldName)))
        elif self.fields[fieldName]['type'] == mforms.CheckColumnType:
          self.widgets['external_schemas'].set_bool(row, lineNumber, int(getattr(schema, 'get_' + fieldName)))
    self.widgets['external_schemas'].set_selected(selected_row)

  def edit_field(self, edited_row, edited_col, value):
    fieldName = self.fields_list[edited_col]
    filename = self.widgets['external_schemas'].get_string(edited_row, self.fields_list.index('filename'))
    for externalSchema in self.db.externalSchemas:
      if externalSchema.get_filename == filename:
        es = externalSchema
        break
    setattr(es, 'set_' + fieldName, value)
    self.find_rows(self.widgets['external_schemas'].get_selected())
