__doc__ = "Calculate rebar weight to concrete volume ratio."
__title__ = "Rebar ratio"
__author__ = "MWolinski"
from Autodesk.Revit import DB
from Autodesk.Revit import UI
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from pyrevit import forms
from rebar_selector import RebarSelector

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView


def get_objects(doc, uidoc):
    selection = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]
    # If no object is selected prompt user to select
    if len(selection) < 1:
        selected_obj = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Choose elements")
        selection = [doc.GetElement(reference.ElementId) for reference in selected_obj]
    return selection


def can_host_rebar(element):
    can_host = element.get_Parameter(DB.BuiltInParameter.DPART_CAN_HOST_REBAR).AsInteger()
    if can_host == 1:
        return True
    else:
        message = "Operation failed!\n" + "One of the selected elements cannot host rebar."
        forms.alert(msg=message, ok=True, exitscript=True)
        return False


# Main logic
elements = get_objects(doc, uidoc)
if len(elements) > 1:
    for element in elements:
        if can_host_rebar(element):
            # do stuff
            pass
elif len(elements) == 1:
    if can_host_rebar(elements[0]):
        # do stuff
        pass
