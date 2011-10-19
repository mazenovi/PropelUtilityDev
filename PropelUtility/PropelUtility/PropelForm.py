import mforms

__all__ = ["PropelForm"]

VERSION = "1.0.0"

class PropelForm:

  defaults = {
    'space':12,
  }

  def __init__(self):
    pass

  @staticmethod
  def spaced_section_box(bool, name):
    box = mforms.newSectionBox(bool, name)
    box.set_padding(PropelForm.defaults['space'])
    box.set_spacing(PropelForm.defaults['space'])
    return box

  @staticmethod
  def spaced_box(bool):
    box = mforms.newBox(bool)
    box.set_padding(PropelForm.defaults['space'])
    box.set_spacing(PropelForm.defaults['space'])
    return box