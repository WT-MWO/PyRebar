__doc__ = "Calculate rebar weight to concrete volume ratio."
__title__ = "Rebar ratio"
__author__ = "MWolinski"
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView
