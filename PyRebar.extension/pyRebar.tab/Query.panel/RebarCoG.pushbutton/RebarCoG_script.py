__doc__ = "Calculate CoG of selected bars."
__title__ = "Rebar CoG"
__author__ = "MWolinski"
import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from rebar_selector import RebarSelector
from .rebar_cog import RebarCoG
from .visualize_point import visualize_point

ROUNDING = 3

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

rs = RebarSelector(doc, uidoc)
rebar_collector = rs.get_rebars()

rebar_cog = RebarCoG(rebar_collector)
cog = rebar_cog.get_cog()


final_cog = cog[0]
total_mass = cog[1]

X = round(final_cog[0], ROUNDING)
Y = round(final_cog[1], ROUNDING)
Z = round(final_cog[2], ROUNDING)

cog_text = "CoG: X= {0} mm, Y= {1} mm, Z= {2} mm".format(str(X), str(Y), str(Z))
mass_text = "Total mass: " + str(round(total_mass, ROUNDING))
print(cog_text)
print(mass_text)

centroid = DB.XYZ(final_cog[0], final_cog[1], final_cog[2])

diameter = 2.0

visualize_point(doc, centroid, diameter)
