import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

groups_collector = (
    DB.FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_IOSModelGroups).WhereElementIsNotElementType().ToElementIds()
)


t = Transaction(doc, "HidingRevitLinks")
t.Start()

for group in groups_collector:
    if group is not None:
        if doc.GetElement(group).CanBeHidden(view):
            view.HideElements(groups_collector)

t.Commit()

#print("Complete")