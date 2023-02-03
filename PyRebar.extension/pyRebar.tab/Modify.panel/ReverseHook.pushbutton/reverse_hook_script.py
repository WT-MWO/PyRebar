__doc__ = """Reverse 'Hook at Start' and 'Hook at End' of the rebar.
This tool doesn't work when you pick Shape Driven rebar and
'Include hooks in Rebar Shape definition' option is enabled."""

__title__ = "Reverse Hook"
__author__ = "Wolinski"
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

# import clr

# clr.AddReference("System.Windows.Forms")
# clr.AddReference("Ironpython.Wpf")
from pyrevit import script

# import wpf
# from System import Windows
from .....lib.warning_view import WarningWindow
from .....lib.rebar_selector import RebarSelector

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

xaml_file = script.get_bundle_file("warning.xaml")


def can_reverse(rebar):
    if rebar.IsRebarShapeDriven() and defines_hooks:
        return False
    elif rebar.IsRebarFreeForm:
        return True
    else:
        print("Unknown rebar type")


# Get reinforcement settings
settings = DB.Structure.ReinforcementSettings.GetReinforcementSettings(doc)
defines_hooks = settings.RebarShapeDefinesHooks

# Get selected object
rs = RebarSelector(doc, uidoc)
elements = rs.get_rebars()

# Handling transactions
tg = TransactionGroup(doc, "ReverseHook")
tg.Start()


# TODO: Make this flexible and working for single bars and rebar groups.
not_reversed_rebars = []

for rebar in elements:
    if can_reverse(rebar):
        orient0 = rebar.GetHookOrientation(0)
        orient1 = rebar.GetHookOrientation(1)
        left = DB.Structure.RebarHookOrientation.Left
        right = DB.Structure.RebarHookOrientation.Right
        print(orient0)
        print(orient1)
        t = Transaction(doc, "Reverse")
        t.Start()
        if orient0 == right:
            rebar.SetHookOrientation(0, left)
        elif orient0 == left:
            rebar.SetHookOrientation(0, right)
        if orient1 == right:
            rebar.SetHookOrientation(1, left)
        elif orient1 == left:
            rebar.SetHookOrientation(1, right)
        t.Commit()
    else:
        number = rebar.LookupParameter("Number").AsString()
        not_reversed_rebars.append(number)

tg.Assimilate()

if len(not_reversed_rebars > 0):
    message = "This tool doesn't work when you pick Shape Driven rebar and\
    'Include hooks in Rebar Shape definition' option is enabled.\
    Numbers of rebars not modified: {}".format(
        not_reversed_rebars
    )
    WarningWindow(
        xaml_file=xaml_file,
        label_text="Operation failed!",
        text_content=message,
    ).ShowDialog()
