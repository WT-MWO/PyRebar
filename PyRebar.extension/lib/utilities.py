from Autodesk.Revit import DB


def is_rebar_group(rebar_object):
    """Checks if object is a rebar group
    Arg:
        rebar_object: DB.Structure.Rebar"""
    n_bars = rebar_object.NumberOfBarPositions
    if n_bars > 1:
        return True
    else:
        return False


def get_existing_bar_index(bar_object):
    """Checks if rebar exists at given position (can be hidden or removed)
    Arguments:
        rebar_object(DB.Structure.Rebar): the rebar object
    Returns:
        indexes(list(int))"""
    indexes = []
    n_bars = bar_object.NumberOfBarPositions
    for i in range(0, n_bars):
        if bar_object.DoesBarExistAtPosition(i):
            indexes.append(i)
    return indexes


def get_curves_from_group_at_index(rebar, index):
    multiplanaroption = DB.Structure.MultiplanarOption.IncludeAllMultiplanarCurves
    """Returns a curve from rebar at given index from rebar group
    Arguments:
        rebar (DB.Structure.Rebar): the rebar object
        index (int): the index of a bar in group
    Returns:
        list[DB.Line or DB.Curve]"""
    if rebar.DistributionType == DB.Structure.DistributionType.Uniform or DB.Structure.DistributionType.VaryingLength:
        rebar_curves = rebar.GetTransformedCenterlineCurves(False, False, False, multiplanaroption, index)
    else:
        rebar_curves = rebar.GetCenterlineCurves(False, False, False, multiplanaroption, index)
    return rebar_curves
