from Autodesk.Revit import DB
import math


class RebarCoG:
    def __init__(self, rebar_collector):
        """Calculates rebar CoG
        Arguments:
        rebar_collector: DB.FilteredElementCollector
        """
        self.rebar_collector = rebar_collector
        self.multiplanaroption = DB.Structure.MultiplanarOption.IncludeAllMultiplanarCurves

    def _is_rebar_group(self, rebar_object):
        """Checks if object is a rebar group
        Arg:
            rebar_object: DB.Structure.Rebar"""
        n_bars = rebar_object.NumberOfBarPositions
        if n_bars > 1:
            return True
        else:
            return False

    def _compute_segment_centroid(self, curve, diameter, index):
        """Computes segment centroid.
        Arguments:
        curve (DB.Line or DB.Curve)
        diameter (float)
        Returns:
        list[centroid, mass]
            where:
            centroid(list) - [x(float), y(float), z(float)] in mm
            mass - float value in kg
        """
        # Conversion from feet to mm
        k = 304.8
        r_o = 7.85e-6  # kg/mm3
        r = diameter / 2  # mm
        area = math.pi * r**2
        length = curve.Length * k
        volume = area * length
        mass = volume * r_o
        if isinstance(curve, DB.Line):
            sp_X = curve.GetEndPoint(0).X * k
            sp_Y = curve.GetEndPoint(0).Y * k
            sp_Z = curve.GetEndPoint(0).Z * k
            ep_X = curve.GetEndPoint(1).X * k
            ep_Y = curve.GetEndPoint(1).Y * k
            ep_Z = curve.GetEndPoint(1).Z * k
            cp_X = (sp_X + ep_X) / 2
            cp_Y = (sp_Y + ep_Y) / 2
            cp_Z = (sp_Z + ep_Z) / 2
            # centroid = DB.XYZ(cp_X, cp_Y, cp_Z)
            centroid = [cp_X, cp_Y, cp_Z]
            return centroid, mass
        if isinstance(curve, DB.Arc):
            arc_radius = curve.Radius * k
            arc_center_X = curve.Center.X * k
            arc_center_Y = curve.Center.Y * k
            arc_center_Z = curve.Center.Z * k
            # Midpoint of arc
            a_mp_X = curve.Evaluate(0.5, True).X * k
            a_mp_Y = curve.Evaluate(0.5, True).Y * k
            a_mp_Z = curve.Evaluate(0.5, True).Z * k
            # Calculate 'x' coordinate of centroid for arc
            circumference = 2 * math.pi * arc_radius
            theta = math.radians(length / circumference * 360)
            alpha = theta / 2
            # Scalar value [mm]
            radius2 = arc_radius + r
            radius1 = arc_radius - r
            # TODO: Check results with p computed for annular sector, is it better?
            p = (2 * math.sin(alpha) / (3 * alpha)) * (radius2**3 - radius1**3) / (radius2**2 - radius1**2)
            # p = arc_radius * math.sin(alpha) / alpha
            # Calculate a line vector and unit vector between center and midpoint
            v_X = a_mp_X - arc_center_X
            v_Y = a_mp_Y - arc_center_Y
            v_Z = a_mp_Z - arc_center_Z
            # Calculate line length
            v_L = math.sqrt(v_X**2 + v_Y**2 + v_Z**2)
            # Calculate unit vector
            if v_L != 0:
                u_X = v_X / v_L
                u_Y = v_Y / v_L
                u_Z = v_Z / v_L
            else:
                raise ZeroDivisionError
            # Centroid point
            cp_X = arc_center_X + p * u_X
            cp_Y = arc_center_Y + p * u_Y
            cp_Z = arc_center_Z + p * u_Z
            # centroid = DB.XYZ(cp_X, cp_Y, cp_Z)
            centroid = [cp_X, cp_Y, cp_Z]  # OK
            return centroid, mass

    def _compute_centroid(self, list_of_centroids, list_of_masses):
        """
        Arguments:
        List of centroids - centroid of each segment of bar
        List of masses - mass for each segment of bar
        Structure:
        List of centroids [x,y,z], [x,y,z],
        List of masses [M1, M2, M3]
        Returns:
        list of coordinates of CoG [x, y, z]"""

        coord_mass = [[list_of_masses[i] * j for j in sub] for i, sub in enumerate(list_of_centroids)]
        # coord_mass = [[xM1, yM1,zM1], [xM2, yM2, zM2], ...]
        sum_xm = sum(i[0] for i in coord_mass)
        sum_ym = sum(i[1] for i in coord_mass)
        sum_zm = sum(i[2] for i in coord_mass)
        sum_mass = sum(list_of_masses)
        if sum_mass != 0:
            cog_x = sum_xm / sum_mass
            cog_y = sum_ym / sum_mass
            cog_z = sum_zm / sum_mass
            return [cog_x, cog_y, cog_z], sum_mass
        else:
            raise ZeroDivisionError

    def _get_rebar_diam(self, rebar):
        diam = rebar.LookupParameter("Bar Diameter")
        return diam.AsDouble() * 304.8

    def _get_existing_bar_index(self, bar_object):
        """Checks if rebar exists at given position (can be hidden or removed)
        Arguments:
            rebar_object: DB.Structure.Rebar
        Returns:
            indexes(list(int))"""
        indexes = []
        n_bars = bar_object.NumberOfBarPositions
        for i in range(0, n_bars):
            if bar_object.DoesBarExistAtPosition(i):
                indexes.append(i)
        return indexes

    def get_cog(self):
        all_bar_centroids = []
        all_bar_masses = []
        for rebar in self.rebar_collector:
            rebar_diam = self._get_rebar_diam(rebar)
            # Check if rebar object is group
            if self._is_rebar_group(rebar_object=rebar):
                # Compute centroid for each bar in group
                for i in self._get_existing_bar_index(rebar):
                    if (
                        rebar.DistributionType == DB.Structure.DistributionType.Uniform
                        or DB.Structure.DistributionType.VaryingLength
                    ):
                        rebar_curve = rebar.GetTransformedCenterlineCurves(
                            False, False, False, self.multiplanaroption, i
                        )
                    else:
                        rebar_curve = rebar.GetCenterlineCurves(False, False, False, self.multiplanaroption, i)
                    # Compute centroid for each segment
                    centroids = []
                    masses = []
                    for curve in rebar_curve:
                        segment_centroid = self._compute_segment_centroid(curve, rebar_diam, i)
                        centroids.append(segment_centroid[0])
                        masses.append(segment_centroid[1])
                        # Compute centroid and total mass for each bar
                    cog = self._compute_centroid(centroids, masses)[0]
                    mass = self._compute_centroid(centroids, masses)[1]
                    # Add to global list
                    all_bar_centroids.append(cog)
                    all_bar_masses.append(mass)
            else:  # single rebar object
                index = 0
                # Get bar curves
                rebar_curve = rebar.GetCenterlineCurves(False, False, False, self.multiplanaroption, index)
                # Compute centroid for each segment
                centroids = []
                masses = []
                for curve in rebar_curve:
                    segment_centroid = self._compute_segment_centroid(curve, rebar_diam, index)
                    centroids.append(segment_centroid[0])
                    masses.append(segment_centroid[1])
                    # Compute centroid and total mass for each bar
                cog = self._compute_centroid(centroids, masses)[0]
                mass = self._compute_centroid(centroids, masses)[1]
                # Add to global list
                all_bar_centroids.append(cog)
                all_bar_masses.append(mass)
        final_cog = self._compute_centroid(all_bar_centroids, all_bar_masses)[0]
        total_mass = self._compute_centroid(all_bar_centroids, all_bar_masses)[1]
        return final_cog, total_mass
