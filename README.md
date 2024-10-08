# PyRebar
[PyRevit](https://github.com/pyrevitlabs/pyRevit/tree/master) extension for Autodesk Revit :registered: reinforcement modelling. 
This is a toolkit of useful scripts increasing productivity during reinforcement detailing.

![image](https://github.com/user-attachments/assets/c11f6705-ff08-4fcd-ac93-23397733875c)


## Features
Most of the functions use **flexible selection** - you can preselect rebars to execute command only on them, or script is executed on all rebars in view if nothing is selected.

### Summary
#### View tab
- **Unobscure bars** - Works for all reinforcement bars in current view.
- **Obscure bars**  - Works for all reinforcement bars in current view.

#### Selection tab
- **Same Number** - Selects all rebars with the same number within the same partition. :warning: Requires preselection of rebar.
- **Select by Parameter** - (WIP) :construction: selects all rebar objects with assigned parameter.
- **Select Rebar Type** - Selects all rebars in view by chosen type.

#### Modify tab
- **Reverse hook** - Reverse hook :warning: This function works only when 'Include hooks in Rebar Shape definition' is disabled in Reinforcement Settings.

#### Query tab
- **RebarCoG** - Calculates the Centre of Gravity of selected rebar or rebars. The CoG can be visualized with small Sphere generic model. CoG is returned in mm, with respect to project base point. The total mass is returned in $kg$.
- **Rebar ratio** - Calculates rebar mass/concrete volume ratio in $\frac{kg}{m^3}$. User is prompted to select a formwork, all reinforcement in selected element is taken into account. In case of multiple elements selected the masses and volumes are added to eachother.
- **Get mass** - Calculates mass of the selected rebar element(s). The calculation is based on equation: $\frac{\pi d^2}{4} L_{bar }$ , where $d$ is diameter, $L_{bar}$ is total bar length calculated by Revit. Value is returned in $kg$.



