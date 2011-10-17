import sys
sys.path.append('./modules/PropelUtility')
# import the wb module
from wb import *
# import the grt module
import grt
# import the mforms module for GUI stuff
import mforms
# import the re module
import re
# import the pickle module
import pickle
# import etree module
import ElementTree as ET
# define PropelUtilisty class
import new

from PropelForm import *

import PropelDatabase
import PropelTabDatabase
import PropelTabGrid
import PropelTabTables
import PropelTabColumns
import PropelTabForeignKeys
import PropelTabIndices
import PropelTabBehaviors
import PropelTabExternalSchemas
import PropelTabExport
import PropelTabFile


ModuleInfo = DefineModule(name= "Propel Utilities", author= "mazenovi", version="1.0")

class PropelUtilityGUI(mforms.Form):
  
  tabs_list = [
    'database',
    'tables',
    'columns',
    'foreign_keys',
    'indices',
    'behaviors',
    'external_schemas',
    'export'
    #'import',
    #'settings',
  ]

  tabs = {
    'database':{
      'name':'Database',
      'class':PropelTabDatabase,
      'method':'PropelTabDatabase'
    },
    'tables':{
      'name':'Tables',
      'class':PropelTabTables,
      'method':'PropelTabTables'
    },
    'columns':{
      'name':'Columns',
      'class':PropelTabColumns,
      'method':'PropelTabColumns'
    },
    'foreign_keys':{
      'name':'Foreign Keys',
      'class':PropelTabForeignKeys,
      'method':'PropelTabForeignKeys'
    },
    'indices':{
      'name':'Indices',
      'class':PropelTabIndices,
      'method':'PropelTabIndices'
    },
    'behaviors':{
      'name':'Behaviors',
      'class':PropelTabBehaviors,
      'method':'PropelTabBehaviors'
    },
    'external_schemas':{
      'name':'External Schemas',
      'class':PropelTabExternalSchemas,
      'method':'PropelTabExternalSchemas'
    },
    'export':{
      'name':'Export',
      'class':PropelTabExport,
      'method':'PropelTabExport'
    }#,
    #'import':{
    #  'name':'Import',
    #  'class':PropelTabFile,
    #  'method':'PropelTabFile'
    #},
    #'settings':{
    #  'name':'Preferences',
    #  'class':PropelTabFile,
    #  'method':'PropelTabFile'
    #}
  }

  defaults = {
    'width':700,
    'height':700,
    'fold_behaviors':True,
    'export_FK_name':False,
    'export_index':False,
    'export_index_name':False,
    'tab_index':0
  }

  widget = {}

  def __init__(self, catalog):
    
    self.db = PropelDatabase.PropelDatabase(grt.root.wb.doc.physicalModels[0].catalog)
    # have to store app prefernces in catalog.customData :/
    for k, v in self.defaults.iteritems():
      if not self.db.wbObject.customData.has_key(k):
        self.db.cache[k] = v
      else:
        self.db.cache[k] = self.db.wbObject.customData[k]
    # main windows : self
    mforms.Form.__init__(self, None, mforms.FormResizable)
    self.set_title("Propel Utility")
    self.set_size(self.defaults['width'], self.defaults['height'])
    # main box
    box = PropelForm.spaced_box(False)
    # header
    box.add(self.header_box(), False, False)
    # main tabs
    self.tvMain = mforms.newTabView(False)
    for name in self.tabs_list:
      tTab = getattr(self.tabs[name]['class'], self.tabs[name]['method'])(False, name, self.db)
      self.tvMain.add_page(tTab, self.tabs[name]['name'])
    self.tvMain.relayout()
    self.tvMain.set_active_tab(int(self.db.get_tab_index))
    #self.tvMain.add_tab_changed_callback(self.refresh_text_editor)
    #self.refresh_text_editor()
    box.add(self.tvMain, True, True)
    self.set_content(box)
    self.ui_ok_cancel_button(box)
 
  def header_box(self):
    headBox = mforms.newBox(True)
    img = mforms.newImageBox()
    img.set_image("./modules/PropelUtility/propel-logo.png")
    img.set_size(self.defaults['width']/2-PropelForm.defaults['space']*2, 100)
    headBox.add(img, False, False)
    return headBox

  def ui_ok_cancel_button(self, box):
    tBox = PropelForm.spaced_box(True)
    label = mforms.newLabel("remember to validate your changes by press OK, and save you .mwb file in MySQLWorkbench to save you Propel Utilty changes ;)")
    tBox.add(label, False, True)
    self.cancelButton = mforms.newButton()
    self.cancelButton.set_text("cancel")
    tBox.add_end(self.cancelButton, False, True)
    self.okButton = mforms.newButton()
    self.okButton.set_text("ok")
    tBox.add_end(self.okButton, False, True)
    self.okButton.add_clicked_callback(self.save)
    box.add_end(tBox, False, True)

  def save(self):
    self.db.set_tab_index = self.tvMain.get_active_tab()
    self.db.save()

  def run(self):
    self.run_modal(self.okButton, self.cancelButton)

@ModuleInfo.plugin("wb.catalog.util.PropelUtility", caption= "Propel Utilty", input= [wbinputs.currentCatalog()], pluginMenu= "Catalog", type="standalone")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)

def PropelUtility(catalog):
  form = PropelUtilityGUI(catalog)
  form.run()
  return 0

@ModuleInfo.plugin("wb.catalog.util.PropelErase", caption= "Propel Erase All Propel Data", input= [wbinputs.currentCatalog()], pluginMenu= "Catalog", type="standalone")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)

def PropelErase(catalog):
  if mforms.Utilities.show_warning("Warning", "All propel data of you will be lost", "OK", "NO IT'S A JOKE", ""):
    db = PropelDatabase.PropelDatabase(grt.root.wb.doc.physicalModels[0].catalog)
    # have to store app prefernces in catalog.customData :/
    for k, v in PropelUtilityGUI.defaults.iteritems():
      if not db.wbObject.customData.has_key(k):
        db.cache[k] = v
      else:
        db.cache[k] = db.wbObject.customData[k]
    db.erase()
  return 0