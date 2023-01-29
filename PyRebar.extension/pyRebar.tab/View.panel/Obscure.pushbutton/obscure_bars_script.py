__doc__ = "Make all bars obscured in view."
__title__ = "Obscure Bars"
__author__ = "Wolinski"
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
x = False

t = Transaction(doc, "ObscuredBars")
t.Start()
for rebar in rebar_collector:
    rebar.SetUnobscuredInView(view, x)
t.Commit()
