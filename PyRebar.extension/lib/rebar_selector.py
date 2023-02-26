from Autodesk.Revit.UI import *
from Autodesk.Revit import DB


class RebarSelector:
    def __init__(self, doc, uidoc):
        self.doc = doc
        self.uidoc = uidoc

    def is_rebar(self, selection):
        """Checks if object is Rebar type."""
        pass

    def get_rebars(self):
        """Gets Rebar type objects from selected elements, if no objects selected
        triggers Pick Objects method"""
        selection = [
            self.doc.GetElement(x) for x in self.uidoc.Selection.GetElementIds()
        ]
        # If no object is selected prompt user to select
        if len(selection) < 1:
            selection = self.uidoc.Selection.PickObjects(
                Selection.ObjectType.Element, "Choose rebars"
            )
            elements = [self.doc.GetElement(el_id) for el_id in selection]
        else:
            elements = selection
        return elements

    def get_all_rebars(self):
        """Gets Rebar type objects from selected elements, if no objects selected
        gets all rebars in view"""
        selection = [
            self.doc.GetElement(x) for x in self.uidoc.Selection.GetElementIds()
        ]
        # If no object is selected prompt user to select
        if len(selection) < 1:
            elements = (
                DB.FilteredElementCollector(self.doc)
                .OfCategory(DB.BuiltInCategory.OST_Rebar)
                .WhereElementIsNotElementType()
            )
        else:
            elements = selection
        return elements
