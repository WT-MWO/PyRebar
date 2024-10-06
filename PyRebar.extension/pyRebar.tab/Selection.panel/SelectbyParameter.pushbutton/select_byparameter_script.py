__doc__ = "Select all rebars in view by chosen Parameter."
__title__ = "Select by Parameter"
__author__ = "Wolinski"

from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from pyrevit import script
from pyrevit.forms import WPFWindow
from System.Collections.Generic import List
from rebar_selector import RebarSelector

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView


xaml_file = script.get_bundle_file("view.xaml")

default_parameters = ["Diameter, Partition, Comment, Schedule Mark"]

rs = RebarSelector(doc, uidoc)
rebar_collector = rs.get_all_model_rebars()


def get_rebar_ids_by_parameter(rebar_collector, parameter_name, expected_value):
    """Finds ids of rebars matching given parameter values.
    Args:
    rebar_collector (DB.FilteredElementCollector)
    parameter_name (str): name of the parameter
    expected_value (str): value of the parameter
    Returns:
    List[DB.ElementId]"""
    rebar_ids = List[DB.ElementId]()
    for rebar in rebar_collector:
        if rebar.LookupParameter(parameter_name) == expected_value:
            rebar_ids.Add(rebar.Id)
    return rebar_ids


class MainWindow(WPFWindow):
    def __init__(self, xaml_file):
        WPFWindow.__init__(self, xaml_file)
        self.cmbBox.ItemsSource = default_parameters
        self.ShowDialog()

    def window_close(self, sender, args):
        """Closes opened xaml window."""
        self.Close()

    def select_by_parameter(self):
        """Selects rebars with given parameters"""
        parameter_name = self.cmbBox.SelectedItem
        parameter_value = self.txtBoxValue.Text

        # TODO: This can be handled non invasively e.g. with message box warning
        if parameter_name is None or len(parameter_name) < 1:
            raise ValueError
        if parameter_value is None:
            raise ValueError

        ids = get_rebar_ids_by_parameter(
            parameter_name, parameter_value, rebar_collector
        )
        uidoc.Selection.SetElementIds(ids)
        self.Close()


window = MainWindow(xaml_file=xaml_file)
