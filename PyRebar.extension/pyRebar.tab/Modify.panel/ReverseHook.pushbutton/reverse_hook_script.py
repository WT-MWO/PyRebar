__doc__ = "Reverse Hook at Start and Hook at End of the rebar."
__title__ = "Reverse Hook"
__author__ = "Wolinski"
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView
t = Transaction(doc, "Set Length")

selection = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]

tg = TransactionGroup(doc, "ReverseHook")
tg.Start()

# TODO: Make this flexible and working for single bars and rebar groups.
for rebar in selection:
    orient0 = rebar.GetHookOrientation(0)
    orient1 = rebar.GetHookOrientation(1)

    t = Transaction(doc, "SubTransaction")
    t.Start()

    if orient0 == 0:
        rebar.SetHookOrientation(0, DB.Structure.RebarHookOrientation.Left)
        rebar.SetHookOrientation(1, DB.Structure.RebarHookOrientation.Left)
    t.Commit()
tg.Assimilate()
