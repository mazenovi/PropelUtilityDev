from PropelTab import *
from PropelForm import *
import mforms

__all__ = ["PropelTabGrid"]

VERSION = "1.0.0"

class PropelTabGrid(PropelTab):

  defaults = {
    'popup_width':530,
    'popup_height':50,
    'popup_x':110,
    'popup_y':250
  }

  def search(self):
    tBox = PropelForm.spaced_box(True)
    self.widgets['search_label'] = mforms.newLabel("table pattern")
    tBox.add(self.widgets['search_label'], False, True)
    self.widgets['search_pattern'] = mforms.newTextEntry()
    tBox.add(self.widgets['search_pattern'], True, True)
    self.widgets['search_button'] = mforms.newButton()
    self.widgets['search_button'].set_text("matching tables")
    self.widgets['search_match_count'] = mforms.newLabel("")
    self.widgets['search_button'].add_clicked_callback(lambda: self.find_rows(0))
    tBox.add(self.widgets['search_button'], False, True)
    tBox.add(self.widgets['search_match_count'], False, True)
    self.add(tBox, False, True)

  def colmuns_name(self, grid_name):
    for fieldName in self.fields_list:
      self.widgets[grid_name].add_column(self.fields[fieldName]['type'], self.fields[fieldName]['label'], self.fields[fieldName]['width'], self.fields[fieldName]['editable'])
    self.widgets[grid_name].end_columns()
    self.widgets[grid_name].add_activated_callback(getattr(self, 'activate_field'))
    self.widgets[grid_name].set_cell_edited_callback(getattr(self, 'edit_field'))
    self.find_rows(0)

  def select_box(self, grid_name, edited_row, edited_col, fieldName):
    tBox = mforms.Form(None, mforms.FormResizable)
    tBox.set_title("Propel Choice")
    tBox.set_size(self.defaults['popup_width'], self.defaults['popup_height'])
    tBox.set_position(self.defaults['popup_x'], self.defaults['popup_y'])
    box = mforms.newBox(False)
    list = mforms.newSelector(mforms.SelectorPopup)
    list.add_items(self.fields[fieldName]['items'])
    list.set_selected(list.index_of_item_with_title(self.widgets[grid_name].get_string(edited_row, edited_col)))
    box.add(list, False, True)
    ok = mforms.newButton()
    ok.set_text("select this value")
    ok.add_clicked_callback(lambda: self.edit_field(edited_row, edited_col, list.get_string_value()))
    box.add_end(ok, False, True)
    tBox.set_content(box)
    tBox.run_modal(ok, None)

  

