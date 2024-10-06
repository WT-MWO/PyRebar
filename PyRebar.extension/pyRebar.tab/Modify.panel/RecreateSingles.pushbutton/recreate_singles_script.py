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

# Get all rebar  parameters?


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
    Returns: DB.Structure.RebarHookType"""
    hook_type_id = rebar_object.GetHookTypeId(index)
    return doc.GetElement(hook_type_id)


def get_hook_orient(rebar_object, index):
    """Returns hook orientation of the rebar object.
    Args:
    index: int - 0 for start, 1 for end
    Returns: DB.Structure.RebarHookOrientation"""
    hook_type_id = rebar_object.GetHookOrientation(index)
    return doc.GetElement(hook_type_id)


def get_rebar_shape(rebar_object):
    """Returns rebar shape the rebar object.
    Returns: DB.Structure.RebarShape"""
    shape_id = rebar_object.GetShapeId()
    return doc.GetElement(shape_id)


def recreate_shapedriven_rebar(
    doc, rebar_shape, rebar_type, start_hook_type, end_hook_type, host, norm, curves, start_hook_orient, end_hook_orient
):
    new_rebar = DB.Structure.Rebar.CreateFromRebarShape(
        doc,
        rebar_shape,
        rebar_type,
        start_hook_type,
        end_hook_type,
        host,
        norm,
        curves,
        start_hook_orient,
        end_hook_orient,
    )
    pass


# Get selected object
rs = RebarSelector(doc, uidoc)
elements = rs.get_rebars()

for rebar in elements:
    if utilities.is_rebar_group(rebar_object=rebar):
        host = get_bar_host(rebar)
        rebar_type = get_rebar_type(rebar)
        start_hook_type = get_hook_type(rebar, 0)
        end_hook_type = get_hook_type(rebar, 1)
        start_hook_orient = get_hook_orient(rebar, 0)
        end_hook_orient = get_hook_orient(rebar, 1)

        if rebar.IsRebarShapeDriven():
            rebar_shape = get_rebar_shape(rebar)
            norm = ""
            curves = ""

        # Get curve for each bar at index
        # for i in utilities.get_existing_bar_index(rebar):
        #     rebar_curve = utilities.get_curves_from_group_at_index(rebar, i)

        # Open multitransaction

        # close
