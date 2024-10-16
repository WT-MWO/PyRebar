__doc__ = "Select all rebars in view by chosen Parameter."
__title__ = "Select by Parameter"
__author__ = "Wolinski"

from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from pyrevit import script
from pyrevit.forms import WPFWindow
from System.Collections.Generic import List
from System import String
from rebar_selector import RebarSelector
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView


xaml_file = script.get_bundle_file("view.xaml")

default_parameters = ["Diameter", "Partition", "Comments", "Schedule Mark"]

# parameters_lst = List[String]()

# for parameter in default_parameters:
#     parameters_lst.Add(parameter)


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
    # TODO: handle the units if parameter is the "name"
    # lower both param value and expected value? to make sure its not case sensitive?
    rebar_ids = List[DB.ElementId]()
    for rebar in rebar_collector:
        if rebar.LookupParameter(parameter_name).AsString() == expected_value:
            rebar_ids.Add(rebar.Id)
    return rebar_ids


class MainWindow(WPFWindow):
    def __init__(self, xaml_file):
        WPFWindow.__init__(self, xaml_file)
        # TODO: manual input in the combobox does not work
        self.cmbBox.ItemsSource = default_parameters
        self.ShowDialog()

    def window_close(self, sender, args):
        """Closes opened xaml window."""
        self.Close()

    def select_rebar_by_parameter(self, sender, args):
        """Selects rebars with given parameters"""
        parameter_name = self.cmbBox.SelectedItem
        parameter_value = self.txtBoxValue.Text  # try this with text value?
        if parameter_name is None or len(parameter_name) < 1:
            forms.alert("Parameter name field cannot be empty", ok=True)
        if parameter_value is None:
            forms.alert("Parameter value field cannot be empty", ok=True)
        ids = get_rebar_ids_by_parameter(
            rebar_collector, parameter_name, parameter_value
        )
        uidoc.Selection.SetElementIds(ids)
        self.Close()

    def ComboBox_TextChanged(self, sender, args):
        return self.cmbBox.Text


window = MainWindow(xaml_file=xaml_file)
