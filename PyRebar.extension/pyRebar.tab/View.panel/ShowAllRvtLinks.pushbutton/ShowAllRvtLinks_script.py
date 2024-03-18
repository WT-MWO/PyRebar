import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

link_collector = (
    DB.FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_RvtLinks).OfClass(DB.RevitLinkInstance).ToElementIds()
)


t = Transaction(doc, "HidingRevitLinks")
t.Start()

for link in link_collector:
    if link is not None:
        if doc.GetElement(link).isHidden(view):
            view.UnhideElements(link_collector)

t.Commit()

#print("Complete")