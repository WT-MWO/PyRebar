__doc__ = """Recreate single bars from rebar group."""

__title__ = "RecreateSingle"
__author__ = "Wolinski"
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from rebar_selector import RebarSelector
import utilities

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView


# Get rebar type
# Get rebar geomety type, if shape driven recreate shape driven?
# Get hooktype
# Get all rebar  parameters?
# Recreate rebar shape driven? freeform?


def get_bar_host(rebar_object):
    """Returns host element of given rebar
    Returns: DB.Element"""
    id = rebar_object.GetHostId()
    return doc.GetElement(id)


def get_rebar_type(rebar_object):
    """Returns rebar type of the rebar object
    Returns: DB.Structure.RebarBarType"""
    type_id = rebar_object.GetTypeId()
    return doc.GetElement(type_id)


def get_hook_type(rebar_object, index):
    """Returns hook type of the rebar object.
    Args:
    index: int - 0 for start, 1 for end
    Returns:"""
    hook_type_id = rebar_object.GetHookTypeId(index)
    return doc.GetElement(hook_type_id)


# Get selected object
rs = RebarSelector(doc, uidoc)
elements = rs.get_rebars()

for rebar in elements:
    if utilities.is_rebar_group(rebar_object=rebar):
        host = get_bar_host(rebar)
        bar_type = get_rebar_type(rebar)
        start_hook_type = get_hook_type(rebar, 0)
        end_hook_type = get_hook_type(rebar, 1)

        if rebar.IsRebarShapeDriven():
            # recrate shapedriven
            pass
        # Get curve for each bar at index
        # for i in utilities.get_existing_bar_index(rebar):
        #     rebar_curve = utilities.get_curves_from_group_at_index(rebar, i)
