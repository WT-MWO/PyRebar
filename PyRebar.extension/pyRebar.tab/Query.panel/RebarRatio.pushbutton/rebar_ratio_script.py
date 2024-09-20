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
    """Gets selected objects or prompts for selection"""
    selection = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]
    # If no object is selected prompt user to select
    if len(selection) < 1:
        selected_obj = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Choose elements")
        selection = [doc.GetElement(reference.ElementId) for reference in selected_obj]
    return selection


def can_host_rebar(element):
    """Verifies if element is valid and can host rebars
        Arguments:
        element(Element)
    Returns:
        boolean"""
    can_host = element.get_Parameter(DB.BuiltInParameter.DPART_CAN_HOST_REBAR).AsInteger()
    if can_host == 1:
        return True
    else:
        message = "Operation failed!\n" + "One of the selected elements cannot host rebar."
        forms.alert(msg=message, ok=True, exitscript=True)
        return False


filter = DB.ElementClassFilter(DB.Structure.Rebar)


def get_element_dependent_rebars(element):
    """Finds all dependent rebars of the element:
    Arguments:
        element(Element)
    Returns:
        list[Rebar]"""
    dependent_elements = element.GetDependentElements(filter)
    rebars = []
    for id in dependent_elements:
        # rebar = doc.GetElement(id)
        rebars.append(doc.GetElement(id))
    return rebars


def get_total_rebar_mass(rebars):
    """Calculates total mass of rebars
    Arguments:
        rebars(list[Rebar])
    Returns:
        mass(float) - mass in kg"""
    for rebar in rebars:
        # do stuff
        pass


def calculate_ratio(element, rebars):
    """Calculates ratio
    Arguments:
        element(Element)
        rebars(list[Rebar])
    Returns:
        ratio(float)"""
    # get element volume
    volume = element.Volume
    # get all element rebars
    total_rebar_mass = get_total_rebar_mass(rebars)
    ratio = round(total_rebar_mass / volume, 2)
    print(ratio)
    # TODO: add more info, like how many elements included?


# Main logic
elements = get_objects(doc, uidoc)
if len(elements) > 1:
    for element in elements:
        if can_host_rebar(element):
            # do stuff
            pass
elif len(elements) == 1:
    if can_host_rebar(elements[0]):
        rebars = get_element_dependent_rebars(elements[0])
        pass
