__doc__ = "Select all rebars in view by Diameter."
__title__ = "Select by Diameter"
__author__ = "Wolinski"
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView


cmbBox.ItemsSource = sorted(
    [
        x.GetFillPattern().Name
        for x in revit.query.get_all_fillpattern_elements(DB.FillPatternTarget.Drafting)
    ]
)
