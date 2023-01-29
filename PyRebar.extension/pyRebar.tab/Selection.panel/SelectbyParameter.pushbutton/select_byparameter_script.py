__doc__ = "Select all rebars in view by chosen Parameter."
__title__ = "Select by Diameter"
__author__ = "Wolinski"
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

"""
Goal is to create gui window with lisbox of parameters. Some of them can be predefined such as Comment, Partition
and add additional window with possibility to add own custom parameters and remove them.
This will require creation of some sort of .db file. This is cool bigger project.
A lot to learn
"""