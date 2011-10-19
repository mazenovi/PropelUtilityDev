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
    'export_FK_name':False,
    'export_add_ai_on_pk':False,
    'export_index':False,
    'export_index_name':False,
    'export_unique':False,
    'export_unique_name':False,
    'export_schema_path':'schema.xml',
    'text_editor_width':970,
    'text_editor_height':300
  }

  def __init__(self, bool, name, db):
    self.db = db
    for k, v in self.defaults.iteritems():
      if not self.db.wbObject.customData.has_key(k):
        self.db.cache[k] = v
      else:
        self.db.cache[k] = self.db.wbObject.customData[k]
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
    database = self.convert_bool_value(database, PropelDatabase)
    for t in self.db.tables:
      table = ET.SubElement(database, 'table')
      for k, v in PropelTable.fields.iteritems():
        if getattr(t, 'get_' + k) and getattr(t, 'get_' + k) != PropelTable.fields[k]['default']:
          table.attrib[k] = getattr(t, 'get_' + k)
        elif not PropelTable.fields[k]['optional']:
          table.attrib[k] = PropelTable.fields[k]['default']
      table = self.convert_bool_value(table, PropelTable)
      for c in t.columns:
        column = ET.SubElement(table, 'column')
        for k, v in PropelColumn.fields.iteritems():
          if k != 'table':
            if getattr(c, 'get_' + k)  and getattr(c, 'get_' + k) != PropelColumn.fields[k]['default']:
              column.attrib[k] = str(getattr(c, 'get_' + k))
            elif c.get_primaryKey and k == 'autoIncrement' and self.widgets['export_add_ai_on_pk'].get_bool_value():
              column.attrib[k] = 'True'
            elif not PropelColumn.fields[k]['optional']:
              column.attrib[k] = PropelColumn.fields[k]['default']
        column = self.convert_bool_value(column, PropelColumn)
      for fk in t.foreignKeys:
        foreign_key = ET.SubElement(table, 'foreign-key')
        for k, v in PropelForeignKey.fields.iteritems():
          if k != 'table' and k != 'localColumn' and k!= 'foreignColumn':
            if k == 'name':
              if self.widgets['export_FK_name'].get_bool_value():
                foreign_key.attrib[k] = str(getattr(fk, 'get_' + k))
            elif getattr(fk, 'get_' + k) and getattr(fk, 'get_' + k) != PropelForeignKey.fields[k]['default']:
              foreign_key.attrib[k] = str(getattr(fk, 'get_' + k))
            elif not PropelForeignKey.fields[k]['optional']:
              foreign_key.attrib[k] = PropelForeignKey.fields[k]['default']
        foreign_key = self.convert_bool_value(foreign_key, PropelForeignKey)
        for k, col in enumerate(fk.wbObject.referencedColumns):
          reference = ET.SubElement(foreign_key, 'reference')
          reference.attrib['localColumn'] = str(getattr(fk, 'get_localColumn_' + str(k)))
          reference.attrib['foreignColumn'] = str(getattr(fk, 'get_foreignColumn_' + str(k)))
      for i in t.indices:
        if (i.get_indexType == 'UNIQUE' and self.widgets['export_unique'].get_bool_value()) or (i.get_indexType == 'INDEX' and self.widgets['export_index'].get_bool_value()):
          type = i.get_indexType.lower()
          indice = ET.SubElement(table, type)
          for k, v in PropelIndice.fields.iteritems():
            if k != 'columnName' and k != 'table' and k != 'indexType':
              if k == 'name':
                if (i.get_indexType == 'UNIQUE' and self.widgets['export_unique_name'].get_bool_value()) or (i.get_indexType == 'INDEX' and self.widgets['export_index_name'].get_bool_value()):
                  indice.attrib[k] = str(getattr(i, 'get_' + k))
              elif getattr(i, 'get_' + k):
                indice.attrib[k] = str(getattr(i, 'get_' + k))
              elif not PropelIndice.fields[k]['optional']:
                indice.attrib[k] = PropelIndice.fields[k]['default']
          for column_name in i.get_columnsName:
            indice_column = ET.SubElement(indice, type + '-column')
            indice_column.attrib['name'] = column_name
          indice = self.convert_bool_value(indice, PropelIndice)
      for k, b in enumerate(t.behaviors):
        behavior = ET.SubElement(table, 'behavior')
        behavior.attrib['name'] = b.get_name
        for p in PropelBehavior.behaviors[b.get_name]:
          if getattr(b, 'get_parameter_' + str(p)) != '':
            parameter = ET.SubElement(behavior, 'parameter')
            parameter.attrib['name'] = p
            parameter.attrib['value'] = getattr(b, 'get_parameter_' + str(p))      
    for k, es in enumerate(self.db.externalSchemas):
      external_schema = ET.SubElement(database, 'external-schema')
      for k, v in PropelExternalSchema.fields.iteritems():
        if getattr(es, 'get_' + k):
          external_schema.attrib[k] = str(getattr(es, 'get_' + k))
        elif not PropelExternalSchema.fields[k]['optional']:
          external_schema.attrib[k] = PropelExternalSchema.fields[k]['default']
      external_schema = self.convert_bool_value(external_schema, PropelExternalSchema)
    self.indent(database)
    return ET.tostring(database)

  def convert_bool_value(self, xmltag, associatedClass):
    for k, v in xmltag.attrib.iteritems():
      if associatedClass.fields[k]['type'] == mforms.CheckColumnType:
        if v:
          xmltag.attrib[k] = 'true'
        else:
          xmltag.attrib[k] = 'false'
    return xmltag

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
    self.widgets['export_FK_name'].set_active(self.db.cache['export_FK_name'])
    self.widgets['export_FK_name'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_FK_name'], False, True)

    self.widgets['export_add_ai_on_pk'] = mforms.newCheckBox()
    self.widgets['export_add_ai_on_pk'].set_text('add AI to PK')
    self.widgets['export_add_ai_on_pk'].set_active(self.db.cache['export_add_ai_on_pk'])
    self.widgets['export_add_ai_on_pk'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_add_ai_on_pk'], False, True)

    self.widgets['export_index'] = mforms.newCheckBox()
    self.widgets['export_index'].set_text('export all indexes')
    self.widgets['export_index'].set_active(self.db.cache['export_index'])
    self.widgets['export_index'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_index'], False, True)

    self.widgets['export_index_name'] = mforms.newCheckBox()
    self.widgets['export_index_name'].set_text('export all indexe\'s name')
    self.widgets['export_index_name'].set_active(self.db.cache['export_index_name'])
    self.widgets['export_index_name'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_index_name'], False, True)

    self.widgets['export_unique'] = mforms.newCheckBox()
    self.widgets['export_unique'].set_text('export all uniques')
    self.widgets['export_unique'].set_active(self.db.cache['export_unique'])
    self.widgets['export_unique'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_unique'], False, True)

    self.widgets['export_unique_name'] = mforms.newCheckBox()
    self.widgets['export_unique_name'].set_text('export all unique\'s name')
    self.widgets['export_unique_name'].set_active(self.db.cache['export_unique_name'])
    self.widgets['export_unique_name'].add_clicked_callback(lambda: self.refresh_text_editor_schema_box())
    tBox.add(self.widgets['export_unique_name'], False, True)

    self.add(tBox, False, True)

  def refresh_text_editor_schema_box(self):
    self.db.cache['export_FK_name'] = self.widgets['export_FK_name'].get_bool_value()
    self.db.cache['export_add_ai_on_pk'] = self.widgets['export_add_ai_on_pk'].get_bool_value()
    self.db.cache['export_index'] = self.widgets['export_index'].get_bool_value()
    self.db.cache['export_index_name'] = self.widgets['export_index_name'].get_bool_value()
    self.db.cache['export_unique'] = self.widgets['export_unique'].get_bool_value()
    self.db.cache['export_unique_name'] = self.widgets['export_unique_name'].get_bool_value()
    self.widgets['export_text_editor'].set_value(self.get_xmlized_schema())

  def browse_schema_box(self):
    tBox = PropelForm.spaced_box(True)
    label = mforms.newLabel("export propel schema")
    tBox.add(label, False, True)
    self.widgets['export_schema_path'] = mforms.newTextEntry()
    self.widgets['export_schema_path'].set_value(self.db.cache['export_schema_path'])
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
    self.db.cache['export_schema_path'] = self.widgets['export_schema_path'].get_string_value()

  def save_schema(self):
    if self.widgets['export_schema_path'].get_string_value() != "":
      f = open(self.widgets['export_schema_path'].get_string_value(),"w")
      f.write(self.get_xmlized_schema())
      f.close()
    else:
      mforms.Utilities.show_warning("Warning", "Please select a xml file to export schema", "OK", "", "")

