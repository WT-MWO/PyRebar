class RebarSelector:
    def __init__(self, doc, uidoc):
        self.doc = doc
        self.uidoc = uidoc

    def is_rebar(self, selection):
        pass

    def get_rebars(self):
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
