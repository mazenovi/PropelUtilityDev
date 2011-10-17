from PropelTabFile import *
from PropelDatabase import *
from PropelTable import *
from PropelColumn import *
from PropelForeignKey import *
from PropelBehavior import *
from PropelIndice import *
from PropelExternalSchema import *
from PropelForm import *
import ElementTree as ET
import mforms
import re

__all__ = ["PropelTabExport"]

VERSION = "1.0.0"

class PropelTabExport(PropelTabFile):

  defaults = {
    'text_editor_width':730,
    'text_editor_height':300
  }

  def __init__(self, bool, name, db):
    self.db = db
    super(PropelTabExport, self).__init__(bool, name)
    self.options_schema_box()
    self.text_editor_schema_box()
    self.browse_schema_box()
    self.refresh_text_editor_schema_box()

  
  # return a xml propel schema from catalog
  def get_xmlized_schema(self):
    database = ET.Element('database')
    for k, v in PropelDatabase.fields.iteritems():
      if self.db.cache.has_key(k):
        database.attrib[k] = self.db.cache[k]
      elif not PropelDatabase.fields[k]['optional']:
        database.attrib[k] = PropelDatabase.fields[k]['default']
    for t in self.db.tables:
      table = ET.SubElement(database, 'table')
      for k, v in PropelTable.fields.iteritems():
        if getattr(t, 'get_' + k):
          table.attrib[k] = getattr(t, 'get_' + k)
        elif not PropelTable.fields[k]['optional']:
          table.attrib[k] = PropelTable.fields[k]['default']
      for c in t.columns:
        column = ET.SubElement(table, 'column')
        for k, v in PropelColumn.fields.iteritems():
          if k != 'table':
            if getattr(c, 'get_' + k):
              column.attrib[k] = str(getattr(c, 'get_' + k))
            elif not PropelColumn.fields[k]['optional']:
              column.attrib[k] = PropelColumn.fields[k]['default']
      for fk in t.foreignKeys:
        foreign_key = ET.SubElement(table, 'foreign-key')
        for k, v in PropelForeignKey.fields.iteritems():
          if k != 'table' and k != 'localColumn' and k!= 'foreignColumn':
            if getattr(fk, 'get_' + k):
              foreign_key.attrib[k] = str(getattr(fk, 'get_' + k))
            elif not PropelForeignKey.fields[k]['optional']:
              foreign_key.attrib[k] = PropelForeignKey.fields[k]['default']
        for k, col in enumerate(fk.wbObject.referencedColumns):
          reference = ET.SubElement(foreign_key, 'reference')
          reference.attrib['localColumn'] = str(getattr(fk, 'get_localColumn_' + str(k)))
          reference.attrib['foreignColumn'] = str(getattr(fk, 'get_foreignColumn_' + str(k)))
      for k, b in enumerate(t.behaviors):
        behavior = ET.SubElement(table, 'behavior')
        behavior.attrib['name'] = b.get_name
        for p in PropelBehavior.behaviors[b.get_name]:
          if getattr(b, 'get_parameter_' + str(p)) != '':
            parameter = ET.SubElement(behavior, 'parameter')
            parameter.attrib['name'] = p
            parameter.attrib['value'] = getattr(b, 'get_parameter_' + str(p))
      for i in t.indices:
        if i.get_indexType == 'UNIQUE' or i.get_indexType == 'INDEX':
          type = i.get_indexType.lower()
          indice = ET.SubElement(table, type)
          for k, v in PropelIndice.fields.iteritems():
            if k != 'columnName' and k != 'table' and k != 'indexType':
              if getattr(i, 'get_' + k):
                indice.attrib[k] = str(getattr(i, 'get_' + k))
              elif not PropelIndice.fields[k]['optional']:
                indice.attrib[k] = PropelIndice.fields[k]['default']
          for column_name in i.get_columnsName:
            indice_column = ET.SubElement(indice, type + '-column')
            indice_column.attrib['name'] = column_name
    for k, es in enumerate(self.db.externalSchemas):
      external_schema = ET.SubElement(database, 'external-schema')
      for k, v in PropelExternalSchema.fields.iteritems():
        if getattr(es, 'get_' + k):
          external_schema.attrib[k] = str(getattr(es, 'get_' + k))
        elif not PropelExternalSchema.fields[k]['optional']:
          external_schema.attrib[k] = PropelExternalSchema.fields[k]['default']

    self.indent(database)
    return ET.tostring(database)

  def indent(self, elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            self.indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

  def text_editor_schema_box(self):
    tBox = PropelForm.spaced_box(True)
    self.widgets['export_text_editor'] = mforms.newTextBox(mforms.BothScrollBars)
    self.widgets['export_text_editor'].set_size(self.defaults['text_editor_width'], self.defaults['text_editor_height'])
    self.widgets['export_text_editor'].set_bordered(True)
    self.widgets['export_text_editor'].set_read_only(False)
    tBox.add(self.widgets['export_text_editor'], False, True)
    self.add(tBox, False, True)

  def options_schema_box(self):
    tBox = PropelForm.spaced_box(True)
    self.widgets['export_FK_name'] = mforms.newCheckBox()
    self.widgets['export_FK_name'].set_text('export all FK name')
    self.widgets['export_FK_name'].set_active(self.db.wbObject.customData['export_FK_name'])
    self.widgets['export_FK_name'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_FK_name'], False, True)

    self.widgets['export_index'] = mforms.newCheckBox()
    self.widgets['export_index'].set_text('export all indexes')
    self.widgets['export_index'].set_active(self.db.wbObject.customData['export_index'])
    self.widgets['export_index'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_index'], False, True)

    self.widgets['export_index_name'] = mforms.newCheckBox()
    self.widgets['export_index_name'].set_text('export all indexe\'s name')
    self.widgets['export_index_name'].set_active(self.db.wbObject.customData['export_index_name'])
    self.widgets['export_index_name'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_index_name'], False, True)

    self.widgets['export_unique'] = mforms.newCheckBox()
    self.widgets['export_unique'].set_text('export all uniques')
    self.widgets['export_unique'].set_active(self.db.wbObject.customData['export_unique'])
    self.widgets['export_unique'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_unique'], False, True)

    self.widgets['export_unique_name'] = mforms.newCheckBox()
    self.widgets['export_unique_name'].set_text('export all unique\'s name')
    self.widgets['export_unique_name'].set_active(self.db.wbObject.customData['export_unique_name'])
    self.widgets['export_unique_name'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_unique_name'], False, True)
    self.add(tBox, False, True)

  def refresh_text_editor_schema_box(self):
    self.widgets['export_text_editor'].set_value(self.get_xmlized_schema())


  def browse_schema_box(self):
    tBox = PropelForm.spaced_box(True)
    label = mforms.newLabel("export propel schema")
    tBox.add(label, False, True)
    self.widgets['export_schema_path'] = mforms.newTextEntry()
    tBox.add(self.widgets['export_schema_path'], True, True)
    self.widgets['export_schema_file'] = mforms.newFileChooser(mforms.SaveFile)
    self.widgets['export_schema_file'].set_extensions('XML files (*.xml)|*.xml','xml')
    self.widgets['export_schema_file'].set_title("export schema file")
    browse = mforms.newButton()
    browse.set_text("Browse")
    browse.add_clicked_callback(lambda: self.browse_schema())
    tBox.add(browse, False, True)
    save = mforms.newButton()
    save.set_text("Save")
    save.add_clicked_callback(lambda: self.save_schema())
    tBox.add(save, False, True)
    self.add(tBox, False, True)

  def browse_schema(self):
    self.widgets['export_schema_file'].run_modal()
    self.widgets['export_schema_path'].set_value(self.widgets['export_schema_file'].get_path())

  def save_schema(self):
    if self.widgets['export_schema_path'].get_string_value() != "":
      f = open(self.widget['export_schema_path'].get_string_value(),"w")
      f.write(self.get_xmlized_schema())
      f.close()
    else:
      mforms.Utilities.show_warning("Warning", "Please select a xml file to export schema", "OK", "", "")

