__doc__ = "Make all bars unobscured in view."
__title__ = "Unobscure Bars"
__author__ = "MWolinski"
import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

rebar_collector = (
    DB.FilteredElementCollector(doc)
    .OfCategory(DB.BuiltInCategory.OST_Rebar)
    .WhereElementIsNotElementType()
)
x = True

t = Transaction(doc, "Unobscured")
t.Start()
for rebar in rebar_collector:
    rebar.SetUnobscuredInView(view, x)
t.Commit()
