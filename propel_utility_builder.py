import sys
import os
import re
import binascii

imported_modules = [
  'sys',
  'os',
  'grt',
  'mforms',
  're',
  'pickle',
  'new',
  'warnings',
  'tempfile',
  'binascii'
]

included_files = [
  'ElementTree',
  'PropelForm',
  'PropelObject',
  'PropelColumn',
  'PropelForeignKey',
  'PropelIndice',
  'PropelBehavior',
  'PropelTable',
  'PropelExternalSchema',
  'PropelDatabase',
  'PropelTab',
  'PropelTabGrid',
  'PropelTabDatabase',
  'PropelTabTables',
  'PropelTabColumns',
  'PropelTabForeignKeys',
  'PropelTabIndices',
  'PropelTabBehaviors',
  'PropelTabFile',
  'PropelTabExternalSchemas',
  'PropelTabExport',
  '../propel_utility_dev_grt'
]

builded_file = 'propel_utility_grt.py'

# importations
builded = 'from wb import *\n'
for module in imported_modules:
  builded += 'import '+ module +'\n'

# include
for file in included_files:
  i = open('PropelUtility/' + file + '.py', 'r')
  builded += "\n# " + file + "\n"
  for line in i:
    if not re.match("^\n", line) and not re.match("^[\t ]*#", line) and not re.match("^from", line) and not re.match("^import", line):
      builded += line
  i.close()

# pop namespace in main
builded = builded.replace('self.db = PropelDatabase.PropelDatabase(grt.root.wb.doc.physicalModels[0].catalog)','self.db = PropelDatabase(grt.root.wb.doc.physicalModels[0].catalog)')
builded = builded.replace('tTab = getattr(self.tabs[name][\'class\'], self.tabs[name][\'method\'])(False, name, self.db)', 'tTab = self.tabs[name][\'class\'](False, name, self.db)')
builded = builded.replace('ET.', '')

# remove dev labels
builded = builded.replace('Propel Utilities (Dev)', 'Propel Utilities')
builded = builded.replace('PropelUtilityDev', 'PropelUtility')
builded = builded.replace('Propel Utilty (Dev)', 'Propel Utility')
builded = builded.replace('PropelEraseDev', 'PropelErase')
builded = builded.replace('Propel Erase All Data (Dev)', 'Propel Erase All Data')

# code specific to module
builded = re.sub(re.compile('^__all__.*=.*\[\n(\s*"\w+",\n*)+\s*\]\n', re.MULTILINE), '', builded)
builded = re.sub(re.compile('^__all__.*=.*\[.*\]\s*\n', re.MULTILINE), '', builded)
builded = re.sub('VERSION = ".*"\n', '', builded)

# import propel image in python code
sys.path.append(str(os.path.dirname(os.path.realpath(__file__))) + '/PropelUtility')

img = open(str(os.path.dirname(os.path.realpath(__file__))) + '/PropelUtility/propel-logo.png', 'rb')
builded_img = ''
for line_img in img:
  builded_img += binascii.hexlify(line_img)

builded = builded.replace(
  'img.set_image(str(os.path.dirname(os.path.realpath(__file__))) + \'/PropelUtility/propel-logo.png\')',
  """
    i = open(str(tempfile.gettempdir() + \'/propel-logo.png\'), 'wb')
    i.write(binascii.unhexlify(\'""" + builded_img + """\'))
    i.close()
    img.set_image(str(tempfile.gettempdir() + \'/propel-logo.png\'))
  """
)


f = open(builded_file, 'w')
f.write(builded)

