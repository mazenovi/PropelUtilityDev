from PropelTabGrid import *
from PropelBehavior import *
from PropelForm import *
import mforms
import re
import pickle

__all__ = ["PropelTabBehaviors"]

VERSION = "1.0.0"

class PropelTabBehaviors(PropelTabGrid):

  fields_list = [
    'table',
    'name',
    'parameter',
    'value'
  ]

  defaults = {
    'extra_behaviors_path':'behaviors.py'
  }

  def __init__(self, bool, name, db):
    self.db = db

    if not self.db.wbObject.customData['extra_behaviors_path']:
      self.db.cache['extra_behaviors_path'] = self.defaults['extra_behaviors_path']
    else:
      self.db.cache['extra_behaviors_path'] = self.db.wbObject.customData['extra_behaviors_path']

    self.fields = PropelBehavior.fields
    self.fields['name']['items'] = sorted(PropelBehavior.getBehaviorsDict(self.db.cache['extra_behaviors_path']).keys())
    self.behaviors = PropelBehavior.getBehaviorsDict(self.db.cache['extra_behaviors_path'])
    super(PropelTabBehaviors, self).__init__(bool, name)
    self.widgets['behaviors'] = mforms.newTreeView(1)
    self.search('behaviors')
    self.colmuns_name('behaviors')
    self.browse_extra_behaviors_box()
    self.add_remove_behavior_button()    
    self.add_end(self.widgets['behaviors'], True, True)
    

  def find_rows(self, selected_row):
    candidates = []
    for table in self.db.tables:
      if self.widgets['behaviors_search_pattern'].get_string_value() == "" or re.search(self.widgets['behaviors_search_pattern'].get_string_value(), table.get_name):
        candidates.append(table)
    self.widgets['behaviors'].clear_rows()
    self.widgets['behaviors_search_match_count'].set_text("%i table(s) found" % len(candidates))
    for table in candidates:
      row = self.widgets['behaviors'].add_row()
      self.widgets['behaviors'].set_string(row, self.fields_list.index('table'), table.get_name)
      for behavior in table.behaviors:
        for parameter in self.behaviors[behavior.get_name]:
          row = self.widgets['behaviors'].add_row()
          for lineNumber, fieldName in enumerate(self.fields_list):
            if fieldName == 'name':
              self.widgets['behaviors'].set_string(row, lineNumber, str(behavior.get_name))
            elif fieldName == 'parameter':
              self.widgets['behaviors'].set_string(row, lineNumber, str(parameter))
            elif fieldName == 'value':
              self.widgets['behaviors'].set_string(row, lineNumber, str(getattr(behavior, 'get_parameter_' + parameter)))
            elif self.fields[fieldName]['type'] == mforms.StringColumnType:
              self.widgets['behaviors'].set_string(row, lineNumber, str(getattr(behavior, 'get_' + fieldName)))
            elif self.fields[fieldName]['type'] == mforms.CheckColumnType:
              self.widgets['behaviors'].set_bool(row, lineNumber, int(getattr(behavior, 'get_' + fieldName)))
        # we must add a line for behavior without any argument too
        if len(self.behaviors[behavior.get_name]) == 0:
          row = self.widgets['behaviors'].add_row()
          for lineNumber, fieldName in enumerate(self.fields_list):
            if fieldName == 'name':
              self.widgets['behaviors'].set_string(row, lineNumber, str(behavior.get_name))
            elif fieldName == 'parameter':
              self.widgets['behaviors'].set_string(row, lineNumber, '')
            elif fieldName == 'value':
              self.widgets['behaviors'].set_string(row, lineNumber, '')
            elif self.fields[fieldName]['type'] == mforms.StringColumnType:
              self.widgets['behaviors'].set_string(row, lineNumber, '')
            elif self.fields[fieldName]['type'] == mforms.CheckColumnType:
              self.widgets['behaviors'].set_bool(row, lineNumber, '')
    self.widgets['behaviors'].set_selected(selected_row)
    

  def activate_field(self, edited_row, edited_col):
    fieldName = self.fields_list[edited_col]
    if self.fields[fieldName].has_key('items') and len(self.fields[fieldName]['items']) > 0:
      self.select_box('behaviors', edited_row, edited_col, fieldName)

  def edit_field(self, edited_row, edited_col, value):
    if value != '':
      fieldName = self.fields_list[edited_col]
      keys = range(0, self.widgets['behaviors'].get_selected()+1)
      keys.reverse()
      for i in keys:
        if self.widgets['behaviors'].get_string(i, self.fields_list.index('table')):
          tableName = str(self.widgets['behaviors'].get_string(i, self.fields_list.index('table')))
          break
      for table in self.db.tables:
        if table.get_name == tableName:
          t = table
          break
      if fieldName == 'name':
        behaviorName = value
        t.behaviors.append(PropelBehavior({'name':behaviorName}, t))
      elif fieldName == 'value':
        behaviorName = self.widgets['behaviors'].get_string(edited_row, self.fields_list.index('name'))
        parameterName = self.widgets['behaviors'].get_string(edited_row, self.fields_list.index('parameter'))
        for behavior in t.behaviors:
          if behavior.get_name == behaviorName:
            b = behavior
            break
        setattr(b, 'set_parameter_' + parameterName, value)
    self.find_rows(self.widgets['behaviors'].get_selected()+1)

  def add_remove_behavior_button(self):
    tBox = PropelForm.spaced_box(True)
    self.widgets['selectBehaviors'] = mforms.newSelector(mforms.SelectorPopup)
    self.widgets['selectBehaviors'].add_items(sorted(PropelBehavior.getBehaviorsDict(self.widgets['extra_behaviors_path'].get_string_value()).keys()))
    tBox.add(self.widgets['selectBehaviors'], False, True)
    addBehavior = mforms.newButton()
    addBehavior.set_text("add selected behavior to selected table")
    addBehavior.add_clicked_callback(lambda: self.add_behavior())
    tBox.add(addBehavior, False, True)
    removeBehavior = mforms.newButton()
    removeBehavior.set_text("remove this behavior")
    removeBehavior.add_clicked_callback(lambda: self.remove_behavior())
    tBox.add(removeBehavior, False, True)
    self.add_end(tBox, False, True)

  def add_behavior(self):
    behaviorName = str(self.widgets['selectBehaviors'].get_string_value())
    tableName = self.widgets['behaviors'].get_string(self.widgets['behaviors'].get_selected(), self.fields_list.index('table'))
    if behaviorName and tableName:
      for table in self.db.tables:
        if table.get_name == tableName:
          t = table
          break
      t.behaviors.append(PropelBehavior({'name':behaviorName}, t))
      self.find_rows(self.widgets['behaviors'].get_selected()+1)
    else:
      mforms.Utilities.show_warning("Warning", "Please select a table row with a not null 'name' column to add a behavior", "OK", "", "")

  def remove_behavior(self):
    behaviorName = self.widgets['behaviors'].get_string(self.widgets['behaviors'].get_selected(), self.fields_list.index('name'))
    keys = range(0, self.widgets['behaviors'].get_selected()+1)
    keys.reverse()
    tableIndex = 0
    for i in keys:
      if self.widgets['behaviors'].get_string(i, self.fields_list.index('table')):
        tableName = self.widgets['behaviors'].get_string(i, self.fields_list.index('table'))
        break
    for i, table in enumerate(self.db.tables):
        if table.get_name == tableName:
          tableIndex = i
          break
    if behaviorName and tableName:
      for i, behavior in enumerate(self.db.tables[tableIndex].behaviors):
        if behavior.get_name == behaviorName:
          del self.db.tables[tableIndex].behaviors[i]
          break
      self.find_rows(tableIndex)
    else:
      mforms.Utilities.show_warning("Warning", "Please select a behavior row with a not null 'behavior' column to remove this behavior", "OK", "", "")

  def browse_extra_behaviors_box(self):
    tBox = PropelForm.spaced_box(True)
    label = mforms.newLabel("extra behaviors")
    tBox.add(label, False, True)
    self.widgets['extra_behaviors_path'] = mforms.newTextEntry()
    self.widgets['extra_behaviors_path'].set_value(self.db.cache['extra_behaviors_path'])
    tBox.add(self.widgets['extra_behaviors_path'], True, True)
    self.widgets['extra_behaviors_file'] = mforms.newFileChooser(mforms.OpenFile)
    self.widgets['extra_behaviors_file'].set_extensions('Python files (*.py)|*.py','py')
    self.widgets['extra_behaviors_file'].set_title("extra behaviors file")
    browse = mforms.newButton()
    browse.set_text("Browse")
    browse.add_clicked_callback(lambda: self.browse_schema())
    tBox.add(browse, False, True)
    label = mforms.newLabel("see http://m4z3.me/extrabehaviors for details")
    tBox.add(label, False, True)
    self.add_end(tBox, False, True)

  def browse_schema(self):
    self.widgets['extra_behaviors_file'].run_modal()
    self.widgets['extra_behaviors_path'].set_value(self.widgets['extra_behaviors_file'].get_path())
    self.db.cache['extra_behaviors_path'] = self.widgets['extra_behaviors_path'].get_string_value()
    self.widgets['selectBehaviors'].clear()
    self.widgets['selectBehaviors'].add_items(sorted(PropelBehavior.getBehaviorsDict(self.widgets['extra_behaviors_path'].get_string_value()).keys()))
      