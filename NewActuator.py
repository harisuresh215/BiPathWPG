from typing import Any
import numpy as np
import os
import sys
import time


#-------------------------------------------------------------------------
# class material
#-------------------------------------------------------------------------
class material:
    def __init__(self, density, maxAllowableStressMPa = 400, bhn = 2, youngsModulus = 10):
        self.maxAllowableStressMPa = maxAllowableStressMPa
        self.bhn = bhn
        self.youngsModulus = youngsModulus
        self.density = density

#-------------------------------------------------------------------------
# class bearings
#-------------------------------------------------------------------------
class bearings_discrete:
    def __init__(self,idRequiredMM):
        # Bearing dataset entered according to e1102 in [idMM,odMM,widthMM,massKG] format pg no b10-12
        self.data_bearings = [[10,19,5,0.005],[12,21,5,0.006],[15,24,5,0.007],[17,26,5,0.007],[20,32,7,0.017],[25,37,7,0.021],[28,52,12,0.096],[30,42,7,0.024],[32,58,13,0.122],[35,47,7,0.027],[40,52,7,0.031],[45,58,7,0.038],[50,65,7,0.050],[55,72,9,0.081],[60,78,10,0.103],[65,85,10,0.128],[70,90,10,0.134],[75,95,10,0.149],[80,100,10,0.151],[85,110,13,0.263],
                              [90,115,13,0.276],[95,120,13,0.297],[100,125,13,0.31],[105,130,13,0.324],[110,140,16,0.497],[120,150,16,0.537],[130,165,18,0.758],[140,170,18,0.832],[150,190,20,1.15],[160,200,20,1.23]]
        self.idRequiredMM = idRequiredMM
        self.indexBearing =   0
        while (self.data_bearings[self.indexBearing][0] < self.idRequiredMM):
            self.indexBearing +=1
        # # Extract columns
        # data_bearings = np.array(self.data_bearings)
        # self.d = data_bearings[:, 0].reshape(-1, 1)  # Inner diameters
        # self.D = data_bearings[:, 1]  # Outer diameters
        # self.B = data_bearings[:, 2]  # Widths
        # self.L = data_bearings[:, 3]  # Load ratings

        # # Create linear regression models
        # self.lr_D = LinearRegression().fit(self.d, self.D)
        # self.lr_B = LinearRegression().fit(self.d, self.B)
        # self.lr_L = LinearRegression().fit(self.d, self.L)

    def getBearingIDMM(self):
        return self.data_bearings[self.indexBearing][0]
    
    def getBearingODMM(self):
        return self.data_bearings[self.indexBearing][1]
    
    def getBearingWidthMM(self):
        return self.data_bearings[self.indexBearing][2]
    
    def getBearingMassKG(self):
        return self.data_bearings[self.indexBearing][3]

    # # Continuous functions
    # def getBearingIDMM(self):
    #     return self.idRequiredMM  # Identity function for d

    # def getBearingODMM(self):
    #     return np.round(self.lr_D.predict(np.array([[self.idRequiredMM]]))[0],3)

    # def getBearingWidthMM(self):
    #     return np.round(self.lr_B.predict(np.array([[self.idRequiredMM]]))[0],2)

    # def getBearingMassKG(self):
    #     return np.round(self.lr_L.predict(np.array([[self.idRequiredMM]]))[0],3)

class bearings_continuous:
    def __init__(self,idRequiredMM):
        # Bearing dataset entered according to e1102 in [idMM,odMM,widthMM,massKG] format pg no b10-12
        self.data_bearings = [[25,37,7,0.021],
                              [28,52,12,0.096],
                              [30,42,7,0.024],
                              [32,58,13,0.122],
                              [35,47,7,0.027],
                              [40,52,7,0.031],
                              [45,58,7,0.038],
                              [50,65,7,0.050],
                              [55,72,9,0.081],
                              [60,78,10,0.103],
                              [65,85,10,0.128],
                              [70,90,10,0.134],
                              [75,95,10,0.149],
                              [80,100,10,0.151],
                              [85,110,13,0.263],
                              [90,115,13,0.276],
                              [95,120,13,0.297],
                              [100,125,13,0.31],
                              [105,130,13,0.324],
                              [110,140,16,0.497],
                              [120,150,16,0.537],
                              [130,165,18,0.758],
                              [140,170,18,0.832],
                              [150,190,20,1.15],
                              [160,200,20,1.23]]
        self.idRequiredMM = idRequiredMM
        self.indexBearing =   0

        # while (self.data_bearings[self.indexBearing][0] < self.idRequiredMM):
        #     self.indexBearing +=1
        # # Extract columns
        # data_bearings = np.array(self.data_bearings)
        # self.d = data_bearings[:, 0].reshape(-1, 1)  # Inner diameters
        # self.D = data_bearings[:, 1]  # Outer diameters
        # self.B = data_bearings[:, 2]  # Widths
        # self.L = data_bearings[:, 3]  # Load ratings

        # # Create linear regression models
        # self.lr_D = LinearRegression().fit(self.d, self.D)
        # self.lr_B = LinearRegression().fit(self.d, self.B)
        # self.lr_L = LinearRegression().fit(self.d, self.L)

    def getBearingIDMM(self):
        return self.idRequiredMM
        return self.data_bearings[self.indexBearing][0]
    
    def getBearingODMM(self):
        a_OD = 1.180682635961756 
        b_OD = 8.566071759021273
        Bearing_OD = a_OD * self.idRequiredMM + b_OD
        return Bearing_OD
        return self.data_bearings[self.indexBearing][1]
    
    def getBearingWidthMM(self):
        a_widths  = 0.09293718515472396
        b_widths  = 4.617962372776808

        Bearing_Width = a_widths * self.idRequiredMM + b_widths
        return Bearing_Width
        return self.data_bearings[self.indexBearing][2]
    
    def getBearingMassKG(self):
        a_weights = 8.4777526725202e-05
        b_weights = -0.006890846402773096
        c_weights = 0.18849936113412308

        Bearing_Weight = a_weights * self.idRequiredMM * self.idRequiredMM + b_weights * self.idRequiredMM + c_weights
        return Bearing_Weight
        return self.data_bearings[self.indexBearing][3]

#-------------------------------------------------------------------------
# Nuts and bolts class
#-------------------------------------------------------------------------
class nuts_and_bolts_dimensions:
    def __init__(self, bolt_dia, bolt_type="socket_head"):
        self.bolt_dia  = bolt_dia
        self.bolt_type = bolt_type
        self.bolt_head_dia, self.bolt_head_height = self.get_bolt_head_dimensions(diameter=self.bolt_dia, bolt_type=self.bolt_type)
        self.nut_width_across_flats, self.nut_thickness = self.get_nut_dimensions(diameter=self.bolt_dia)

    def get_bolt_head_dimensions(self, diameter, bolt_type="socket_head"):
        diameter = float(diameter)

        socket_head_table = {
            1.6: {"d2": (3.00), "k": (1.60)},
            2.0: {"d2": (3.80), "k": (2.00)},
            2.5: {"d2": (4.50), "k": (2.50)},
            3.0: {"d2": (5.50), "k": (3.00)},
            4.0: {"d2": (7.00), "k": (4.00)},
            5.0: {"d2": (8.50), "k": (5.00)},
            6.0: {"d2": (10.00), "k": (6.00)},
            8.0: {"d2": (13.00), "k": (8.00)},
            10.0: {"d2": (16.00), "k": (10.00)}
        }

        # Only dk is stored for CSK, t is calculated as (dk - d) / 2
        csk_table = {
            3.0: {"dk": 6},
            4.0: {"dk": 8},
            5.0: {"dk": 10},
            6.0: {"dk": 12},
            8.0: {"dk": 16},
            10.0: {"dk": 20},
            12.0: {"dk": 24},
            16.0: {"dk": 30},
            20.0: {"dk": 36}
        }

        if bolt_type == "socket_head":
            spec = socket_head_table.get(diameter)
            if not spec:
                raise ValueError(f"Socket head bolt M{diameter} not found.")
            return [spec["d2"], spec["k"]]  # Return d2, k

        elif bolt_type == "CSK":
            spec = csk_table.get(diameter)
            if not spec:
                raise ValueError(f"CSK bolt M{diameter} not found.")
            dk = spec["dk"]
            t = (dk - diameter) / 2
            return [dk, round(t, 3)]  # Rounded for clarity

        else:
            raise ValueError("bolt_type must be 'socket_head' or 'CSK'")

    def get_nut_dimensions(self, diameter):
        diameter = float(diameter)

        nut_table = {
            2.0: {"width_across_flats": 4, "height": 1.6},
            2.5: {"width_across_flats": 5, "height": 2},
            3.0: {"width_across_flats": 5.5, "height": 2.4},
            4.0: {"width_across_flats": 7, "height": 3.2},
            5.0: {"width_across_flats": 8, "height": 4},
            6.0: {"width_across_flats": 10, "height": 5},
            7.0: {"width_across_flats": None, "height": 5.5},  # ISO not defined
            8.0: {"width_across_flats": 13, "height": 6.5},
            10.0: {"width_across_flats": 16, "height": 8},
            12.0: {"width_across_flats": 18, "height": 10},
            14.0: {"width_across_flats": 21, "height": 13},
            16.0: {"width_across_flats": 24, "height": 13},
            18.0: {"width_across_flats": 27, "height": 15},
            20.0: {"width_across_flats": 30, "height": 16},
            24.0: {"width_across_flats": 36, "height": 18},
            27.0: {"width_across_flats": 40, "height": 20},
            30.0: {"width_across_flats": 43, "height": 22},
        }

        spec = nut_table.get(diameter)
        if not spec:
            raise ValueError(f"No nut data found for bolt diameter M{diameter}")

        width_across_flats = spec["width_across_flats"]
        height = spec["height"]

        return [width_across_flats, height]

#=========================================================================
# Motor class
#=========================================================================
class motor:
    def __init__(self, 
                 maxMotorAngVelRPM     = 1190, # RPM
                 maxMotorTorque        = 8.83, # Nm
                 maxMotorPower         = 8.83 * 1190 * 2*np.pi/60, # W 
                 motorMass             = 0.778, # KG
                 motorDia              = 106.8, # mm
                 motorLength           = 47.6,  # mm
                 motor_mount_hole_PCD       = 32,
                 motor_mount_hole_dia       = 4,
                 motor_mount_hole_num       = 4,
                 motor_output_hole_PCD      = 23,
                 motor_output_hole_dia      = 4,
                 motor_output_hole_num      = 4,
                 wire_slot_dist_from_center = 30,
                 wire_slot_length           = 10,
                 wire_slot_radius           = 4,
                 motorName             = "U12"):
        
        self.motorName                  = motorName
        self.maxMotorAngVelRPM          = maxMotorAngVelRPM
        self.maxMotorAngVelRadPerSec    = maxMotorAngVelRPM * (2 * np.pi / 60)
        self.maxMotorTorque             = maxMotorTorque
        self.maxMotorPower              = maxMotorPower
        self.massKG                     = motorMass     # kg
        self.motorDiaMM                 = motorDia      # mm #TODO: make use of this parameter
        self.motorLengthMM              = motorLength   # mm #TODO: make use of this parameter
        self.motor_mount_hole_PCD       = motor_mount_hole_PCD 
        self.motor_mount_hole_dia       = motor_mount_hole_dia
        self.motor_mount_hole_num       = motor_mount_hole_num
        self.motor_output_hole_PCD      = motor_output_hole_PCD 
        self.motor_output_hole_dia      = motor_output_hole_dia
        self.motor_output_hole_num      = motor_output_hole_num
        self.wire_slot_dist_from_center = wire_slot_dist_from_center 
        self.wire_slot_length           = wire_slot_length 
        self.wire_slot_radius           = wire_slot_radius

    # Maximum motor angular velocity in rad/s
    def getMaxMotorAngVelRadPerSec(self):
        return self.maxMotorAngVelRadPerSec
    
    # Maximum motor power in W
    def getMaxMotorPower(self):
        return self.maxMotorPower
    
    # Maximum motor torque in Nm
    def getMaxMotorTorque(self):
        return self.maxMotorTorque
    
    # Mass of the motor in kg
    def getMassKG(self):
        return self.massKG
    
    #dimension of the motor in MM
    def getDiaMM(self):
        return self.motorDiaMM
    
    def getLengthMM(self):
        return self.motorLengthMM
    
    #dimensions of Stator
    def getStatorIDMM(self):
        return self.motorStatorIDMM
    
    def getStatorODMM(self):
        return self.motorStatorODMM
    
    def getStatorHeight(self):
        return self.motorStatorHeightMM
    
    # Print the motor parameters
    def printParameters(self):
        print("Maximum motor angular velocity = ", self.maxMotorAngVelRPM, " RPM")
        print("Maximum motor power = ", self.maxMotorPower, " W")
        print("Maximum motor torque = ", self.maxMotorTorque, " Nm")
        print("Maximum motor angular velocity = ", self.maxMotorAngVelRadPerSec, " rad/s")
        print("Mass of the motor = ", self.massKG, " kg")
        print ('Diameter of the motor = ', self.motorDiaMM, ' mm')
        print( " Length of the motor = ", self.motorLengthMM, ' mm')
        if (self.motorStatorIDMM != 0 and self.motorStatorODMM != 0 and self.motorStatorHeightMM !=0):
            print (' Inner Diameter of Stator = ', self.motorStatorIDMM, ' mm')
            print (' Outer Diameter of Stator = ', self.motorStatorODMM, ' mm')
            print (' Height of Stator = ', self.motorStatorIDMM, ' mm')

#=========================================================================
# Motor Driver class
#=========================================================================
class motor_driver:
    def __init__(self, driver_name, motor_driver_data):
        self.driver_name                          = driver_name
        self.driver_upper_holes_dist_from_center  = motor_driver_data["driver_upper_holes_dist_from_center"]
        self.driver_lower_holes_dist_from_center  = motor_driver_data["driver_lower_holes_dist_from_center"]
        self.driver_side_holes_dist_from_center   = motor_driver_data["driver_side_holes_dist_from_center"]
        self.driver_mount_holes_dia               = motor_driver_data["driver_mount_holes_dia"]
        self.driver_mount_inserts_OD              = motor_driver_data["driver_mount_inserts_OD"]
        self.driver_mount_thickness               = motor_driver_data["driver_mount_thickness"]
        self.driver_mount_height                  = motor_driver_data["driver_mount_height"]

        # self.print_vars()
    
    def print_vars(self):
        print("driver_name:", self.driver_name)
        print("driver_upper_holes_dist_from_center: ", self.driver_upper_holes_dist_from_center)
        print("driver_lower_holes_dist_from_center: ", self.driver_lower_holes_dist_from_center)
        print("driver_side_holes_dist_from_center: ", self.driver_side_holes_dist_from_center)
        print("driver_mount_holes_dia: ", self.driver_mount_holes_dia)
        print("driver_mount_inserts_OD: ", self.driver_mount_inserts_OD)
        print("driver_mount_thickness: ", self.driver_mount_thickness)
        print("driver_mount_height: ", self.driver_mount_height)
        print("---")

#=========================================================================
#-------------------------------------------------------------------------
# Bipath3K - Planetary Gearbox (Bipathwolfrom Planetary Gearbox)
#-------------------------------------------------------------------------
class bipathwolfromPlanetaryGearbox:
    def __init__(self,
                 design_parameters,
                 gear_standard_parameters,
                 Ns      = 20, # Teeth: sun gear
                 NpBig   = 40, # Teeth: bigger planet gear
                 NpSmall = 20, # Teeth: smaller planet gear
                 NrBig   = 80, # Teeth: bigger ring gear
                 NrSmall = 40, # Teeth: smaller ring gear
                 numPlanet                 = 2,
                 moduleBig                 = 0.5,
                 moduleSmall               = 0.5,
                 densityGears              = 7850,
                 densityStructure          = 2710,
                 fwSunMM                   = 5.0,
                 fwPlanetBigMM             = 5.0,
                 fwPlanetSmallMM           = 5.0,
                 fwRingBigMM               = 5.0,
                 fwRingSmallMM             = 5.0,
                 maxGearAllowableStressMPa = 400):
        
        #-----------------------------------
        # Discrete Optimizaition Variables 
        #-----------------------------------
        self.Ns          = Ns
        self.NpBig       = NpBig
        self.NpSmall     = NpSmall
        self.NrBig       = NrBig
        self.NrSmall     = NrSmall
        self.numPlanet   = numPlanet
        self.moduleBig   = moduleBig
        self.moduleSmall = moduleSmall
        
        #-----------------------------------
        # Material Properties
        #-----------------------------------
        self.densityGears              = densityGears
        self.densityStructure          = densityStructure
        self.maxGearAllowableStressMPa = maxGearAllowableStressMPa         # MPa
        self.maxGearAllowableStressPa  = maxGearAllowableStressMPa * 10**6 # Pa
        
        #-------------------------------
        # Facewidths
        #-------------------------------
        self.fwSunMM         = fwSunMM
        self.fwPlanetBigMM   = fwPlanetBigMM
        self.fwPlanetSmallMM = fwPlanetSmallMM
        self.fwRingBigMM     = fwRingBigMM
        self.fwRingSmallMM   = fwRingSmallMM
        self.fwFloatingSunMM = 5.0
        #------------------------------
        # Gearbox parameters
        #------------------------------
        self.mu               = gear_standard_parameters["coefficientOfFriction"] # 0.3 # Gear standard parameters
        self.pressureAngleDEG = gear_standard_parameters["pressureAngleDEG"]      # 20  # deg
        
        self.planetMinDistanceMM  = design_parameters["planetMinDistanceMM"]    # mm
        self.ringRadialWidthSmall = design_parameters["ringRadialWidthMMSmall"] # ringRadialWidthSmall
        self.ringRadialWidthBig   = design_parameters["ringRadialWidthMMBig"]   # ringRadialWidthBig
        # self.carrierWidthMM     = carrierWidthMM
        self.floatingSunMinTeeth    = design_parameters["floating_sun_min_teeth"]
        self.floatingSunMinWallMM   = design_parameters["floating_sun_min_wall"]
        self.floatingSunBoreClrMM   = design_parameters["floating_sun_bore_clearance"]
        self.idlerMinGapMM          = design_parameters["idler_planet_min_gap"]
        self.mainSunToothedInPlane2 = design_parameters["main_sun_plane2_toothed"]
        
        #------------------------------
        # Profile Shift Coefficients TODO: Remove this
        #------------------------------
        self.profileShiftCoefficientRingSmall   = 0.0
        self.profileShiftCoefficientRingBig     = 0.0
        self.profileShiftCoefficientPlanetBig   = self.profileShiftCoefficientRingBig
        self.profileShiftCoefficientPlanetSmall = self.profileShiftCoefficientRingSmall
        self.profileShiftCoefficientSun         = -self.profileShiftCoefficientPlanetBig
    # FIXME  :recheck constrainsts  
    def geometricConstraint(self):
        return (((self.Ns + self.NpBig) * self.moduleBig == (self.NrSmall - self.NpSmall) * self.moduleSmall) and
                ((self.Ns + 2 * self.NpBig) == (self.NrBig)) and
                (self.NrBig * self.moduleBig > self.NrSmall * self.moduleSmall))
        
    def meshingConstraint(self):
        # TODO: VERIFY THIS WITH EXAMPLE AND SELF ANALYSIS
        oldrule = ((self.Ns % self.numPlanet == 0) and (self.NrSmall % self.numPlanet == 0) and (self.NrBig % self.numPlanet == 0))
        newrule = (((self.NrSmall + self.NpSmall) % self.numPlanet == 0))
        return oldrule and newrule
    
    def noPlanetInterferenceConstraint(self):
         oldrule = 2*(self.Ns + self.NpBig)*self.moduleBig*np.sin(np.pi/self.numPlanet) >= 2*self.moduleBig*self.NpBig + self.planetMinDistanceMM
         m, n, Ns2 = self.moduleBig, self.numPlanet, self.getFloatingSunTeeth()
         if Ns2 < self.floatingSunMinTeeth:
             return False
         Rc      = (self.Ns + self.NpBig) * m / 2                         # radius of the circle the planets sit on
         Rtip    = self.NpSmall * self.moduleSmall / 2 + self.moduleSmall # small planet tip radius
         gap_ok  = (2*Rc*np.sin(np.pi/(2*n)) - 2*Rtip) >= self.idlerMinGapMM
         sun_r   = self.Ns*m/2 + (m if self.mainSunToothedInPlane2 else -1.25*m)
         root_fs = Ns2*m/2 - 1.25*m
         wall_ok = (root_fs - sun_r) >= (self.floatingSunMinWallMM + self.floatingSunBoreClrMM)
         return oldrule and gap_ok and wall_ok
    

    def getMassKG(self):
        # Volume of the Sun gear
        fwSunM            = (self.fwSunMM / 1000.0)
        fwPlanetBigM      = (self.fwPlanetBigMM / 1000.0)
        fwPlanetSmallM    = (self.fwPlanetSmallMM / 1000.0)
        fwRingSmallM      = (self.fwRingSmallMM / 1000.0)
        fwRingBigM        = (self.fwRingBigMM / 1000.0)
        carrierWidthM     = (self.carrierWidthMM / 1000.0)

        sunVolume         = np.pi * fwSunM * (self.getPCRadiusSunM()**2)
        planetBigVolume   = np.pi * fwPlanetBigM * (self.getPCRadiusPlanetBigM()**2)
        planetSmallVolume = np.pi * fwPlanetSmallM * (self.getPCRadiusPlanetSmallM()**2)
        ringSmallVolume   = np.pi * fwRingSmallM * (self.getOuterRadiusRingSmallM()**2 - self.getPCRadiusRingSmallM()**2)
        ringBigVolume     = np.pi * fwRingBigM * (self.getOuterRadiusRingBigM()**2 - self.getPCRadiusRingBigM()**2)
        carrierVolume     =  2 * np.pi * carrierWidthM * (self.getCarrierRadiusM()**2)

        # Total mass of the compound planetary gearbox
        combinedGearVolume = sunVolume + (self.numPlanet * (planetBigVolume + planetSmallVolume)) + ringBigVolume + ringSmallVolume
        TotalMassKG        = (combinedGearVolume * self.densityGears + carrierVolume * self.densityStructure)
        return TotalMassKG

    def gearRatio(self):
        GR1 = 2*self.NrSmall*self.NpBig / (self.Ns * (self.NpBig - self.NpSmall))
        GR2 = ((self.Ns + self.NrBig) * self.NpBig * self.NrSmall) / (self.Ns * (self.NpBig * self.NrSmall - self.NpSmall * self.NrBig))
        if GR1 == GR2:
            pass
        else:
            print("ERROR: Gear ratio mismatch")
        return GR1
    
    #======================================
    # Efficiency Calculations
    #======================================
    #--------------------------------------
    # Utility Functions
    #--------------------------------------
    def inverse_involute(self,inv_alpha):
        # This is an approximation of the inverse involute function
        alpha  = ((3*inv_alpha)**(1/3) - 
                  (2*inv_alpha)/5 + 
                  (9/175)*(3)**(2/3)*inv_alpha**(5/3) - 
                  (2/175)*(3)**(1/3)*(inv_alpha)**(7/3) - 
                  (144/67375)*(inv_alpha)**(3) + 
                  (3258/3128125)*(3)**(2/3)*(inv_alpha)**(11/3) - 
                  (49711/153278125)*(3)**(1/3)*(inv_alpha)**(13/3))
        return alpha

    def involute(self,alpha):
        return (np.tan(alpha) - alpha)

    # Define the differentiable quadratic approximation of the min function
    def quadratic_min(self, a, b, k=0.01):
        return (a + b - np.sqrt((a - b)**2 + k**2)) / 2

    #-----------------------------------------
    # Gear tooth profile parameters
    #-----------------------------------------
    def getPressureAngleRad(self):
        return self.pressureAngleDEG * np.pi / 180  # Pressure angle in radians

    def getWorkingPressureAngle(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        #---------------------------------
        # Pressure Angle
        #---------------------------------
        alpha = self.getPressureAngleRad()

        #---------------------------------
        # Working pressure angle
        #---------------------------------
        # Sun-Planet-Stg1
        inv_alpha_w_sunPlanet_stg1 = 2*np.tan(alpha)*((xs + xp1)/(Ns + Np1)) + self.involute(alpha)
        alpha_w_sunPlanet_stg1     = self.inverse_involute(inv_alpha_w_sunPlanet_stg1)

        # Planet-Ring-Stg1
        inv_alpha_w_planetRing_stg1 = 2*np.tan(alpha)*((xr1 - xp1)/(Nr1 - Np1)) + self.involute(alpha)
        alpha_w_planetRing_stg1     = self.inverse_involute(inv_alpha_w_planetRing_stg1)

        # Planet-Ring-Stg2
        inv_alpha_w_planetRing_stg2 = 2*np.tan(alpha)*((xr2 - xp2)/(Nr2 - Np2)) + self.involute(alpha)
        alpha_w_planetRing_stg2     = self.inverse_involute(inv_alpha_w_planetRing_stg2)

        return alpha_w_sunPlanet_stg1, alpha_w_planetRing_stg1, alpha_w_planetRing_stg2

    def getCenterDistModificationCoeff(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        #------------------------------
        # Pressure Angle
        #------------------------------
        alpha = self.getPressureAngleRad()  # Pressure angle in radians

        #------------------------------
        # Working pressure angle
        #------------------------------
        alpha_w_sunPlanet_stg1, alpha_w_planetRing_stg1, alpha_w_planetRing_stg2 = self.getWorkingPressureAngle()

        #------------------------------------------
        # Centre distance modification coefficient
        #------------------------------------------
        y_sunPlanet_stg1  = (( Ns + Np1) / 2) * ((np.cos(alpha) / np.cos(alpha_w_sunPlanet_stg1)) - 1)
        y_planetRing_stg1 = ((Nr1 - Np1) / 2) * ((np.cos(alpha) / np.cos(alpha_w_planetRing_stg1)) - 1)
        y_planetRing_stg2 = ((Nr2 - Np2) / 2) * ((np.cos(alpha) / np.cos(alpha_w_planetRing_stg2)) - 1)

        return y_sunPlanet_stg1, y_planetRing_stg1, y_planetRing_stg2

    def getCenterDistance(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        #-------------------------------
        # Centre distance modification coefficient
        #-------------------------------
        y_sunPlanet_stg1, y_planetRing_stg1, y_planetRing_stg2 = self.getCenterDistModificationCoeff()

        #-------------------------------
        # Centre distance
        #-------------------------------

        centerDist_sunPlanet_stg1  = ((Ns + Np1)/2   + y_sunPlanet_stg1)* module1
        centerDist_planetRing_stg1 = ((Nr1 - Np1)/2  + y_planetRing_stg1)* module1
        centerDist_planetRing_stg2 = ((Nr2 - Np2)/2  + y_planetRing_stg2)* module2

        return centerDist_sunPlanet_stg1, centerDist_planetRing_stg1, centerDist_planetRing_stg2

    def getBaseDia(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        # Pressure Angle
        alpha = self.getPressureAngleRad() # Rad

        # Reference Diameter
        D_sun     = module1 * Ns   # Sun's reference diameter
        D_planet1 = module1 * Np1  # Planet's reference diameter
        D_planet2 = module2 * Np2  # Planet's reference diameter
        D_ring1    = module1 * Nr1 # Ring's reference diameter
        D_ring2    = module2 * Nr2 # Ring's reference diameter

        # Base Diameter
        D_b_sun      = D_sun * np.cos(alpha)
        D_b_planet1  = D_planet1 * np.cos(alpha)
        D_b_planet2  = D_planet2 * np.cos(alpha)
        D_b_ring1    = D_ring1 * np.cos(alpha)
        D_b_ring2    = D_ring2 * np.cos(alpha)

        return D_b_sun, D_b_planet1, D_b_planet2, D_b_ring1, D_b_ring2

    def getTipCircleDia(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0
        
        #----------------------------
        # Pressure Angle
        #----------------------------
        alpha = self.getPressureAngleRad() # Rad

        #----------------------------
        # Reference Diameter
        #----------------------------
        D_sun     = module1 * Ns  # Sun's reference diameter
        D_planet1 = module1 * Np1 # Planet's reference diameter
        D_planet2 = module2 * Np2 # Planet's reference diameter
        D_ring1   = module1 * Nr1 # Ring's reference diameter
        D_ring2   = module2 * Nr2 # Ring's reference diameter

        #----------------------------
        # Center Distance Modification Coefficient
        #----------------------------
        y_sunPlanet_stg1, y_planetRing_stg1, y_planetRing_stg2 = self.getCenterDistModificationCoeff()

        #----------------------------
        # Tip circle diameter
        #----------------------------
        # Sun
        D_a_sun = D_sun + 2 * module1 * (1 + y_sunPlanet_stg1 - xp1)

        # Planet
        D_a_planet1 = D_planet1 + 2 * module1 * (1 + self.quadratic_min((y_sunPlanet_stg1 - xs), xp1))  
        # D_a_planet2 = D_planet2 + 2 * module2 * (1 + self.quadratic_min((y_planetRing - xs),xp2)) 
        D_a_planet2 = D_planet2 + 2 * module2 * (1 + xp2) 
        
        # Ring
        D_a_ring1 = D_ring1 - 2 * module1 * (1 - xr1)
        D_a_ring2 = D_ring2 - 2 * module2 * (1 - xr2)
        
        return D_a_sun, D_a_planet1, D_a_planet2, D_a_ring1, D_a_ring2

    def getTipPressureAngle(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        alpha = self.getPressureAngleRad() # Pressure Angle (Rad)
        D_b_sun, D_b_planet1, D_b_planet2, D_b_ring1, D_b_ring2 = self.getBaseDia() # Base Diameter
        D_a_sun, D_a_planet1, D_a_planet2, D_a_ring1, D_a_ring2 = self.getTipCircleDia() # Tip Circle Diameter

        #----------------------------
        # Tip Pressure angle
        #----------------------------
        alpha_a_sun    =  np.arccos(D_b_sun / D_a_sun)
        alpha_a_planet1 = np.arccos(D_b_planet1/D_a_planet1)
        alpha_a_planet2 = np.arccos(D_b_planet2/D_a_planet2)
        alpha_a_ring1   = np.arccos(D_b_ring1 / D_a_ring1)
        alpha_a_ring2   = np.arccos(D_b_ring2 / D_a_ring2)

        return alpha_a_sun, alpha_a_planet1, alpha_a_planet2, alpha_a_ring1, alpha_a_ring2

    def getErrorTipCircleDia_planet(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0
        
        # Centre distance modification coefficient
        y_sunPlanet_stg1, y_planetRing_stg1, y_planetRing_stg2 = self.getCenterDistModificationCoeff()

        # Tip Circle Diameter
        _, D_a_planet1_quadMin, D_a_planet2_quadMin, _, _ = self.getTipCircleDia()
        D_a_planet1_actMin = module1 * Np1 + 2 * module1 * (1 + np.minimum((y_sunPlanet_stg1 - xs),xp1)) # TODO: How will we implement min function 
        D_a_planet2_actMin = module2 * Np2 + 2 * module2 * (1 + xp2) # TODO: How will we implement min function 

        return np.abs(D_a_planet1_quadMin - D_a_planet1_actMin), np.abs(D_a_planet2_quadMin - D_a_planet2_actMin)

    #-------------------------------------------------------------------------
    # Contact Ratio
    #-------------------------------------------------------------------------
    def contactRatio_sunPlanet_stg1(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        # Working pressure angle
        alpha_w_sunPlanet_stg1, _, _ = self.getWorkingPressureAngle()

        # Tip pressure angle
        alpha_a_sun, alpha_a_planet1, _, _, _ = self.getTipPressureAngle()

        # Contact ratio
        Approach_CR_sunPlanet_stg1 = (Np1 / (2 * np.pi)) * (np.tan(alpha_a_planet1) - np.tan(alpha_w_sunPlanet_stg1)) # Approach contact ratio
        Recess_CR_sunPlanet_stg1   = (Ns / (2 * np.pi)) * (np.tan(alpha_a_sun) - np.tan(alpha_w_sunPlanet_stg1))      # Recess contact ratio

        # write the final formula
        CR_sunPlanet_stg1 = Approach_CR_sunPlanet_stg1 + Recess_CR_sunPlanet_stg1

        return Approach_CR_sunPlanet_stg1, Recess_CR_sunPlanet_stg1, CR_sunPlanet_stg1

    def contactRatio_planetRing_stg1(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        # Working pressure angle
        _, alpha_w_planetRing_stg1, _ = self.getWorkingPressureAngle()

        # Tip pressure angle
        _, alpha_a_planet1, _, alpha_a_ring1, _ = self.getTipPressureAngle()

        # Contact ratio
        Approach_CR_planetRing_stg1 = -(Nr1 / (2 * np.pi)) * (np.tan(alpha_a_ring1) - np.tan(alpha_w_planetRing_stg1)) # Approach contact ratio
        Recess_CR_planetRing_stg1   =   Np1 / (2 * np.pi) * (np.tan(alpha_a_planet1) - np.tan(alpha_w_planetRing_stg1)) # Recess contact ratio
        
        # Contact Ratio
        CR_planetRing_stg1 = Approach_CR_planetRing_stg1 + Recess_CR_planetRing_stg1

        return Approach_CR_planetRing_stg1, Recess_CR_planetRing_stg1, CR_planetRing_stg1

    def contactRatio_planetRing_stg2(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        # Working pressure angle
        _, _, alpha_w_planetRing_stg2 = self.getWorkingPressureAngle()

        # Tip pressure angle
        _, _, alpha_a_planet2, _, alpha_a_ring2 = self.getTipPressureAngle()

        # Contact ratio
        Approach_CR_planetRing_stg2 = -(Nr2 / (2 * np.pi)) * (np.tan(alpha_a_ring2) - np.tan(alpha_w_planetRing_stg2)) # Approach contact ratio
        Recess_CR_planetRing_stg2   =   Np2 / (2 * np.pi) * (np.tan(alpha_a_planet2) - np.tan(alpha_w_planetRing_stg2)) # Recess contact ratio
        
        # Contact Ratio
        CR_planetRing_stg2 = Approach_CR_planetRing_stg2 + Recess_CR_planetRing_stg2
        
        return Approach_CR_planetRing_stg2, Recess_CR_planetRing_stg2, CR_planetRing_stg2

    #-----------------------------------------
    # Gearbox Efficiency
    #-----------------------------------------
    def getEfficiency(self):
        module1 = self.moduleBig
        module2 = self.moduleSmall
        Ns      = self.Ns
        Np1     = self.NpBig
        Np2     = self.NpSmall
        Nr1     = self.NrBig
        Nr2     = self.NrSmall
        xs      = 0
        xp1     = 0
        xp2     = 0
        xr1     = 0
        xr2     = 0

        # Contact ratio
        eps_sunPlanet_stg1A, eps_sunPlanet_stg1R, _ = self.contactRatio_sunPlanet_stg1()
        eps_planetRing_stg1A, eps_planetRing_stg1R, _ = self.contactRatio_planetRing_stg1()
        eps_planetRing_stg2A, eps_planetRing_stg2R, _ = self.contactRatio_planetRing_stg2()
        
        # Contact-Ratio-Factor
        epsilon_sunPlanet_stg1  = eps_sunPlanet_stg1A**2 + eps_sunPlanet_stg1R**2 - eps_sunPlanet_stg1A - eps_sunPlanet_stg1R + 1 
        epsilon_planetRing_stg1 = eps_planetRing_stg1A**2 + eps_planetRing_stg1R**2 - eps_planetRing_stg1A - eps_planetRing_stg1R + 1 
        epsilon_planetRing_stg2 = eps_planetRing_stg2A**2 + eps_planetRing_stg2R**2 - eps_planetRing_stg2A - eps_planetRing_stg2R + 1 
        
        # Efficiency
        eff_SP_stg1 = 1 - self.mu * np.pi * ((1 / Np1) + (1 / Ns)) * epsilon_sunPlanet_stg1
        eff_PR_stg1 = 1 - self.mu * np.pi * ((1 / Np1) - (1 / Nr1)) * epsilon_planetRing_stg1
        eff_PR_stg2 = 1 - self.mu * np.pi * ((1 / Np2) - (1 / Nr2)) * epsilon_planetRing_stg2

        I1  = (Nr1 / Ns)
        I2  = (Nr1 * Np2) / (Np1 * Nr2)
        n_a = eff_SP_stg1 # self.getEfficiency_sunPlanet_stg1(Var = Var)
        n_b = eff_PR_stg1 # self.getEfficiency_planetRing_stg1(Var = Var)
        n_c = eff_PR_stg2 # self.getEfficiency_planetRing_stg2(Var = Var)

        Numerator   = (1 + n_a * n_b * I1) * (1 - I2)
        Denominator = (1 + I1) * (1 - n_b * n_c * I2)
        return Numerator / Denominator

    # ---------------------------------------

    def getEfficiency_old(self):
        I1 = self.NrBig / self.Ns
        I2 = (self.NrBig * self.NpSmall) / (self.NpBig * self.NrSmall)
        n_a = self.getEfficiencySunPlanet()
        n_b = self.getEfficiencyPlanetRingBig()
        n_c = self.getEfficiencyPlanetRingSmall()

        # print(" ")
        # print("I1 = ", I1)
        # print("I2 = ", I2)
        # print("n_a = ", n_a)
        # print("n_b = ", n_b)
        # print("n_c = ", n_c)
        # print(" ")

        Numerator = (1 + n_a*n_b*I1)*(1-I2)
        Denominator = (1+I1)*(1-n_b*n_c*I2)
        return Numerator / Denominator

    def getPCRadiusSunM(self):
        return ((self.Ns * self.moduleBig / 2) / 1000.0)

    def getPCRadiusPlanetBigM(self):
        return ((self.NpBig * self.moduleBig / 2) / 1000.0)

    def getPCRadiusPlanetSmallM(self):
        return ((self.NpSmall * self.moduleSmall / 2) / 1000.0)

    def getPCRadiusRingBigM(self):
        return ((self.NrBig * self.moduleBig / 2) / 1000.0)   

    def getPCRadiusRingSmallM(self):
        return ((self.NrSmall * self.moduleSmall / 2) / 1000.0) 

    def getOuterRadiusRingSmallM(self):
        ringPCDiameterMM = self.NrSmall * self.moduleSmall 
        ringPCRadiusMM = ringPCDiameterMM / 2
        return (ringPCRadiusMM + self.ringRadialWidthSmall) / 1000.0

    def getOuterRadiusRingBigM(self):
        ringPCDiameterMM = self.NrBig * self.moduleBig
        ringPCRadiusMM = ringPCDiameterMM / 2
        return (ringPCRadiusMM + self.ringRadialWidthBig) / 1000.0
    
    def getPCRadiusSunMM(self):
        return ((self.Ns * self.moduleBig / 2))

    def getPCRadiusPlanetBigMM(self):
        return ((self.NpBig * self.moduleBig / 2))

    def getPCRadiusPlanetSmallMM(self):
        return ((self.NpSmall * self.moduleSmall / 2))

    def getPCRadiusRingBigMM(self):
        return ((self.NrBig * self.moduleBig / 2))   

    def getPCRadiusRingSmallMM(self):
        return ((self.NrSmall * self.moduleSmall / 2)) 

    def getOuterRadiusRingSmallMM(self):
        ringPCDiameterMM = self.NrSmall * self.moduleSmall 
        ringPCRadiusMM = ringPCDiameterMM / 2
        return (ringPCRadiusMM + self.ringRadialWidthSmall)

    def getOuterRadiusRingBigMM(self):
        ringPCDiameterMM = self.NrBig * self.moduleBig
        ringPCRadiusMM = ringPCDiameterMM / 2
        return (ringPCRadiusMM + self.ringRadialWidthBig)
    
    def getCarrierRadiusM(self):
        return (((self.Ns + self.NpBig + self.NpBig/2)/2)*self.moduleBig) / 1000.0

    # Set the face width of the sun gear, planet gear, and ring gear in mm
    def setfwSunMM(self, fwSunMM):
        self.fwSunMM = fwSunMM

    def setfwPlanetBigMM(self, fwPlanetBigMM):
        self.fwPlanetBigMM = fwPlanetBigMM

    def setfwPlanetSmallMM(self, fwPlanetSmallMM):
        self.fwPlanetSmallMM = fwPlanetSmallMM

    def setfwRingBigMM(self, fwRingBigMM):
        self.fwRingBigMM = fwRingBigMM

    def setfwRingSmallMM(self, fwRingSmallMM):
        self.fwRingSmallMM = fwRingSmallMM

    def setModuleBig(self, moduleBig):
        self.moduleBig = moduleBig

    def setModuleSmall(self, moduleSmall):
        self.moduleSmall = moduleSmall

    def setNs(self, Ns):
        self.Ns = Ns

    def setNpBig(self, NpBig):
        self.NpBig = NpBig

    def setNpSmall(self, NpSmall):
        self.NpSmall = NpSmall

    def setNrBig(self, NrBig):
        self.NrBig = NrBig

    def setNrSmall(self, NrSmall):
        self.NrSmall = NrSmall
    
    def setNumPlanet(self, numPlanet):
        self.numPlanet = numPlanet

    def getFloatingSunTeeth(self):     
        return self.NrSmall - 2*self.NpSmall
    
    def getPCRadiusFloatingSunMM(self): 
        return self.getFloatingSunTeeth() * self.moduleBig / 2
    
    def setfwFloatingSunMM(self, fw):   
        self.fwFloatingSunMM = fw

    def getEfficiencySunPlanet(self):
        module = self.moduleBig                                       # Module of the gear
        alpha = self.pressureAngleDEG * np.pi / 180                   # Pressure angle in radians
        
        D_b_sun    = module * self.Ns * np.cos(alpha)                 # Sun's basic circle diameter
        D_b_planet = module * self.NpBig * np.cos(alpha)              # Planet's basic circle diameter

        centerDist = (self.Ns + self.NpBig) * module / 2              # Center distance between the gears
        alpha_w = np.arccos((D_b_sun + D_b_planet) / (2*centerDist))  # Working pressure angle

        # TODO: For non-equal profile shift coefficients: Use this later
        #ya = 0# ??????

        ya = 0 # Addendum of the sun gear 
        xp = self.profileShiftCoefficientPlanetBig
        xs = self.profileShiftCoefficientSun

        # TODO: For non-equal profile shift coefficients: Use this later
        # D_a_sun    = module * sun.numTeeth + 2*module*(1 + ya - xp)             # Sun's tip circle diameter
        # D_a_planet = module * sun.numTeeth + 2*module*(1 + np.min([ya-xs, xp])) # Planet's tip circle diameter
        
        D_a_sun    = module * self.Ns + 2*module*(1 + xs)             # Sun's tip circle diameter
        D_a_planet = module * self.NpBig + 2*module*(1 + xp) # Planet's tip circle diameter

        alpha_a_sun = np.arccos(D_b_sun / D_a_sun) # Sun's Tip pressure angle
        alpha_a_planet = np.arccos(D_b_planet / D_a_planet) # Planet's Tip pressure angle
        
        eps1 = ((self.NpBig) / (2 * np.pi)) * (np.tan(alpha_a_planet) - np.tan(alpha_w) ) # Approach contact ratio
        eps2 = (self.Ns / (2 * np.pi)) * (np.tan(alpha_a_sun) - np.tan(alpha_w) ) # Recess contact ratio
        epsilon = eps1**2 + eps2**2 - eps1 - eps2 + 1 # equivalent contact ratio

        # NOTE: pinion is always an external gear and gear may be an internal or external gear
        eff = 1 - self.mu * np.pi * (( 1 / self.Ns) + (1 / self.NpBig)) * epsilon
        return eff
    
    def getEfficiencyPlanetRingBig(self):
        module = self.moduleBig                      # Module of the gear
        alpha = self.pressureAngleDEG * np.pi / 180  # Pressure angle in radians
        
        D_b_ring    = module * self.NrBig * np.cos(alpha)       # Sun's basic circle diameter
        D_b_planet = module * self.NpBig * np.cos(alpha)        # Planet's basic circle diameter

        centerDist = (self.NrBig - self.NpBig) * module / 2    # Center distance between the gears
        alpha_w = np.arccos((D_b_ring - D_b_planet) / (2*centerDist))  # Working pressure angle

        # TODO: For non-equal profile shift coefficients: Use this later
        #ya = 0# ??????

        ya = 0 # Addendum of the sun gear 
        xr = self.profileShiftCoefficientRingBig
        xp = self.profileShiftCoefficientPlanetBig

        # TODO: For non-equal profile shift coefficients: Use this later
        # D_a_sun    = module * sun.numTeeth + 2*module*(1 + ya - xp)             # Sun's tip circle diameter
        # D_a_planet = module * sun.numTeeth + 2*module*(1 + np.min([ya-xs, xp])) # Planet's tip circle diameter
        
        D_a_ring    = module * self.NrBig - 2*module*(1 - xr)             # Ring's tip circle diameter
        D_a_planet = module * self.NpBig + 2*module*(1 + xp) # Planet's tip circle diameter

        alpha_a_ring = np.arccos(D_b_ring / D_a_ring) # Sun's Tip pressure angle
        alpha_a_planet = np.arccos(D_b_planet / D_a_planet) # Planet's Tip pressure angle
        
        eps1 = ((self.NrBig) / (2 * np.pi)) * (np.tan(alpha_a_ring) - np.tan(alpha_w) ) # Approach contact ratio
        eps2 = (self.NpBig / (2 * np.pi)) * (np.tan(alpha_a_planet) - np.tan(alpha_w) ) # Recess contact ratio
        epsilon = eps1**2 + eps2**2 - eps1 - eps2 + 1 # equivalent contact ratio

        # NOTE: pinion is always an external gear and gear may be an internal or external gear
        eff = 1 - self.mu * np.pi * (( 1 / self.NpBig) - (1 / self.NrBig)) * epsilon
        return eff

    def getEfficiencyPlanetRingSmall(self):
        module = self.moduleSmall                      # Module of the gear
        alpha = self.pressureAngleDEG * np.pi / 180  # Pressure angle in radians
        
        D_b_ring    = module * self.NrSmall * np.cos(alpha)       # Sun's basic circle diameter
        D_b_planet = module * self.NpSmall * np.cos(alpha)    # Planet's basic circle diameter

        centerDist = (self.NrSmall - self.NpSmall) * module / 2    # Center distance between the gears
        alpha_w = np.arccos((D_b_ring - D_b_planet) / (2*centerDist))  # Working pressure angle

        # TODO: For non-equal profile shift coefficients: Use this later
        #ya = 0# ??????

        ya = 0 # Addendum of the sun gear 
        xr = self.profileShiftCoefficientRingSmall
        xp = self.profileShiftCoefficientPlanetSmall

        # TODO: For non-equal profile shift coefficients: Use this later
        # D_a_sun    = module * sun.numTeeth + 2*module*(1 + ya - xp)             # Sun's tip circle diameter
        # D_a_planet = module * sun.numTeeth + 2*module*(1 + np.min([ya-xs, xp])) # Planet's tip circle diameter
        
        D_a_ring    = module * self.NrSmall - 2*module*(1 - xr)             # Ring's tip circle diameter
        D_a_planet = module * self.NpSmall + 2*module*(1 + xp) # Planet's tip circle diameter

        alpha_a_ring = np.arccos(D_b_ring / D_a_ring) # Sun's Tip pressure angle
        alpha_a_planet = np.arccos(D_b_planet / D_a_planet) # Planet's Tip pressure angle
        
        eps1 = ((self.NrSmall) / (2 * np.pi)) * (np.tan(alpha_a_ring) - np.tan(alpha_w) ) # Approach contact ratio
        eps2 = (self.NpSmall / (2 * np.pi)) * (np.tan(alpha_a_planet) - np.tan(alpha_w) ) # Recess contact ratio
        epsilon = eps1**2 + eps2**2 - eps1 - eps2 + 1 # equivalent contact ratio

        # NOTE: pinion is always an external gear and gear may be an internal or external gear
        eff = 1 - self.mu * np.pi * (( 1 / self.NpSmall) - (1 / self.NrSmall)) * epsilon
        return eff

    # Print the planetary gearbox parameters
    def printParameters(self):
        print("Ns = ", self.Ns)
        print("NpBig = ", self.NpBig)
        print("NpSmall = ", self.NpSmall)
        print("NrBig = ", self.NrBig)
        print("NrSmall = ", self.NrSmall)
        print("Module (First Layer) = ", self.moduleBig)
        print("Module (Second Layer) = ", self.moduleSmall)
        print("Number of planets = ", self.numPlanet)
        print("Face width of sun gear = ", round(self.fwSunMM,2), " mm")
        print("Face width of Bigger planet gear = ", round(self.fwPlanetBigMM,2), " mm")
        print("Face width of Smaller planet gear = ", round(self.fwPlanetSmallMM,2), " mm")
        print("Face width of Bigger ring gear = ", round(self.fwRingBigMM,2), " mm")
        print("Face width of Smaller ring gear = ", round(self.fwRingSmallMM,2), " mm")
        print("Carrier width = ", self.carrierWidthMM, " mm")
        print("Bigger Ring radial width = ", self.ringRadialWidthBig, " mm")
        print("Smaller Ring radial width = ", self.ringRadialWidthSmall, " mm")
        print("Pitch circle radius of sun gear = ", self.getPCRadiusSunM() * 1000, " mm")
        print("Pitch circle radius of Bigger planet gear = ", self.getPCRadiusPlanetBigM() * 1000, " mm")
        print("Pitch circle radius of Smaller planet gear = ", self.getPCRadiusPlanetSmallM() * 1000, " mm")
        print("Pitch circle radius of Big ring gear = ", self.getPCRadiusRingBigM() * 1000, " mm")
        print("Pitch circle radius of Smaller ring gear = ", self.getPCRadiusRingSmallM() * 1000, " mm")
        print("Outer radius of Bigger ring gear = ", self.getOuterRadiusRingBigM() * 1000, " mm")
        print("Outer radius of Smaller ring gear = ", self.getOuterRadiusRingSmallM() * 1000, " mm")
        print("Carrier radius = ", self.getCarrierRadiusM() * 1000, " mm")
        print("Geometric constraint = ", self.geometricConstraint())
        print("Meshing constraint = ", self.meshingConstraint())
        print("No planet interference constraint = ", self.noPlanetInterferenceConstraint())
        print("Mass of the planetary gearbox = ", self.getMassKG(), " kg")
        print("Efficiency of the planetary gearbox = ", self.getEfficiency())
        #print("Maximum allowable stress for the gear material = ", self.getMaxGearAllowableStress(), " MPa")

    # Print the planetary gearbox parameters
    def printParametersLess(self):
        # print("----------------------------3k Planetary Gearbox--------------------------")
        vars = [self.moduleBig, self.moduleSmall, self.Ns, self.NpBig, self.NpSmall, self.NrBig, self.NrSmall, self.numPlanet]
        faceWidths = [round(self.fwSunMM,2), round(self.fwPlanetBigMM,2), round(self.fwPlanetSmallMM,2), round(self.fwRingBigMM,2), round(self.fwRingSmallMM,2)]
        print("[mB, mS, Ns, NpB, NpS, NrB, NrS, numPl]:", vars) 
        print("Face widths = ", faceWidths)
        print(" ")
        print("Gear ratio = ", self.gearRatio())
        print("Efficiency = ", round(self.getEfficiency(),4))
        print("Mass (gearbox, kg) = ", round(self.getMassKG(),3), " kg")
        # print("--------------------------------------------------------------------------")


#-------------------------------------------------------------------------
# Bipath 3K Planetary Actuator class (Bipath Wolfrom Planetary Actuator Class)
#-------------------------------------------------------------------------
class bipathwolfromPlanetaryActuator:
    def __init__(self, 
                 design_parameters,
                 motor_driver_params,
                 motor                    = motor,
                 bipathwolfromPlanetaryGearbox  = bipathwolfromPlanetaryGearbox,
                 FOS                      = 2.0,
                 serviceFactor            = 2.0,
                 maxGearboxDiameter       = 140.0,
                 stressAnalysisMethodName = "Lewis"):
        
        self.motor                    = motor
        self.bipathwolfromPlanetaryGearbox  = bipathwolfromPlanetaryGearbox
        self.FOS                      = FOS
        self.serviceFactor            = serviceFactor
        self.maxGearboxDiameter       = maxGearboxDiameter # TODO: convert it to 
                                                          # outer diameter of 
                                                          # the motor
        self.stressAnalysisMethodName = stressAnalysisMethodName

        self.design_params = design_parameters
        self.motor_driver_params = motor_driver_params

        #--------------------------------------------
        # Motor Specifications
        #--------------------------------------------
        self.motorLengthMM           = self.motor.getLengthMM()
        self.motorDiaMM              = self.motor.getDiaMM()
        self.motorMassKG             = self.motor.getMassKG()
        self.MaxMotorTorque          = self.motor.maxMotorTorque
        self.MaxMotorAngVelRPM       = self.motor.maxMotorAngVelRPM
        self.MaxMotorAngVelRadPerSec = self.motor.maxMotorAngVelRadPerSec

        #-----------------------------------------
        # Actuator Design Free Parameters
        #-----------------------------------------
        self.sCarrierExtrusionDiaMM       = design_parameters["sCarrierExtrusionDiaMM"]       # 12 # TODO: depends on the numPlanet, planet radii and clearance of planets
        self.sCarrierExtrusionClearanceMM = design_parameters["sCarrierExtrusionClearanceMM"] # 2

        self.gearbox_casing_thickness         = design_parameters["gearbox_casing_thickness"]
        self.small_ring_gear_casing_thickness = design_parameters["small_ring_gear_casing_thickness"]
        self.bearingIDClearanceMM             = design_parameters["bearingIDClearanceMM"]

        self.ring1RadialWidthMM = self.bipathwolfromPlanetaryGearbox.ringRadialWidthBig   # 5
        self.ring2RadialWidthMM = self.bipathwolfromPlanetaryGearbox.ringRadialWidthSmall # 5

        # --- Setting the variables ---
        self.setVariables()

        self.actuator_width = 0

    def cost(self):
        massActuator = self.getMassKG_3DP()
        effActuator  = self.bipathwolfromPlanetaryGearbox.getEfficiency()
        widthActuator = self.bipathwolfromPlanetaryGearbox.fwPlanetBigMM + self.bipathwolfromPlanetaryGearbox.fwPlanetSmallMM
        module = self.bipathwolfromPlanetaryGearbox.moduleBig
        cost = massActuator - 2 * effActuator + 0.2 * widthActuator
        return cost

    def setVariables(self):
        # --- Optimization Variables --- 
        self.Ns         = self.bipathwolfromPlanetaryGearbox.Ns
        self.Np_b       = self.bipathwolfromPlanetaryGearbox.NpBig
        self.Np_s       = self.bipathwolfromPlanetaryGearbox.NpSmall
        self.Nr_b       = self.Ns + self.Np_b * 2
        self.Nr_s       = self.Ns + self.Np_b + self.Np_s
        self.module     = self.bipathwolfromPlanetaryGearbox.moduleBig
        self.num_planet = self.bipathwolfromPlanetaryGearbox.numPlanet

        #------------------------
        # --- Fixed Variables ---
        #------------------------
        # --- Clearances --- 
        self.clearance_planet                           = self.design_params["clearance_planet"]
        self.clearance_sun_coupler_sec_carrier          = self.design_params["clearance_sun_coupler_sec_carrier"]
        self.clearance_case_mount_holes_shell_thickness = self.design_params["clearance_case_mount_holes_shell_thickness"]
        self.case_mounting_nut_clearance                = self.design_params["case_mounting_nut_clearance"]
        self.standard_clearance_1_5mm                   = self.design_params["standard_clearance_1_5mm"]
        self.standard_fillet_1_5mm                      = self.design_params["standard_fillet_1_5mm"]
        self.standard_bearing_insertion_chamfer         = self.design_params["standard_bearing_insertion_chamfer"]
        self.tight_clearance_3DP                        = self.design_params["tight_clearance_3DP"]        
        self.loose_clearance_3DP                        = self.design_params["loose_clearance_3DP"]

        # --- Gear Variables ---
        self.pressure_angle = self.bipathwolfromPlanetaryGearbox.getPressureAngleRad()
        self.pressure_angle_deg = self.bipathwolfromPlanetaryGearbox.getPressureAngleRad() * 180 / np.pi

        # --- Motor ---
        self.motor_OD                            = self.motorDiaMM                     # 86.8
        self.motor_height                        = self.motorLengthMM                  # 26.5
        self.motor_mount_hole_PCD                = self.motor.motor_mount_hole_PCD     # 32
        self.motor_mount_hole_dia                = self.motor.motor_mount_hole_dia     # 4
        self.motor_mount_hole_num                = self.motor.motor_mount_hole_num     # 4
        self.motor_output_hole_PCD               = self.motor.motor_output_hole_PCD    # 23
        self.motor_output_hole_dia               = self.motor.motor_output_hole_dia    # 4
        self.motor_output_hole_num               = self.motor.motor_output_hole_num    # 4
        self.wire_slot_dist_from_center          = self.motor.wire_slot_dist_from_center # 30
        self.wire_slot_length                    = self.motor.wire_slot_length         # 10
        self.wire_slot_radius                    = self.motor.wire_slot_radius         # 4

        self.driver_upper_holes_dist_from_center = self.motor_driver_params["driver_upper_holes_dist_from_center"] # 23
        self.driver_lower_holes_dist_from_center = self.motor_driver_params["driver_lower_holes_dist_from_center"] # 15
        self.driver_side_holes_dist_from_center  = self.motor_driver_params["driver_side_holes_dist_from_center"]  # 20
        self.driver_mount_holes_dia              = self.motor_driver_params["driver_mount_holes_dia"]  # 2.5
        self.driver_mount_inserts_OD             = self.motor_driver_params["driver_mount_inserts_OD"] # 3.5
        self.driver_mount_thickness              = self.motor_driver_params["driver_mount_thickness"]  # 1.5
        self.driver_mount_height                 = self.motor_driver_params["driver_mount_height"]     # 4

        self.central_hole_offset_from_motor_mount_PCD = self.design_params["central_hole_offset_from_motor_mount_PCD"] # 5

        motor_output_hole_bolt = nuts_and_bolts_dimensions(bolt_dia = self.motor_output_hole_dia, bolt_type="CSK")
        self.motor_output_hole_CSK_OD          = motor_output_hole_bolt.bolt_head_dia   
        self.motor_output_hole_CSK_head_height = motor_output_hole_bolt.bolt_head_height


        # --- Motor & gearbox Casing ---
        self.case_mounting_hole_dia                 = self.design_params["case_mounting_hole_dia"] #3
        self.case_mounting_bolt_depth               = self.design_params["case_mounting_bolt_depth"]   #4.5
        self.output_mounting_hole_dia               = self.design_params["output_mounting_hole_dia"]   #4
        self.Motor_case_thickness                   = self.design_params["Motor_case_thickness"]   #2.5
        self.output_mounting_nut_depth              = self.design_params["output_mounting_nut_depth"]  #3
        self.Motor_case_OD_base_to_chamfer          = self.design_params["Motor_case_OD_base_to_chamfer"]  #5
        self.pattern_offset_from_motor_case_OD_base = self.design_params["pattern_offset_from_motor_case_OD_base"] #3
        self.pattern_bulge_dia                      = self.design_params["pattern_bulge_dia"]  #3
        self.pattern_num_bulge                      = self.design_params["pattern_num_bulge"]  #18
        self.pattern_depth                          = self.design_params["pattern_depth"]  #2
        self.base_plate_thickness                   = self.design_params["base_plate_thickness"]   #4
        self.case_mounting_surface_height           = self.design_params["case_mounting_surface_height"]   #4
        self.air_flow_hole_offset                   = self.design_params["air_flow_hole_offset"]   #3

        case_mounting_hole_bolt = nuts_and_bolts_dimensions(bolt_dia=self.case_mounting_hole_dia, bolt_type="socket_head")

        self.case_mounting_hole_allen_socket_dia = case_mounting_hole_bolt.bolt_head_dia # 5.5
        self.case_mounting_wrench_size           = case_mounting_hole_bolt.nut_width_across_flats # 5.5
        self.case_mounting_nut_thickness         = case_mounting_hole_bolt.nut_thickness # 2.4

        output_mounting_hole_bolt = nuts_and_bolts_dimensions(bolt_dia=self.output_mounting_hole_dia, bolt_type="socket_head")

        self.output_mounting_nut_thickness   = output_mounting_hole_bolt.nut_thickness # 3.2
        self.output_mounting_nut_wrench_size = output_mounting_hole_bolt.nut_width_across_flats # 7

        # --- Sun gear ---
        self.sun_shaft_bearing_ID      = self.design_params["sun_shaft_bearing_ID"] # 8
        self.sun_shaft_bearing_OD      = self.design_params["sun_shaft_bearing_OD"] # 16
        self.sun_coupler_hub_thickness = self.design_params["sun_coupler_hub_thickness"] # 4
        self.sun_shaft_bearing_width   = self.design_params["sun_shaft_bearing_width"] # 4
        self.sun_central_bolt_dia      = self.design_params["sun_central_bolt_dia"] # 5

        sun_central_bolt = nuts_and_bolts_dimensions(bolt_dia = self.sun_central_bolt_dia, bolt_type="socket_head")
        self.sun_central_bolt_socket_head_dia = sun_central_bolt.bolt_head_dia # 8.5

        self.fw_s_calc = self.bipathwolfromPlanetaryGearbox.fwSunMM

        # --- Planet Gear ---

        self.planet_pin_bolt_dia      = self.design_params["planet_pin_bolt_dia"] # 5
        self.planet_shaft_dia         = self.design_params["planet_shaft_dia"] # 8
        self.planet_shaft_step_offset = self.design_params["planet_shaft_step_offset"] # 1
        self.planet_bearing_OD        = self.design_params["planet_bearing_OD"] # 12
        self.planet_bearing_width     = self.design_params["planet_bearing_width"] # 3
        self.planet_bore              = self.design_params["planet_bore"] # 10

        planet_pin_bolt = nuts_and_bolts_dimensions(bolt_dia=self.planet_pin_bolt_dia, bolt_type="socket_head")
        self.planet_pin_socket_head_dia  = planet_pin_bolt.bolt_head_dia # 8.5
        self.planet_pin_bolt_wrench_size = planet_pin_bolt.nut_width_across_flats # 8    

        self.fw_p_b = self.bipathwolfromPlanetaryGearbox.fwPlanetBigMM

        # --- Ring Gear ---
        self.ring_radial_thickness = self.design_params["ring_radial_thickness"]
        self.fw_r_s = self.bipathwolfromPlanetaryGearbox.fwRingSmallMM

        # --- Gearbox Casing ---
        self.gear_casing_thickness = self.design_params["gear_casing_thickness"]

        # --- Carrier & Sec Carrier--- 
        self.sec_carrier_thickness = self.design_params["sec_carrier_thickness"] # 5

        self.carrier_trapezoidal_support_sun_offset                 = self.design_params["carrier_trapezoidal_support_sun_offset"]# 5
        self.carrier_trapezoidal_support_hole_PCD_offset_bearing_ID = self.design_params["carrier_trapezoidal_support_hole_PCD_offset_bearing_ID"]# 4
        self.carrier_trapezoidal_support_hole_dia                   = self.design_params["carrier_trapezoidal_support_hole_dia"]# 3
        self.carrier_bearing_step_width                             = self.design_params["carrier_bearing_step_width"]# 1.5

        self.carrier_PCD = (self.Np_b + self.Ns) * self.module
        
        carrier_trapezoidal_support_hole = nuts_and_bolts_dimensions(bolt_dia=self.carrier_trapezoidal_support_hole_dia, bolt_type="socket_head")

        self.carrier_trapezoidal_support_hole_socket_head_dia = carrier_trapezoidal_support_hole.bolt_head_dia
        self.carrier_trapezoidal_support_hole_wrench_size     = carrier_trapezoidal_support_hole.nut_width_across_flats        

        self.carrier_thickness                                      = self.design_params["carrier_thickness"]

        # --- Bearing Retainer --- 
        self.bearing_retainer_thickness                            = self.design_params["bearing_retainer_thickness"]#2

        # --- Small Ring ---
        self.small_ring_output_wall_thickness                                           = self.design_params["small_ring_output_wall_thickness"]
        self.small_ring_output_wall_to_bearing_shaft_attachement_hole_dia               = self.design_params["small_ring_output_wall_to_bearing_shaft_attachement_hole_dia"]
        self.small_ring_output_wall_to_bearing_shaft_attachement_hole_depth             = self.design_params["small_ring_output_wall_to_bearing_shaft_attachement_hole_depth"]
        self.small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd               = self.design_params["small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd"]        
        self.small_ring_output_wall_to_bearing_shaft_attachement_hole_num               = self.design_params["small_ring_output_wall_to_bearing_shaft_attachement_hole_num"]
        self.carrier_small_ring_inner_bearing_ID                                        = self.design_params["carrier_small_ring_inner_bearing_ID"]
        self.carrier_small_ring_inner_bearing_flap                                      = self.design_params["carrier_small_ring_inner_bearing_flap"]
        self.small_ring_case_thickness                                                  = self.design_params["small_ring_case_thickness"]

        carrier_small_ring_inner_bearing               = bearings_discrete(self.carrier_small_ring_inner_bearing_ID)
        self.carrier_small_ring_inner_bearing_OD       = carrier_small_ring_inner_bearing.getBearingODMM()
        self.carrier_small_ring_inner_bearing_height   = carrier_small_ring_inner_bearing.getBearingWidthMM()


        small_ring_output_wall_to_bearing_shaft_attachement_bolt = nuts_and_bolts_dimensions(bolt_dia=self.small_ring_output_wall_to_bearing_shaft_attachement_hole_dia, bolt_type="CSK")

        self.small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench             = small_ring_output_wall_to_bearing_shaft_attachement_bolt.nut_width_across_flats
        self.small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness          = small_ring_output_wall_to_bearing_shaft_attachement_bolt.nut_thickness

        self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD            = small_ring_output_wall_to_bearing_shaft_attachement_bolt.bolt_head_dia
        self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height   = small_ring_output_wall_to_bearing_shaft_attachement_bolt.bolt_head_height

        #----------------------------
        #---- Dependent Variables ---
        #---------------------------- 
        # --- Clearances --- 
        self.ring_to_chamfer_clearance = self.clearance_planet

        # --- Gear profile parameters ---
        self.h_a = 1 * self.module
        self.h_f = 1.25 * self.module
        self.h_b = 1.25 * self.module
        self.clr_tip_root = self.h_f - self.h_a
        self.clr_tip_root_s = self.h_f - self.h_a

        # --- Ring ---
        # Big
        self.dp_r_b = self.module * self.Nr_b
        self.db_r_b = self.dp_r_b * np.cos ( self.pressure_angle )
        self.fw_r_b = self.fw_p_b
        self.alpha_r_b = ( self.dp_r_b ** 2 - self.db_r_b ** 2 )**0.5 / self.db_r_b * 180 / np.pi - self.pressure_angle_deg
        self.beta_r_b = ( 360 / ( 4 * self.Nr_b ) + self.alpha_r_b ) * 2

        self.ring_OD_b = self.Nr_b * self.module + self.ring_radial_thickness * 2

        # Small
        self.dp_r_s = self.module * self.Nr_s
        self.db_r_s = self.dp_r_s * np.cos ( self.pressure_angle )
        self.alpha_r_s = ( self.dp_r_s ** 2 - self.db_r_s ** 2 )**0.5 / self.db_r_s * 180 / np.pi - self.pressure_angle_deg
        self.beta_r_s = ( 360 / ( 4 * self.Nr_s ) + self.alpha_r_s ) * 2

        # --- Planet ---
        # Big
        self.dp_p_b = self.module * self.Np_b
        self.db_p_b = self.dp_p_b * np.cos ( self.pressure_angle )
        self.alpha_p_b = ( self.dp_p_b ** 2 - self.db_p_b ** 2 )**0.5 / self.db_p_b * 180 / np.pi - self.pressure_angle_deg
        self.beta_p_b = ( 360 / ( 4 * self.Np_b ) - self.alpha_p_b ) * 2

        # Small
        self.dp_p_s = self.module * self.Np_s
        self.db_p_s = self.dp_p_s * np.cos ( self.pressure_angle )
        self.alpha_p_s = ( self.dp_p_s ** 2 - self.db_p_s ** 2 )**0.5 / self.db_p_s * 180 / np.pi - self.pressure_angle_deg
        self.beta_p_s = ( 360 / ( 4 * self.Np_s ) - self.alpha_p_s ) * 2

        self.fw_p_s = self.fw_r_s + self.clearance_planet

        # --- Sun gear ---
        self.dp_s = self.module * self.Ns
        self.db_s = self.dp_s * np.cos ( self.pressure_angle )
        self.alpha_s = ( self.dp_s ** 2 - self.db_s ** 2 )**0.5 / self.db_s * 180 / np.pi - self.pressure_angle_deg
        self.beta_s = ( 360 / ( 4 * self.Ns ) - self.alpha_s ) * 2

        self.sun_hub_dia = self.motor_output_hole_PCD + self.motor_output_hole_dia + self.standard_clearance_1_5mm * 2

        self.fw_s_used = self.fw_p_s + self.fw_p_b + self.clearance_planet + self.sec_carrier_thickness + self.standard_clearance_1_5mm - self.carrier_small_ring_inner_bearing_flap +  self.standard_clearance_1_5mm

        # --- Bearing ---
        IdrequiredMM = self.module * (self.Ns + self.Np_b) + self.bearingIDClearanceMM
        Bearings            = bearings_discrete(IdrequiredMM)
        self.bearing_ID     = Bearings.getBearingIDMM()
        self.bearing_OD     = Bearings.getBearingODMM()
        self.bearing_height = Bearings.getBearingWidthMM()

        # --- Motor & Gearbox casing ---
        self.case_dist = self.sec_carrier_thickness + self.clearance_planet + self.sun_coupler_hub_thickness - self.case_mounting_surface_height
        self.case_mounting_hole_shift = self.case_mounting_hole_dia / 2 - 0.5
        self.clearance_motor_and_case = (5 if ((self.Ns + self.Np_b * 2) * self.module) < self.motor_OD else (((self.Ns + self.Np_b * 2) * self.module - self.motor_OD) * 0.5 + 5) )
        self.motor_case_OD_base = self.motor_OD + self.clearance_motor_and_case * 2 + self.Motor_case_thickness * 2
        self.case_mounting_PCD = self.motor_case_OD_base + self.case_mounting_hole_shift * 2
        self.Motor_case_OD_max = self.case_mounting_PCD + self.case_mounting_hole_allen_socket_dia + self.clearance_case_mount_holes_shell_thickness * 2
        self.bearing_mount_thickness = (self.output_mounting_hole_dia * 2 if (self.bearing_OD + self.output_mounting_hole_dia * 4) > (self.Nr_s * self.module + 2 * self.h_b) else ((self.Nr_s * self.module + 2 * self.h_b - (self.bearing_OD + self.output_mounting_hole_dia * 4)) / 2) + self.output_mounting_hole_dia * 2 + self.standard_clearance_1_5mm)
        self.output_mounting_PCD = self.bearing_OD + self.bearing_mount_thickness
        self.Motor_case_ID = self.motor_OD + self.clearance_motor_and_case * 2

        self.gear_casing_big_ring_to_bearing_dist = self.fw_p_s + self.clearance_planet + self.carrier_thickness + self.standard_clearance_1_5mm*2/3 + self.small_ring_case_thickness - self.standard_clearance_1_5mm # last - is because of change in flap position

        # --- Carrier ---
        self.carrier_PCD = ( self.Np_b + self.Ns ) * self.module

        # Actuator Width
        self.actuator_width = (  self.fw_r_b
                               + self.clearance_planet
                               + self.gear_casing_big_ring_to_bearing_dist
                               + self.bearing_height
                               + self.standard_clearance_1_5mm
                               + self.case_dist
                               + self.bearing_retainer_thickness
                               + self.motor_height
                               + self.case_mounting_surface_height
                               + self.standard_clearance_1_5mm
                               + self.base_plate_thickness)
        # FIXME : Modifications made
        gb = self.bipathwolfromPlanetaryGearbox
        self.Ns_fs = gb.getFloatingSunTeeth()
        if self.Ns_fs > 0:
            self.dp_fs    = self.module * self.Ns_fs
            self.db_fs    = self.dp_fs * np.cos(self.pressure_angle)
            self.alpha_fs = (self.dp_fs**2 - self.db_fs**2)**0.5 / self.db_fs * 180/np.pi - self.pressure_angle_deg
            self.beta_fs  = (360/(4*self.Ns_fs) - self.alpha_fs) * 2
        else:
            self.dp_fs = self.db_fs = self.alpha_fs = self.beta_fs = 0.0
        self.fw_fs              = max(self.fw_p_s, gb.fwFloatingSunMM)
        self.num_idler          = self.num_planet
        self.idler_angle_offset = 180 / self.num_planet
        sun_r = self.dp_s/2 + (self.module if gb.mainSunToothedInPlane2 else -1.25*self.module)
        self.fs_bore_dia        = 2 * (sun_r + gb.floatingSunBoreClrMM)
        self.fs_bore_wall       = (self.dp_fs/2 - 1.25*self.module) - self.fs_bore_dia/2
        self.fs_axial_clearance = self.design_params["floating_sun_axial_clearance"]

    def genEquationFile(self, motor_name="NO_MOTOR", gearRatioLL = 0.0, gearRatioUL = 0.0):
        # writing values into text file imported which is imported into solidworks
        self.setVariables()
        file_path = os.path.join(os.path.dirname(__file__), 'CADs', 'BIPATHWPG', 'Equation_Files', motor_name, f'bwpg_equations_{gearRatioLL}_{gearRatioUL}.txt')
        # print("File Path: ",file_path)
        with open(file_path, 'w') as eqFile:
            l = [
                f'"Np_b" = {self.Np_b}\n',
                f'"Np_s" = {self.Np_s}\n',
                f'"Nr_b" = {self.Nr_b}\n',
                f'"Nr_s" = {self.Nr_s}\n',
                f'"Ns" = {self.Ns}\n',
                f'"Motor_case_ID" = {self.Motor_case_ID}\n',
                f'"Motor_case_OD_base_to_chamfer" = {self.Motor_case_OD_base_to_chamfer}\n',
                f'"Motor_case_OD_max" = {self.Motor_case_OD_max}\n',
                f'"Motor_case_thickness" = {self.Motor_case_thickness}\n',
                f'"air_flow_hole_offset" = {self.air_flow_hole_offset}\n',
                f'"standard_bearing_insertion_chamfer" = {self.standard_bearing_insertion_chamfer}\n',
                f'"alpha_p_b" = {self.alpha_p_b}\n',
                f'"alpha_p_s" = {self.alpha_p_s}\n',
                f'"alpha_r_b" = {self.alpha_r_b}\n',
                f'"alpha_r_s" = {self.alpha_r_s}\n',
                f'"alpha_s" = {self.alpha_s}\n',
                f'"base_plate_thickness" = {self.base_plate_thickness}\n',
                f'"bearing_ID" = {self.bearing_ID}\n',
                f'"bearing_OD" = {self.bearing_OD}\n',
                f'"bearing_height" = {self.bearing_height}\n',
                f'"bearing mount thickness" = {self.bearing_mount_thickness}\n',
                f'"bearing_retainer_thickness" = {self.bearing_retainer_thickness}\n',
                f'"beta_p_b" = {self.beta_p_b}\n',
                f'"beta_p_s" = {self.beta_p_s}\n',
                f'"beta_r_b" = {self.beta_r_b}\n',
                f'"beta_r_s" = {self.beta_r_s}\n',
                f'"beta_s" = {self.beta_s}\n',
                f'"carrier_PCD" = {self.carrier_PCD}\n',
                f'"carrier_bearing_step_width" = {self.carrier_bearing_step_width}\n',
                f'"carrier_small_ring_inner_bearing_ID" = {self.carrier_small_ring_inner_bearing_ID}\n',
                f'"carrier_small_ring_inner_bearing_OD" = {self.carrier_small_ring_inner_bearing_OD}\n',
                f'"carrier_small_ring_inner_bearing_flap" = {self.carrier_small_ring_inner_bearing_flap}\n',
                f'"carrier_small_ring_inner_bearing_height" = {self.carrier_small_ring_inner_bearing_height}\n',
                f'"carrier_thickness" = {self.carrier_thickness}\n',
                f'"carrier_trapezoidal_support_hole_PCD_offset_bearing_ID" = {self.carrier_trapezoidal_support_hole_PCD_offset_bearing_ID}\n',
                f'"carrier_trapezoidal_support_hole_dia" = {self.carrier_trapezoidal_support_hole_dia}\n',
                f'"carrier_trapezoidal_support_hole_socket_head_dia" = {self.carrier_trapezoidal_support_hole_socket_head_dia}\n',
                f'"carrier_trapezoidal_support_hole_wrench_size" = {self.carrier_trapezoidal_support_hole_wrench_size}\n',
                f'"carrier_trapezoidal_support_sun_offset" = {self.carrier_trapezoidal_support_sun_offset}\n',
                f'"case_dist" = {self.case_dist}\n',
                f'"case_mounting_PCD" = {self.case_mounting_PCD}\n',
                f'"case_mounting_bolt_depth" = {self.case_mounting_bolt_depth}\n',
                f'"case_mounting_hole_allen_socket_dia" = {self.case_mounting_hole_allen_socket_dia}\n',
                f'"case_mounting_hole_dia" = {self.case_mounting_hole_dia}\n',
                f'"case_mounting_hole_shift" = {self.case_mounting_hole_shift}\n',
                f'"case_mounting_nut_clearance" = {self.case_mounting_nut_clearance}\n',
                f'"case_mounting_nut_thickness" = {self.case_mounting_nut_thickness}\n',
                f'"case_mounting_surface_height" = {self.case_mounting_surface_height}\n',
                f'"case_mounting_wrench_size" = {self.case_mounting_wrench_size}\n',
                f'"central_hole_offset_from_motor_mount_PCD" = {self.central_hole_offset_from_motor_mount_PCD}\n',
                f'"clearance_case_mount_holes_shell_thickness" = {self.clearance_case_mount_holes_shell_thickness}\n',
                f'"clearance_motor_and_case" = {self.clearance_motor_and_case}\n',
                f'"clearance_planet" = {self.clearance_planet}\n',
                f'"clearance_sun_coupler_sec_carrier" = {self.clearance_sun_coupler_sec_carrier}\n',
                f'"clr_tip_root" = {self.clr_tip_root}\n',
                f'"clr_tip_root_s" = {self.clr_tip_root_s}\n',
                f'"db_p_b" = {self.db_p_b}\n',
                f'"db_p_s" = {self.db_p_s}\n',
                f'"db_r_b" = {self.db_r_b}\n',
                f'"db_r_s" = {self.db_r_s}\n',
                f'"db_s" = {self.db_s}\n',
                f'"dp_p_b" = {self.dp_p_b}\n',
                f'"dp_p_s" = {self.dp_p_s}\n',
                f'"dp_r_b" = {self.dp_r_b}\n',
                f'"dp_r_s" = {self.dp_r_s}\n',
                f'"dp_s" = {self.dp_s}\n',
                f'"driver_lower_holes_dist_from_center" = {self.driver_lower_holes_dist_from_center}\n',
                f'"driver_mount_height" = {self.driver_mount_height}\n',
                f'"driver_mount_holes_dia" = {self.driver_mount_holes_dia}\n',
                f'"driver_mount_inserts_OD" = {self.driver_mount_inserts_OD}\n',
                f'"driver_mount_thickness" = {self.driver_mount_thickness}\n',
                f'"driver_side_holes_dist_from_center" = {self.driver_side_holes_dist_from_center}\n',
                f'"driver_upper_holes_dist_from_center" = {self.driver_upper_holes_dist_from_center}\n',
                f'"fw_p_b" = {self.fw_p_b}\n',
                f'"fw_p_s" = {self.fw_p_s}\n',
                f'"fw_r_b" = {self.fw_r_b}\n',
                f'"fw_r_s" = {self.fw_r_s}\n',
                f'"fw_s_calc" = {self.fw_s_calc}\n',
                f'"fw_s_used" = {self.fw_s_used}\n',
                f'"gear_casing_big_ring_to_bearing_dist" = {self.gear_casing_big_ring_to_bearing_dist}\n',
                f'"gear_casing_thickness" = {self.gear_casing_thickness}\n',
                f'"h_a" = {self.h_a}\n',
                f'"h_b" = {self.h_b}\n',
                f'"h_f" = {self.h_f}\n',
                f'"module" = {self.module}\n',
                f'"motor_OD" = {self.motor_OD}\n',
                f'"motor_case_OD_base" = {self.motor_case_OD_base}\n',
                f'"motor_height" = {self.motor_height}\n',
                f'"motor_mount_hole_PCD" = {self.motor_mount_hole_PCD}\n',
                f'"motor_mount_hole_dia" = {self.motor_mount_hole_dia}\n',
                f'"motor_mount_hole_num" = {self.motor_mount_hole_num}\n',
                f'"motor_output_hole_CSK_OD" = {self.motor_output_hole_CSK_OD}\n',
                f'"motor_output_hole_CSK_head_height" = {self.motor_output_hole_CSK_head_height}\n',
                f'"motor_output_hole_PCD" = {self.motor_output_hole_PCD}\n',
                f'"motor_output_hole_dia" = {self.motor_output_hole_dia}\n',
                f'"motor_output_hole_num" = {self.motor_output_hole_num}\n',
                f'"num_planet" = {self.num_planet}\n',
                f'"output_mounting_PCD" = {self.output_mounting_PCD}\n',
                f'"output_mounting_hole_dia" = {self.output_mounting_hole_dia}\n',
                f'"output_mounting_nut_depth" = {self.output_mounting_nut_depth}\n',
                f'"output_mounting_nut_thickness" = {self.output_mounting_nut_thickness}\n',
                f'"output_mounting_nut_wrench_size" = {self.output_mounting_nut_wrench_size}\n',
                f'"pattern_bulge_dia" = {self.pattern_bulge_dia}\n',
                f'"pattern_depth" = {self.pattern_depth}\n',
                f'"pattern_num_bulge" = {self.pattern_num_bulge}\n',
                f'"pattern_offset_from_motor_case_OD_base" = {self.pattern_offset_from_motor_case_OD_base}\n',
                f'"planet_bearing_OD" = {self.planet_bearing_OD}\n',
                f'"planet_bearing_width" = {self.planet_bearing_width}\n',
                f'"planet_bore" = {self.planet_bore}\n',
                f'"planet_pin_bolt_dia" = {self.planet_pin_bolt_dia}\n',
                f'"planet_pin_bolt_wrench_size" = {self.planet_pin_bolt_wrench_size}\n',
                f'"planet_pin_socket_head_dia" = {self.planet_pin_socket_head_dia}\n',
                f'"planet_shaft_dia" = {self.planet_shaft_dia}\n',
                f'"planet_shaft_step_offset" = {self.planet_shaft_step_offset}\n',
                f'"pressure_angle" = {self.pressure_angle_deg}\n',
                f'"pressure angle" = {self.pressure_angle_deg}\n',
                f'"ring_OD_b" = {self.ring_OD_b}\n',
                f'"ring_radial_thickness" = {self.ring_radial_thickness}\n',
                f'"ring_to_chamfer_clearance" = {self.ring_to_chamfer_clearance}\n',
                f'"sec_carrier_thickness" = {self.sec_carrier_thickness}\n',
                f'"small_ring_case_thickness" = {self.small_ring_case_thickness}\n',
                f'"small_ring_output_wall_thickness" = {self.small_ring_output_wall_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_depth" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_depth}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_dia" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_dia}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_num" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_num}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench}\n',
                f'"standard_clearance_1_5mm" = {self.standard_clearance_1_5mm}\n',
                f'"standard_fillet_1_5mm" = {self.standard_fillet_1_5mm}\n',
                f'"sun_central_bolt_dia" = {self.sun_central_bolt_dia}\n',
                f'"sun_central_bolt_socket_head_dia" = {self.sun_central_bolt_socket_head_dia}\n',
                f'"sun_coupler_hub_thickness" = {self.sun_coupler_hub_thickness}\n',
                f'"sun_hub_dia" = {self.sun_hub_dia}\n',
                f'"sun_shaft_bearing_ID" = {self.sun_shaft_bearing_ID}\n',
                f'"sun_shaft_bearing_OD" = {self.sun_shaft_bearing_OD}\n',
                f'"sun_shaft_bearing_width" = {self.sun_shaft_bearing_width}\n',
                f'"wire_slot_dist_from_center" = {self.wire_slot_dist_from_center}\n',
                f'"wire_slot_length" = {self.wire_slot_length}\n',
                f'"wire_slot_radius" = {self.wire_slot_radius}\n',
                f'"tight_clearance_3DP" = {self.tight_clearance_3DP}\n',
                f'"loose_clearance_3DP" = {self.loose_clearance_3DP}\n',
                f'"Ns_fs" = {self.Ns_fs}\n',
                f'"dp_fs" = {self.dp_fs}\n',
                f'"db_fs" = {self.db_fs}\n',
                f'"alpha_fs" = {self.alpha_fs}\n',
                f'"beta_fs" = {self.beta_fs}\n',
                f'"fw_fs" = {self.fw_fs}\n',
                f'"num_idler" = {self.num_idler}\n',
                f'"idler_angle_offset" = {self.idler_angle_offset}\n',
                f'"fs_bore_dia" = {self.fs_bore_dia}\n',
                f'"fs_bore_wall" = {self.fs_bore_wall}\n',
                f'"fs_axial_clearance" = {self.fs_axial_clearance}\n',
            ]
            eqFile.writelines(l)

        file_path = os.path.join(os.path.dirname(__file__), 'CADs', 'BIPATHWPG', 'Equation_Files', motor_name, f'bwpg_equations_{gearRatioLL}_{gearRatioUL}_onshape.txt')
        # print("File Path: ",file_path)
        with open(file_path, 'w') as eqFile:
            l = [
                f'"Np_b" = {self.Np_b}\n',
                f'"Np_s" = {self.Np_s}\n',
                f'"Nr_b" = {self.Nr_b}\n',
                f'"Nr_s" = {self.Nr_s}\n',
                f'"Ns" = {self.Ns}\n',
                f'"Motor_case_ID" = {self.Motor_case_ID}\n',
                f'"Motor_case_OD_base_to_chamfer" = {self.Motor_case_OD_base_to_chamfer}\n',
                f'"Motor_case_OD_max" = {self.Motor_case_OD_max}\n',
                f'"Motor_case_thickness" = {self.Motor_case_thickness}\n',
                f'"air_flow_hole_offset" = {self.air_flow_hole_offset}\n',
                f'"standard_bearing_insertion_chamfer" = {self.standard_bearing_insertion_chamfer}\n',
                f'"alpha_p_b" = {self.alpha_p_b}\n',
                f'"alpha_p_s" = {self.alpha_p_s}\n',
                f'"alpha_r_b" = {self.alpha_r_b}\n',
                f'"alpha_r_s" = {self.alpha_r_s}\n',
                f'"alpha_s" = {self.alpha_s}\n',
                f'"base_plate_thickness" = {self.base_plate_thickness}\n',
                f'"bearing_ID" = {self.bearing_ID}\n',
                f'"bearing_OD" = {self.bearing_OD}\n',
                f'"bearing_height" = {self.bearing_height}\n',
                f'"bearing_mount_thickness" = {self.bearing_mount_thickness}\n',
                f'"bearing_retainer_thickness" = {self.bearing_retainer_thickness}\n',
                f'"beta_p_b" = {self.beta_p_b}\n',
                f'"beta_p_s" = {self.beta_p_s}\n',
                f'"beta_r_b" = {self.beta_r_b}\n',
                f'"beta_r_s" = {self.beta_r_s}\n',
                f'"beta_s" = {self.beta_s}\n',
                f'"carrier_PCD" = {self.carrier_PCD}\n',
                f'"carrier_bearing_step_width" = {self.carrier_bearing_step_width}\n',
                f'"carrier_small_ring_inner_bearing_ID" = {self.carrier_small_ring_inner_bearing_ID}\n',
                f'"carrier_small_ring_inner_bearing_OD" = {self.carrier_small_ring_inner_bearing_OD}\n',
                f'"carrier_small_ring_inner_bearing_flap" = {self.carrier_small_ring_inner_bearing_flap}\n',
                f'"carrier_small_ring_inner_bearing_height" = {self.carrier_small_ring_inner_bearing_height}\n',
                f'"carrier_thickness" = {self.carrier_thickness}\n',
                f'"carrier_trapezoidal_support_hole_PCD_offset_bearing_ID" = {self.carrier_trapezoidal_support_hole_PCD_offset_bearing_ID}\n',
                f'"carrier_trapezoidal_support_hole_dia" = {self.carrier_trapezoidal_support_hole_dia}\n',
                f'"carrier_trapezoidal_support_hole_socket_head_dia" = {self.carrier_trapezoidal_support_hole_socket_head_dia}\n',
                f'"carrier_trapezoidal_support_hole_wrench_size" = {self.carrier_trapezoidal_support_hole_wrench_size}\n',
                f'"carrier_trapezoidal_support_sun_offset" = {self.carrier_trapezoidal_support_sun_offset}\n',
                f'"case_dist" = {self.case_dist}\n',
                f'"case_mounting_PCD" = {self.case_mounting_PCD}\n',
                f'"case_mounting_bolt_depth" = {self.case_mounting_bolt_depth}\n',
                f'"case_mounting_hole_allen_socket_dia" = {self.case_mounting_hole_allen_socket_dia}\n',
                f'"case_mounting_hole_dia" = {self.case_mounting_hole_dia}\n',
                f'"case_mounting_hole_shift" = {self.case_mounting_hole_shift}\n',
                f'"case_mounting_nut_clearance" = {self.case_mounting_nut_clearance}\n',
                f'"case_mounting_nut_thickness" = {self.case_mounting_nut_thickness}\n',
                f'"case_mounting_surface_height" = {self.case_mounting_surface_height}\n',
                f'"case_mounting_wrench_size" = {self.case_mounting_wrench_size}\n',
                f'"central_hole_offset_from_motor_mount_PCD" = {self.central_hole_offset_from_motor_mount_PCD}\n',
                f'"clearance_case_mount_holes_shell_thickness" = {self.clearance_case_mount_holes_shell_thickness}\n',
                f'"clearance_motor_and_case" = {self.clearance_motor_and_case}\n',
                f'"clearance_planet" = {self.clearance_planet}\n',
                f'"clearance_sun_coupler_sec_carrier" = {self.clearance_sun_coupler_sec_carrier}\n',
                f'"clr_tip_root" = {self.clr_tip_root}\n',
                f'"clr_tip_root_s" = {self.clr_tip_root_s}\n',
                f'"db_p_b" = {self.db_p_b}\n',
                f'"db_p_s" = {self.db_p_s}\n',
                f'"db_r_b" = {self.db_r_b}\n',
                f'"db_r_s" = {self.db_r_s}\n',
                f'"db_s" = {self.db_s}\n',
                f'"dp_p_b" = {self.dp_p_b}\n',
                f'"dp_p_s" = {self.dp_p_s}\n',
                f'"dp_r_b" = {self.dp_r_b}\n',
                f'"dp_r_s" = {self.dp_r_s}\n',
                f'"dp_s" = {self.dp_s}\n',
                f'"driver_lower_holes_dist_from_center" = {self.driver_lower_holes_dist_from_center}\n',
                f'"driver_mount_height" = {self.driver_mount_height}\n',
                f'"driver_mount_holes_dia" = {self.driver_mount_holes_dia}\n',
                f'"driver_mount_inserts_OD" = {self.driver_mount_inserts_OD}\n',
                f'"driver_mount_thickness" = {self.driver_mount_thickness}\n',
                f'"driver_side_holes_dist_from_center" = {self.driver_side_holes_dist_from_center}\n',
                f'"driver_upper_holes_dist_from_center" = {self.driver_upper_holes_dist_from_center}\n',
                f'"fw_p_b" = {self.fw_p_b}\n',
                f'"fw_p_s" = {self.fw_p_s}\n',
                f'"fw_r_b" = {self.fw_r_b}\n',
                f'"fw_r_s" = {self.fw_r_s}\n',
                f'"fw_s_calc" = {self.fw_s_calc}\n',
                f'"fw_s_used" = {self.fw_s_used}\n',
                f'"gear_casing_big_ring_to_bearing_dist" = {self.gear_casing_big_ring_to_bearing_dist}\n',
                f'"gear_casing_thickness" = {self.gear_casing_thickness}\n',
                f'"h_a" = {self.h_a}\n',
                f'"h_b" = {self.h_b}\n',
                f'"h_f" = {self.h_f}\n',
                f'"module" = {self.module}\n',
                f'"motor_OD" = {self.motor_OD}\n',
                f'"motor_case_OD_base" = {self.motor_case_OD_base}\n',
                f'"motor_height" = {self.motor_height}\n',
                f'"motor_mount_hole_PCD" = {self.motor_mount_hole_PCD}\n',
                f'"motor_mount_hole_dia" = {self.motor_mount_hole_dia}\n',
                f'"motor_mount_hole_num" = {self.motor_mount_hole_num}\n',
                f'"motor_output_hole_CSK_OD" = {self.motor_output_hole_CSK_OD}\n',
                f'"motor_output_hole_CSK_head_height" = {self.motor_output_hole_CSK_head_height}\n',
                f'"motor_output_hole_PCD" = {self.motor_output_hole_PCD}\n',
                f'"motor_output_hole_dia" = {self.motor_output_hole_dia}\n',
                f'"motor_output_hole_num" = {self.motor_output_hole_num}\n',
                f'"num_planet" = {self.num_planet}\n',
                f'"output_mounting_PCD" = {self.output_mounting_PCD}\n',
                f'"output_mounting_hole_dia" = {self.output_mounting_hole_dia}\n',
                f'"output_mounting_nut_depth" = {self.output_mounting_nut_depth}\n',
                f'"output_mounting_nut_thickness" = {self.output_mounting_nut_thickness}\n',
                f'"output_mounting_nut_wrench_size" = {self.output_mounting_nut_wrench_size}\n',
                f'"pattern_bulge_dia" = {self.pattern_bulge_dia}\n',
                f'"pattern_depth" = {self.pattern_depth}\n',
                f'"pattern_num_bulge" = {self.pattern_num_bulge}\n',
                f'"pattern_offset_from_motor_case_OD_base" = {self.pattern_offset_from_motor_case_OD_base}\n',
                f'"planet_bearing_OD" = {self.planet_bearing_OD}\n',
                f'"planet_bearing_width" = {self.planet_bearing_width}\n',
                f'"planet_bore" = {self.planet_bore}\n',
                f'"planet_pin_bolt_dia" = {self.planet_pin_bolt_dia}\n',
                f'"planet_pin_bolt_wrench_size" = {self.planet_pin_bolt_wrench_size}\n',
                f'"planet_pin_socket_head_dia" = {self.planet_pin_socket_head_dia}\n',
                f'"planet_shaft_dia" = {self.planet_shaft_dia}\n',
                f'"planet_shaft_step_offset" = {self.planet_shaft_step_offset}\n',
                f'"pressure_angle" = {self.pressure_angle_deg}\n',
                # f'"pressure angle" = {self.pressure_angle_deg}\n',
                f'"ring_OD_b" = {self.ring_OD_b}\n',
                f'"ring_radial_thickness" = {self.ring_radial_thickness}\n',
                f'"ring_to_chamfer_clearance" = {self.ring_to_chamfer_clearance}\n',
                f'"sec_carrier_thickness" = {self.sec_carrier_thickness}\n',
                f'"small_ring_case_thickness" = {self.small_ring_case_thickness}\n',
                f'"small_ring_output_wall_thickness" = {self.small_ring_output_wall_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_depth" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_depth}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_dia" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_dia}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_num" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_num}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench}\n',
                f'"standard_clearance_1_5mm" = {self.standard_clearance_1_5mm}\n',
                f'"standard_fillet_1_5mm" = {self.standard_fillet_1_5mm}\n',
                f'"sun_central_bolt_dia" = {self.sun_central_bolt_dia}\n',
                f'"sun_central_bolt_socket_head_dia" = {self.sun_central_bolt_socket_head_dia}\n',
                f'"sun_coupler_hub_thickness" = {self.sun_coupler_hub_thickness}\n',
                f'"sun_hub_dia" = {self.sun_hub_dia}\n',
                f'"sun_shaft_bearing_ID" = {self.sun_shaft_bearing_ID}\n',
                f'"sun_shaft_bearing_OD" = {self.sun_shaft_bearing_OD}\n',
                f'"sun_shaft_bearing_width" = {self.sun_shaft_bearing_width}\n',
                f'"wire_slot_dist_from_center" = {self.wire_slot_dist_from_center}\n',
                f'"wire_slot_length" = {self.wire_slot_length}\n',
                f'"wire_slot_radius" = {self.wire_slot_radius}\n',
                f'"tight_clearance_3DP" = {self.tight_clearance_3DP}\n',
                f'"loose_clearance_3DP" = {self.loose_clearance_3DP}\n',
                f'"Ns_fs" = {self.Ns_fs}\n',
                f'"dp_fs" = {self.dp_fs}\n',
                f'"db_fs" = {self.db_fs}\n',
                f'"alpha_fs" = {self.alpha_fs}\n',
                f'"beta_fs" = {self.beta_fs}\n',
                f'"fw_fs" = {self.fw_fs}\n',
                f'"num_idler" = {self.num_idler}\n',
                f'"idler_angle_offset" = {self.idler_angle_offset}\n',
                f'"fs_bore_dia" = {self.fs_bore_dia}\n',
                f'"fs_bore_wall" = {self.fs_bore_wall}\n',
                f'"fs_axial_clearance" = {self.fs_axial_clearance}\n',
            ]
            eqFile.writelines(l)

    def genEquationFile_editCADdirectly(self):
        # writing values into text file imported which is imported into solidworks
        self.setVariables()
        file_path = os.path.join(os.path.dirname(__file__), 'CADs', 'BIPATHWPG', 'wpg_equations.txt')
        # print("File Path: ",file_path)
        with open(file_path, 'w') as eqFile:
            l = [
                f'"Np_b" = {self.Np_b}\n',
                f'"Np_s" = {self.Np_s}\n',
                f'"Nr_b" = {self.Nr_b}\n',
                f'"Nr_s" = {self.Nr_s}\n',
                f'"Ns" = {self.Ns}\n',
                f'"Motor_case_ID" = {self.Motor_case_ID}\n',
                f'"Motor_case_OD_base_to_chamfer" = {self.Motor_case_OD_base_to_chamfer}\n',
                f'"Motor_case_OD_max" = {self.Motor_case_OD_max}\n',
                f'"Motor_case_thickness" = {self.Motor_case_thickness}\n',
                f'"air_flow_hole_offset" = {self.air_flow_hole_offset}\n',
                f'"standard_bearing_insertion_chamfer" = {self.standard_bearing_insertion_chamfer}\n',
                f'"alpha_p_b" = {self.alpha_p_b}\n',
                f'"alpha_p_s" = {self.alpha_p_s}\n',
                f'"alpha_r_b" = {self.alpha_r_b}\n',
                f'"alpha_r_s" = {self.alpha_r_s}\n',
                f'"alpha_s" = {self.alpha_s}\n',
                f'"base_plate_thickness" = {self.base_plate_thickness}\n',
                f'"bearing_ID" = {self.bearing_ID}\n',
                f'"bearing_OD" = {self.bearing_OD}\n',
                f'"bearing_height" = {self.bearing_height}\n',
                f'"bearing mount thickness" = {self.bearing_mount_thickness}\n',
                f'"bearing_retainer_thickness" = {self.bearing_retainer_thickness}\n',
                f'"beta_p_b" = {self.beta_p_b}\n',
                f'"beta_p_s" = {self.beta_p_s}\n',
                f'"beta_r_b" = {self.beta_r_b}\n',
                f'"beta_r_s" = {self.beta_r_s}\n',
                f'"beta_s" = {self.beta_s}\n',
                f'"carrier_PCD" = {self.carrier_PCD}\n',
                f'"carrier_bearing_step_width" = {self.carrier_bearing_step_width}\n',
                f'"carrier_small_ring_inner_bearing_ID" = {self.carrier_small_ring_inner_bearing_ID}\n',
                f'"carrier_small_ring_inner_bearing_OD" = {self.carrier_small_ring_inner_bearing_OD}\n',
                f'"carrier_small_ring_inner_bearing_flap" = {self.carrier_small_ring_inner_bearing_flap}\n',
                f'"carrier_small_ring_inner_bearing_height" = {self.carrier_small_ring_inner_bearing_height}\n',
                f'"carrier_thickness" = {self.carrier_thickness}\n',
                f'"carrier_trapezoidal_support_hole_PCD_offset_bearing_ID" = {self.carrier_trapezoidal_support_hole_PCD_offset_bearing_ID}\n',
                f'"carrier_trapezoidal_support_hole_dia" = {self.carrier_trapezoidal_support_hole_dia}\n',
                f'"carrier_trapezoidal_support_hole_socket_head_dia" = {self.carrier_trapezoidal_support_hole_socket_head_dia}\n',
                f'"carrier_trapezoidal_support_hole_wrench_size" = {self.carrier_trapezoidal_support_hole_wrench_size}\n',
                f'"carrier_trapezoidal_support_sun_offset" = {self.carrier_trapezoidal_support_sun_offset}\n',
                f'"case_dist" = {self.case_dist}\n',
                f'"case_mounting_PCD" = {self.case_mounting_PCD}\n',
                f'"case_mounting_bolt_depth" = {self.case_mounting_bolt_depth}\n',
                f'"case_mounting_hole_allen_socket_dia" = {self.case_mounting_hole_allen_socket_dia}\n',
                f'"case_mounting_hole_dia" = {self.case_mounting_hole_dia}\n',
                f'"case_mounting_hole_shift" = {self.case_mounting_hole_shift}\n',
                f'"case_mounting_nut_clearance" = {self.case_mounting_nut_clearance}\n',
                f'"case_mounting_nut_thickness" = {self.case_mounting_nut_thickness}\n',
                f'"case_mounting_surface_height" = {self.case_mounting_surface_height}\n',
                f'"case_mounting_wrench_size" = {self.case_mounting_wrench_size}\n',
                f'"central_hole_offset_from_motor_mount_PCD" = {self.central_hole_offset_from_motor_mount_PCD}\n',
                f'"clearance_case_mount_holes_shell_thickness" = {self.clearance_case_mount_holes_shell_thickness}\n',
                f'"clearance_motor_and_case" = {self.clearance_motor_and_case}\n',
                f'"clearance_planet" = {self.clearance_planet}\n',
                f'"clearance_sun_coupler_sec_carrier" = {self.clearance_sun_coupler_sec_carrier}\n',
                f'"clr_tip_root" = {self.clr_tip_root}\n',
                f'"clr_tip_root_s" = {self.clr_tip_root_s}\n',
                f'"db_p_b" = {self.db_p_b}\n',
                f'"db_p_s" = {self.db_p_s}\n',
                f'"db_r_b" = {self.db_r_b}\n',
                f'"db_r_s" = {self.db_r_s}\n',
                f'"db_s" = {self.db_s}\n',
                f'"dp_p_b" = {self.dp_p_b}\n',
                f'"dp_p_s" = {self.dp_p_s}\n',
                f'"dp_r_b" = {self.dp_r_b}\n',
                f'"dp_r_s" = {self.dp_r_s}\n',
                f'"dp_s" = {self.dp_s}\n',
                f'"driver_lower_holes_dist_from_center" = {self.driver_lower_holes_dist_from_center}\n',
                f'"driver_mount_height" = {self.driver_mount_height}\n',
                f'"driver_mount_holes_dia" = {self.driver_mount_holes_dia}\n',
                f'"driver_mount_inserts_OD" = {self.driver_mount_inserts_OD}\n',
                f'"driver_mount_thickness" = {self.driver_mount_thickness}\n',
                f'"driver_side_holes_dist_from_center" = {self.driver_side_holes_dist_from_center}\n',
                f'"driver_upper_holes_dist_from_center" = {self.driver_upper_holes_dist_from_center}\n',
                f'"fw_p_b" = {self.fw_p_b}\n',
                f'"fw_p_s" = {self.fw_p_s}\n',
                f'"fw_r_b" = {self.fw_r_b}\n',
                f'"fw_r_s" = {self.fw_r_s}\n',
                f'"fw_s_calc" = {self.fw_s_calc}\n',
                f'"fw_s_used" = {self.fw_s_used}\n',
                f'"gear_casing_big_ring_to_bearing_dist" = {self.gear_casing_big_ring_to_bearing_dist}\n',
                f'"gear_casing_thickness" = {self.gear_casing_thickness}\n',
                f'"h_a" = {self.h_a}\n',
                f'"h_b" = {self.h_b}\n',
                f'"h_f" = {self.h_f}\n',
                f'"module" = {self.module}\n',
                f'"motor_OD" = {self.motor_OD}\n',
                f'"motor_case_OD_base" = {self.motor_case_OD_base}\n',
                f'"motor_height" = {self.motor_height}\n',
                f'"motor_mount_hole_PCD" = {self.motor_mount_hole_PCD}\n',
                f'"motor_mount_hole_dia" = {self.motor_mount_hole_dia}\n',
                f'"motor_mount_hole_num" = {self.motor_mount_hole_num}\n',
                f'"motor_output_hole_CSK_OD" = {self.motor_output_hole_CSK_OD}\n',
                f'"motor_output_hole_CSK_head_height" = {self.motor_output_hole_CSK_head_height}\n',
                f'"motor_output_hole_PCD" = {self.motor_output_hole_PCD}\n',
                f'"motor_output_hole_dia" = {self.motor_output_hole_dia}\n',
                f'"motor_output_hole_num" = {self.motor_output_hole_num}\n',
                f'"num_planet" = {self.num_planet}\n',
                f'"output_mounting_PCD" = {self.output_mounting_PCD}\n',
                f'"output_mounting_hole_dia" = {self.output_mounting_hole_dia}\n',
                f'"output_mounting_nut_depth" = {self.output_mounting_nut_depth}\n',
                f'"output_mounting_nut_thickness" = {self.output_mounting_nut_thickness}\n',
                f'"output_mounting_nut_wrench_size" = {self.output_mounting_nut_wrench_size}\n',
                f'"pattern_bulge_dia" = {self.pattern_bulge_dia}\n',
                f'"pattern_depth" = {self.pattern_depth}\n',
                f'"pattern_num_bulge" = {self.pattern_num_bulge}\n',
                f'"pattern_offset_from_motor_case_OD_base" = {self.pattern_offset_from_motor_case_OD_base}\n',
                f'"planet_bearing_OD" = {self.planet_bearing_OD}\n',
                f'"planet_bearing_width" = {self.planet_bearing_width}\n',
                f'"planet_bore" = {self.planet_bore}\n',
                f'"planet_pin_bolt_dia" = {self.planet_pin_bolt_dia}\n',
                f'"planet_pin_bolt_wrench_size" = {self.planet_pin_bolt_wrench_size}\n',
                f'"planet_pin_socket_head_dia" = {self.planet_pin_socket_head_dia}\n',
                f'"planet_shaft_dia" = {self.planet_shaft_dia}\n',
                f'"planet_shaft_step_offset" = {self.planet_shaft_step_offset}\n',
                f'"pressure_angle" = {self.pressure_angle_deg}\n',
                f'"pressure angle" = {self.pressure_angle_deg}\n',
                f'"ring_OD_b" = {self.ring_OD_b}\n',
                f'"ring_radial_thickness" = {self.ring_radial_thickness}\n',
                f'"ring_to_chamfer_clearance" = {self.ring_to_chamfer_clearance}\n',
                f'"sec_carrier_thickness" = {self.sec_carrier_thickness}\n',
                f'"small_ring_case_thickness" = {self.small_ring_case_thickness}\n',
                f'"small_ring_output_wall_thickness" = {self.small_ring_output_wall_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_depth" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_depth}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_dia" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_dia}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_num" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_num}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench}\n',
                f'"standard_clearance_1_5mm" = {self.standard_clearance_1_5mm}\n',
                f'"standard_fillet_1_5mm" = {self.standard_fillet_1_5mm}\n',
                f'"sun_central_bolt_dia" = {self.sun_central_bolt_dia}\n',
                f'"sun_central_bolt_socket_head_dia" = {self.sun_central_bolt_socket_head_dia}\n',
                f'"sun_coupler_hub_thickness" = {self.sun_coupler_hub_thickness}\n',
                f'"sun_hub_dia" = {self.sun_hub_dia}\n',
                f'"sun_shaft_bearing_ID" = {self.sun_shaft_bearing_ID}\n',
                f'"sun_shaft_bearing_OD" = {self.sun_shaft_bearing_OD}\n',
                f'"sun_shaft_bearing_width" = {self.sun_shaft_bearing_width}\n',
                f'"wire_slot_dist_from_center" = {self.wire_slot_dist_from_center}\n',
                f'"wire_slot_length" = {self.wire_slot_length}\n',
                f'"wire_slot_radius" = {self.wire_slot_radius}\n',
                f'"tight_clearance_3DP" = {self.tight_clearance_3DP}\n',
                f'"loose_clearance_3DP" = {self.loose_clearance_3DP}\n',
                f'"Ns_fs" = {self.Ns_fs}\n',
                f'"dp_fs" = {self.dp_fs}\n',
                f'"db_fs" = {self.db_fs}\n',
                f'"alpha_fs" = {self.alpha_fs}\n',
                f'"beta_fs" = {self.beta_fs}\n',
                f'"fw_fs" = {self.fw_fs}\n',
                f'"num_idler" = {self.num_idler}\n',
                f'"idler_angle_offset" = {self.idler_angle_offset}\n',
                f'"fs_bore_dia" = {self.fs_bore_dia}\n',
                f'"fs_bore_wall" = {self.fs_bore_wall}\n',
                f'"fs_axial_clearance" = {self.fs_axial_clearance}\n',
            ]
            eqFile.writelines(l)


        file_path = os.path.join(os.path.dirname(__file__), 'CADs', 'BIPATHWPG', 'wpg_equations_onshape.txt')
        # print("File Path: ",file_path)
        with open(file_path, 'w') as eqFile:
            l = [
                f'"Np_b" = {self.Np_b}\n',
                f'"Np_s" = {self.Np_s}\n',
                f'"Nr_b" = {self.Nr_b}\n',
                f'"Nr_s" = {self.Nr_s}\n',
                f'"Ns" = {self.Ns}\n',
                f'"Motor_case_ID" = {self.Motor_case_ID}\n',
                f'"Motor_case_OD_base_to_chamfer" = {self.Motor_case_OD_base_to_chamfer}\n',
                f'"Motor_case_OD_max" = {self.Motor_case_OD_max}\n',
                f'"Motor_case_thickness" = {self.Motor_case_thickness}\n',
                f'"air_flow_hole_offset" = {self.air_flow_hole_offset}\n',
                f'"standard_bearing_insertion_chamfer" = {self.standard_bearing_insertion_chamfer}\n',
                f'"alpha_p_b" = {self.alpha_p_b}\n',
                f'"alpha_p_s" = {self.alpha_p_s}\n',
                f'"alpha_r_b" = {self.alpha_r_b}\n',
                f'"alpha_r_s" = {self.alpha_r_s}\n',
                f'"alpha_s" = {self.alpha_s}\n',
                f'"base_plate_thickness" = {self.base_plate_thickness}\n',
                f'"bearing_ID" = {self.bearing_ID}\n',
                f'"bearing_OD" = {self.bearing_OD}\n',
                f'"bearing_height" = {self.bearing_height}\n',
                f'"bearing_mount_thickness" = {self.bearing_mount_thickness}\n',
                f'"bearing_retainer_thickness" = {self.bearing_retainer_thickness}\n',
                f'"beta_p_b" = {self.beta_p_b}\n',
                f'"beta_p_s" = {self.beta_p_s}\n',
                f'"beta_r_b" = {self.beta_r_b}\n',
                f'"beta_r_s" = {self.beta_r_s}\n',
                f'"beta_s" = {self.beta_s}\n',
                f'"carrier_PCD" = {self.carrier_PCD}\n',
                f'"carrier_bearing_step_width" = {self.carrier_bearing_step_width}\n',
                f'"carrier_small_ring_inner_bearing_ID" = {self.carrier_small_ring_inner_bearing_ID}\n',
                f'"carrier_small_ring_inner_bearing_OD" = {self.carrier_small_ring_inner_bearing_OD}\n',
                f'"carrier_small_ring_inner_bearing_flap" = {self.carrier_small_ring_inner_bearing_flap}\n',
                f'"carrier_small_ring_inner_bearing_height" = {self.carrier_small_ring_inner_bearing_height}\n',
                f'"carrier_thickness" = {self.carrier_thickness}\n',
                f'"carrier_trapezoidal_support_hole_PCD_offset_bearing_ID" = {self.carrier_trapezoidal_support_hole_PCD_offset_bearing_ID}\n',
                f'"carrier_trapezoidal_support_hole_dia" = {self.carrier_trapezoidal_support_hole_dia}\n',
                f'"carrier_trapezoidal_support_hole_socket_head_dia" = {self.carrier_trapezoidal_support_hole_socket_head_dia}\n',
                f'"carrier_trapezoidal_support_hole_wrench_size" = {self.carrier_trapezoidal_support_hole_wrench_size}\n',
                f'"carrier_trapezoidal_support_sun_offset" = {self.carrier_trapezoidal_support_sun_offset}\n',
                f'"case_dist" = {self.case_dist}\n',
                f'"case_mounting_PCD" = {self.case_mounting_PCD}\n',
                f'"case_mounting_bolt_depth" = {self.case_mounting_bolt_depth}\n',
                f'"case_mounting_hole_allen_socket_dia" = {self.case_mounting_hole_allen_socket_dia}\n',
                f'"case_mounting_hole_dia" = {self.case_mounting_hole_dia}\n',
                f'"case_mounting_hole_shift" = {self.case_mounting_hole_shift}\n',
                f'"case_mounting_nut_clearance" = {self.case_mounting_nut_clearance}\n',
                f'"case_mounting_nut_thickness" = {self.case_mounting_nut_thickness}\n',
                f'"case_mounting_surface_height" = {self.case_mounting_surface_height}\n',
                f'"case_mounting_wrench_size" = {self.case_mounting_wrench_size}\n',
                f'"central_hole_offset_from_motor_mount_PCD" = {self.central_hole_offset_from_motor_mount_PCD}\n',
                f'"clearance_case_mount_holes_shell_thickness" = {self.clearance_case_mount_holes_shell_thickness}\n',
                f'"clearance_motor_and_case" = {self.clearance_motor_and_case}\n',
                f'"clearance_planet" = {self.clearance_planet}\n',
                f'"clearance_sun_coupler_sec_carrier" = {self.clearance_sun_coupler_sec_carrier}\n',
                f'"clr_tip_root" = {self.clr_tip_root}\n',
                f'"clr_tip_root_s" = {self.clr_tip_root_s}\n',
                f'"db_p_b" = {self.db_p_b}\n',
                f'"db_p_s" = {self.db_p_s}\n',
                f'"db_r_b" = {self.db_r_b}\n',
                f'"db_r_s" = {self.db_r_s}\n',
                f'"db_s" = {self.db_s}\n',
                f'"dp_p_b" = {self.dp_p_b}\n',
                f'"dp_p_s" = {self.dp_p_s}\n',
                f'"dp_r_b" = {self.dp_r_b}\n',
                f'"dp_r_s" = {self.dp_r_s}\n',
                f'"dp_s" = {self.dp_s}\n',
                f'"driver_lower_holes_dist_from_center" = {self.driver_lower_holes_dist_from_center}\n',
                f'"driver_mount_height" = {self.driver_mount_height}\n',
                f'"driver_mount_holes_dia" = {self.driver_mount_holes_dia}\n',
                f'"driver_mount_inserts_OD" = {self.driver_mount_inserts_OD}\n',
                f'"driver_mount_thickness" = {self.driver_mount_thickness}\n',
                f'"driver_side_holes_dist_from_center" = {self.driver_side_holes_dist_from_center}\n',
                f'"driver_upper_holes_dist_from_center" = {self.driver_upper_holes_dist_from_center}\n',
                f'"fw_p_b" = {self.fw_p_b}\n',
                f'"fw_p_s" = {self.fw_p_s}\n',
                f'"fw_r_b" = {self.fw_r_b}\n',
                f'"fw_r_s" = {self.fw_r_s}\n',
                f'"fw_s_calc" = {self.fw_s_calc}\n',
                f'"fw_s_used" = {self.fw_s_used}\n',
                f'"gear_casing_big_ring_to_bearing_dist" = {self.gear_casing_big_ring_to_bearing_dist}\n',
                f'"gear_casing_thickness" = {self.gear_casing_thickness}\n',
                f'"h_a" = {self.h_a}\n',
                f'"h_b" = {self.h_b}\n',
                f'"h_f" = {self.h_f}\n',
                f'"module" = {self.module}\n',
                f'"motor_OD" = {self.motor_OD}\n',
                f'"motor_case_OD_base" = {self.motor_case_OD_base}\n',
                f'"motor_height" = {self.motor_height}\n',
                f'"motor_mount_hole_PCD" = {self.motor_mount_hole_PCD}\n',
                f'"motor_mount_hole_dia" = {self.motor_mount_hole_dia}\n',
                f'"motor_mount_hole_num" = {self.motor_mount_hole_num}\n',
                f'"motor_output_hole_CSK_OD" = {self.motor_output_hole_CSK_OD}\n',
                f'"motor_output_hole_CSK_head_height" = {self.motor_output_hole_CSK_head_height}\n',
                f'"motor_output_hole_PCD" = {self.motor_output_hole_PCD}\n',
                f'"motor_output_hole_dia" = {self.motor_output_hole_dia}\n',
                f'"motor_output_hole_num" = {self.motor_output_hole_num}\n',
                f'"num_planet" = {self.num_planet}\n',
                f'"output_mounting_PCD" = {self.output_mounting_PCD}\n',
                f'"output_mounting_hole_dia" = {self.output_mounting_hole_dia}\n',
                f'"output_mounting_nut_depth" = {self.output_mounting_nut_depth}\n',
                f'"output_mounting_nut_thickness" = {self.output_mounting_nut_thickness}\n',
                f'"output_mounting_nut_wrench_size" = {self.output_mounting_nut_wrench_size}\n',
                f'"pattern_bulge_dia" = {self.pattern_bulge_dia}\n',
                f'"pattern_depth" = {self.pattern_depth}\n',
                f'"pattern_num_bulge" = {self.pattern_num_bulge}\n',
                f'"pattern_offset_from_motor_case_OD_base" = {self.pattern_offset_from_motor_case_OD_base}\n',
                f'"planet_bearing_OD" = {self.planet_bearing_OD}\n',
                f'"planet_bearing_width" = {self.planet_bearing_width}\n',
                f'"planet_bore" = {self.planet_bore}\n',
                f'"planet_pin_bolt_dia" = {self.planet_pin_bolt_dia}\n',
                f'"planet_pin_bolt_wrench_size" = {self.planet_pin_bolt_wrench_size}\n',
                f'"planet_pin_socket_head_dia" = {self.planet_pin_socket_head_dia}\n',
                f'"planet_shaft_dia" = {self.planet_shaft_dia}\n',
                f'"planet_shaft_step_offset" = {self.planet_shaft_step_offset}\n',
                f'"pressure_angle" = {self.pressure_angle_deg}\n',
                # f'"pressure angle" = {self.pressure_angle_deg}\n',
                f'"ring_OD_b" = {self.ring_OD_b}\n',
                f'"ring_radial_thickness" = {self.ring_radial_thickness}\n',
                f'"ring_to_chamfer_clearance" = {self.ring_to_chamfer_clearance}\n',
                f'"sec_carrier_thickness" = {self.sec_carrier_thickness}\n',
                f'"small_ring_case_thickness" = {self.small_ring_case_thickness}\n',
                f'"small_ring_output_wall_thickness" = {self.small_ring_output_wall_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_OD}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_CSK_head_height}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_depth" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_depth}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_dia" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_dia}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_num" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_num}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd" = {self.small_ring_output_wall_to_bearing_shaft_attachement_hole_pcd}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_thickness}\n',
                f'"small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench" = {self.small_ring_output_wall_to_bearing_shaft_attachement_nut_wrench}\n',
                f'"standard_clearance_1_5mm" = {self.standard_clearance_1_5mm}\n',
                f'"standard_fillet_1_5mm" = {self.standard_fillet_1_5mm}\n',
                f'"sun_central_bolt_dia" = {self.sun_central_bolt_dia}\n',
                f'"sun_central_bolt_socket_head_dia" = {self.sun_central_bolt_socket_head_dia}\n',
                f'"sun_coupler_hub_thickness" = {self.sun_coupler_hub_thickness}\n',
                f'"sun_hub_dia" = {self.sun_hub_dia}\n',
                f'"sun_shaft_bearing_ID" = {self.sun_shaft_bearing_ID}\n',
                f'"sun_shaft_bearing_OD" = {self.sun_shaft_bearing_OD}\n',
                f'"sun_shaft_bearing_width" = {self.sun_shaft_bearing_width}\n',
                f'"wire_slot_dist_from_center" = {self.wire_slot_dist_from_center}\n',
                f'"wire_slot_length" = {self.wire_slot_length}\n',
                f'"wire_slot_radius" = {self.wire_slot_radius}\n',
                f'"tight_clearance_3DP" = {self.tight_clearance_3DP}\n',
                f'"loose_clearance_3DP" = {self.loose_clearance_3DP}\n',
                f'"Ns_fs" = {self.Ns_fs}\n',
                f'"dp_fs" = {self.dp_fs}\n',
                f'"db_fs" = {self.db_fs}\n',
                f'"alpha_fs" = {self.alpha_fs}\n',
                f'"beta_fs" = {self.beta_fs}\n',
                f'"fw_fs" = {self.fw_fs}\n',
                f'"num_idler" = {self.num_idler}\n',
                f'"idler_angle_offset" = {self.idler_angle_offset}\n',
                f'"fs_bore_dia" = {self.fs_bore_dia}\n',
                f'"fs_bore_wall" = {self.fs_bore_wall}\n',
                f'"fs_axial_clearance" = {self.fs_axial_clearance}\n',
            ]
            eqFile.writelines(l)
    
    # ----------------------------------------
    # Mass of New Design 
    #-----------------------------------------
    def getToothForces(self, constraintCheck=False):
        if constraintCheck:
            # Check if the constraints are satisfied
            if not self.wolfromPlanetaryGearbox.geometricConstraint():
                print("Geometric constraint not satisfied")
                return
            if not self.wolfromPlanetaryGearbox.meshingConstraint():
                print("Meshing constraint not satisfied")
                return
            if not self.wolfromPlanetaryGearbox.noPlanetInterferenceConstraint():
                print("No planet interference constraint not satisfied")
                return

        Ns          = self.bipathwolfromPlanetaryGearbox.Ns
        NpBig       = self.bipathwolfromPlanetaryGearbox.NpBig
        NpSmall     = self.bipathwolfromPlanetaryGearbox.NpSmall
        NrBig       = self.bipathwolfromPlanetaryGearbox.NrBig
        NrSmall     = self.bipathwolfromPlanetaryGearbox.NrSmall
        numPlanet   = self.bipathwolfromPlanetaryGearbox.numPlanet
        moduleBig   = self.bipathwolfromPlanetaryGearbox.moduleBig
        moduleSmall = self.bipathwolfromPlanetaryGearbox.moduleSmall

        RpBig_Mt   = self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetBigM()
        RpSmall_Mt = self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetSmallM()
        Rs_Mt      = self.bipathwolfromPlanetaryGearbox.getPCRadiusSunM()
        RrBig_Mt   = self.bipathwolfromPlanetaryGearbox.getPCRadiusRingBigM()
        RrSmall_Mt = self.bipathwolfromPlanetaryGearbox.getPCRadiusRingSmallM()

        wSun       = self.motor.getMaxMotorAngVelRadPerSec()
        wPlanet    = (-Ns / (2*NpBig) ) * wSun
        wCarrier   = (Ns / (Ns + NrBig)) * wSun
        wRingSmall = (Ns * (NpBig - NpSmall) / (2 * NrSmall * NpBig)) * wSun
        
        I1 = NrBig/Ns
        I2 = ( (NrBig * NpSmall) / (NpBig * NrSmall))
        I3 = RpSmall_Mt / RpBig_Mt

        Ft_sp_big = (self.serviceFactor*self.motor.getMaxMotorTorque()*1000) / (numPlanet * moduleBig * (Ns / 2))
        Ft_rp_big = ((self.serviceFactor*self.motor.getMaxMotorTorque()*1000) * (I1 + I2)) / (numPlanet * moduleBig * (NrBig/2) * (1-I2))
        Ft_rp_small = -((self.serviceFactor*self.motor.getMaxMotorTorque()*1000) * (1+I1)) / (numPlanet * moduleSmall * (NrSmall/2) * (1-I2))

        if (RpBig_Mt > RpSmall_Mt):
            Ft_sp_big_alt = (self.serviceFactor*self.motor.getMaxMotorTorque()) / (numPlanet * (Rs_Mt))
            Ft_rp_big_alt = ((self.serviceFactor*self.motor.getMaxMotorTorque()) * (1 + I3)) / (numPlanet * (Rs_Mt) * (1 - I3))
            Ft_rp_small_alt = -((self.serviceFactor*self.motor.getMaxMotorTorque()) * (2)) / (numPlanet * (Rs_Mt) * (1 - I3))

            # check the error in the force calculation
            if np.abs(Ft_sp_big - Ft_sp_big_alt) > 1e-6:
                print("----------------------------------------------")
                print("                   ERROR                      ")
                print("----------------------------------------------")
                print("Ft_sp_big not equal to Ft_sp_big_alt")
                print("Ft_sp_big:", Ft_sp_big)
                print("Ft_sp_big_alt:", Ft_sp_big_alt)

            if np.abs(Ft_rp_big - Ft_rp_big_alt) > 1e-6:
                print("----------------------------------------------")
                print("                   ERROR                      ")
                print("----------------------------------------------")
                print("Ft_rp_big not equal to Ft_rp_big_alt")
                print("Ft_rp_big:", Ft_rp_big)
                print("Ft_rp_big_alt:", Ft_rp_big_alt)

            if np.abs(Ft_rp_small - Ft_rp_small_alt) > 1e-6:
                print("----------------------------------------------")
                print("                   ERROR                      ")
                print("----------------------------------------------")
                print("Ft_rp_small not equal to Ft_rp_small_alt")
                print("Ft_rp_small:", Ft_rp_small)
                print("Ft_rp_small_alt:", Ft_rp_small_alt)
        else:
            print("Invalid value of RpBig and RpSmall")
            print("RpBig:", RpBig_Mt)
            print("NpBig:", NpBig)
            print(" ")
            print("RpSmall:", RpSmall_Mt)
            print("NpSmall:", NpSmall)

        Ft_rp_small = Ft_rp_small / 2   # ring load is shared by n planets + n idlers
        Ft = [Ft_sp_big, Ft_rp_big, Ft_rp_small]
        return Ft

    def lewisStressAnalysisMinFacewidth(self):
        # Check if the constraints are satisfied
        if not self.bipathwolfromPlanetaryGearbox.geometricConstraint():
            print("Geometric constraint not satisfied")
            return
        if not self.bipathwolfromPlanetaryGearbox.meshingConstraint():
            print("Meshing constraint not satisfied")
            return
        if not self.bipathwolfromPlanetaryGearbox.noPlanetInterferenceConstraint():
            print("No planet interference constraint not satisfied")
            return

        Ns          = self.bipathwolfromPlanetaryGearbox.Ns
        NpBig       = self.bipathwolfromPlanetaryGearbox.NpBig
        NpSmall     = self.bipathwolfromPlanetaryGearbox.NpSmall
        NrBig       = self.bipathwolfromPlanetaryGearbox.NrBig
        NrSmall     = self.bipathwolfromPlanetaryGearbox.NrSmall
        numPlanet   = self.bipathwolfromPlanetaryGearbox.numPlanet
        moduleBig   = self.bipathwolfromPlanetaryGearbox.moduleBig
        moduleSmall = self.bipathwolfromPlanetaryGearbox.moduleSmall

        RpBig = NpBig * moduleBig / 2
        RpSmall = NpSmall * moduleSmall / 2
        Rs = Ns * moduleBig / 2
        RrBig = NrBig * moduleBig / 2
        RrSmall = NrSmall * moduleSmall / 2

        wSun       = self.motor.getMaxMotorAngVelRadPerSec()
        wPlanet    = (-Ns / (2*NpBig) ) * wSun
        wCarrier   = (Ns / (Ns + NrBig)) * wSun
        wRingSmall = (Ns * (NpBig - NpSmall) / (2 * NrSmall * NpBig)) * wSun

        [Ft_sp_big, Ft_rp_big, Ft_rp_small]  = self.getToothForces(False)

        ySun         = 0.154 - 0.912/Ns
        yPlanetBig   = 0.154 - 0.912/NpBig
        yPlanetSmall = 0.154 - 0.912/NpSmall
        yRingSmall   = 0.154 - 0.912/NrSmall
        yRingBig     = 0.154 - 0.912/NrBig

        V_sp_big = (self.bipathwolfromPlanetaryGearbox.getPCRadiusSunM() * wSun)
        V_rp_big = (wCarrier*(self.bipathwolfromPlanetaryGearbox.getPCRadiusSunM() + self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetBigM()) + 
                    wPlanet*(self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetBigM()))
        V_rp_small = (wCarrier*(self.bipathwolfromPlanetaryGearbox.getPCRadiusSunM() + self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetBigM()) +
                      wPlanet*(self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetSmallM()))
        
        # Check 
        V_rp_small_test = wRingSmall*(self.bipathwolfromPlanetaryGearbox.getPCRadiusSunM() + self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetBigM()
                                      + self.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetSmallM())
        
        if np.abs(V_rp_small - V_rp_small_test) > 1e-6:
            print("----------------------------------------------")
            print("                   ERROR                      ")
            print("----------------------------------------------")
            print("V_rp_small not equal to V_rp_small_test")
            print("V_rp_small:", V_rp_small)
            print("V_rp_small_test:", V_rp_small_test)
        
        if V_sp_big <= 7.5:
            Kv_sun = 3/(3+V_sp_big)
            Kv_planetBig1 = 3/(3+V_sp_big)
        elif V_sp_big > 7.5 and V_sp_big <= 12.5:
            Kv_sun = 4.5/(4.5 + V_sp_big)
            Kv_planetBig1 = 4.5/(4.5 + V_sp_big)
        else:
            Kv_sun = 4.5/(4.5 + V_sp_big)
            Kv_planetBig1 = 4.5/(4.5 + V_sp_big)

        if V_rp_big <= 7.5:
            Kv_planetBig2 = 3/(3+V_rp_big)
            Kv_ringBig = 3/(3+V_rp_big)
        elif V_rp_big > 7.5 and V_rp_big <= 12.5:
            Kv_planetBig2 = 4.5/(4.5 + V_rp_big)
            Kv_ringBig = 4.5/(4.5 + V_rp_big)

        if V_rp_small <= 7.5:
            Kv_planetSmall = 3/(3+V_rp_small)
            Kv_ringSmall = 3/(3+V_rp_small)
        elif V_rp_small > 7.5 and V_rp_small <= 12.5:
            Kv_planetSmall = 4.5/(4.5 + V_rp_small)
            Kv_ringSmall = 4.5/(4.5 + V_rp_small)
        
        P_big   = np.pi*moduleBig*0.001 # m
        P_small = np.pi*moduleSmall*0.001 # m

        # # Print
        # print("V_sp_big:", V_sp_big)
        # print("V_rp_big:", V_rp_big)
        # print("V_rp_small:", V_rp_small)

        # Lewis static load capacity
        bMin_sun         = (self.FOS * np.abs(Ft_sp_big   )/ (self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * ySun * Kv_sun * P_big)) # m
        bMin_planetBig1  = (self.FOS * np.abs(Ft_sp_big   )/ (self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * yPlanetBig * Kv_planetBig1 * P_big))
        bMin_planetBig2  = (self.FOS * np.abs(Ft_sp_big   )/ (self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * yPlanetBig * Kv_planetBig2 * P_big))
        bMin_planetSmall = (self.FOS * np.abs(Ft_rp_small )/ (self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * yPlanetSmall * Kv_planetSmall * P_small))
        bMin_ringBig     = (self.FOS * np.abs(Ft_rp_big   )/ (self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * yRingBig * Kv_ringBig * P_big))
        bMin_ringSmall   = (self.FOS * np.abs(Ft_rp_small )/ (self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * yRingSmall * Kv_ringSmall * P_small))

        # Making the width of the bigger planet to be the maximum of the two
        if bMin_planetBig1 > bMin_planetBig2:
            bMin_planetBig = bMin_planetBig1
        else:
            bMin_planetBig = bMin_planetBig2

        # Making the width of ring and planet in the second layer to be same
        if bMin_ringSmall < bMin_planetSmall:
            bMin_ringSmall = bMin_planetSmall
        else:
            bMin_planetSmall = bMin_ringSmall

        # Making the width of ring and planet in the first layer to be same
        if bMin_ringBig < bMin_planetBig:
            bMin_ringBig = bMin_planetBig
        else:
            bMin_planetBig = bMin_ringBig

        self.wolfromPlanetaryGearbox.setfwSunMM         ( bMin_sun*1000 )
        self.wolfromPlanetaryGearbox.setfwPlanetBigMM   ( bMin_planetBig*1000 )
        self.wolfromPlanetaryGearbox.setfwPlanetSmallMM ( bMin_planetSmall*1000 )
        self.wolfromPlanetaryGearbox.setfwRingSmallMM   ( bMin_ringSmall*1000 )
        self.wolfromPlanetaryGearbox.setfwRingBigMM     ( bMin_ringBig*1000 )
        # print("Lewis:")
        # print(f"bMin_planetSmall = {bMin_planetSmall}")
        # print(f"bMin_planetBig = {bMin_planetBig}")
        # print(f"bMin_sun = {bMin_sun}")
        # print(f"bMin_ringSmall = {bMin_ringSmall}")
        # print(f"bMin_ringBig = {bMin_ringBig}")

    def AGMAStressAnalysisMinFacewidth(self):
        # Check if the constraints are satisfied
        if not self.wolfromPlanetaryGearbox.geometricConstraint():
            print("Geometric constraint not satisfied")
            return
        if not self.wolfromPlanetaryGearbox.meshingConstraint():
            print("Meshing constraint not satisfied")
            return
        if not self.wolfromPlanetaryGearbox.noPlanetInterferenceConstraint():
            print("No planet interference constraint not satisfied")
            return

        Ns          = self.wolfromPlanetaryGearbox.Ns
        NpBig       = self.wolfromPlanetaryGearbox.NpBig
        NpSmall     = self.wolfromPlanetaryGearbox.NpSmall
        NrBig       = self.wolfromPlanetaryGearbox.NrBig
        NrSmall     = self.wolfromPlanetaryGearbox.NrSmall
        numPlanet   = self.wolfromPlanetaryGearbox.numPlanet
        moduleBig   = self.wolfromPlanetaryGearbox.moduleBig
        moduleSmall = self.wolfromPlanetaryGearbox.moduleSmall

        RpBig = NpBig * moduleBig / 2
        RpSmall = NpSmall * moduleSmall / 2
        Rs = Ns * moduleBig / 2
        RrBig = NrBig * moduleBig / 2
        RrSmall = NrSmall * moduleSmall / 2

        wSun       = self.motor.getMaxMotorAngVelRadPerSec()
        wPlanet    = (-Ns / (2*NpBig) ) * wSun
        wCarrier   = (Ns / (Ns + NrBig)) * wSun
        wRingSmall = (Ns * (NpBig - NpSmall) / (2 * NrSmall * NpBig)) * wSun

        [Wt_sp_big, Wt_rp_big, Wt_rp_small]  = self.getToothForces(False)

        pressureAngle = self.wolfromPlanetaryGearbox.pressureAngleDEG

        # T Krishna Rao - Design of Machine Elements - II pg.191
        # Modified Lewis Form Factor Y = pi*y for pressure angle = 20
        Y_sun         = (0.154 - 0.912/Ns) * np.pi
        Y_planetBig   = (0.154 - 0.912/NpBig) * np.pi
        Y_planetSmall = (0.154 - 0.912/NpSmall) * np.pi
        Y_ringSmall   = (0.154 - 0.912/NrSmall) * np.pi
        Y_ringBig     = (0.154 - 0.912/NrBig) * np.pi

        V_sp_big = np.abs(self.wolfromPlanetaryGearbox.getPCRadiusSunM() * wSun)
        V_rp_big = np.abs(wCarrier*(self.wolfromPlanetaryGearbox.getPCRadiusSunM() + self.wolfromPlanetaryGearbox.getPCRadiusPlanetBigM()) + 
                    wPlanet*(self.wolfromPlanetaryGearbox.getPCRadiusPlanetBigM()))
        V_rp_small = np.abs(wCarrier*(self.wolfromPlanetaryGearbox.getPCRadiusSunM() + self.wolfromPlanetaryGearbox.getPCRadiusPlanetBigM()) +
                      wPlanet*(self.wolfromPlanetaryGearbox.getPCRadiusPlanetSmallM()))
        
        # Check 
        V_rp_small_test = wRingSmall*(self.wolfromPlanetaryGearbox.getPCRadiusSunM() + self.wolfromPlanetaryGearbox.getPCRadiusPlanetBigM()
                                      + self.wolfromPlanetaryGearbox.getPCRadiusPlanetSmallM())
        
        if np.abs(V_rp_small - V_rp_small_test) > 1e-6:
            print("----------------------------------------------")
            print("                   ERROR                      ")
            print("----------------------------------------------")
            print("V_rp_small not equal to V_rp_small_test")
            print("V_rp_small:", V_rp_small)
            print("V_rp_small_test:", V_rp_small_test)

        # AGMA 908-B89 pg.16
        # Kf Fatigue stress concentration factor
        H = 0.331 - (0.436 * np.pi * pressureAngle / 180)
        L = 0.324 - (0.492 * np.pi * pressureAngle / 180)
        M = 0.261 + (0.545 * np.pi * pressureAngle / 180) 
        # t -> tooth thickness, r -> fillet radius and l -> tooth height
        t_planetSmall = (13.5 * Y_planetSmall)**(1/2) * moduleSmall
        r_planetSmall = 0.3 * moduleSmall 
        l_planetSmall = 2.25 * moduleSmall
        Kf_planetSmall = H + (t_planetSmall / r_planetSmall)**(L) * (t_planetSmall / l_planetSmall)**(M)

        t_planetBig = (13.5 * Y_planetBig)**(1/2) * moduleBig
        r_planetBig = 0.3 * moduleBig 
        l_planetBig = 2.25 * moduleBig
        Kf_planetBig = H + (t_planetBig / r_planetBig)**(L) * (t_planetBig / l_planetBig)**(M)

        t_sun = (13.5 * Y_sun)**(1/2) * moduleBig
        r_sun = 0.3 * moduleBig 
        l_sun = 2.25 * moduleBig
        Kf_sun = H + (t_sun / r_sun)**(L) * (t_sun / l_sun)**(M)

        t_ringSmall = (13.5 * Y_ringSmall)**(1/2) * moduleSmall
        r_ringSmall = 0.3 * moduleSmall 
        l_ringSmall = 2.25 * moduleSmall
        Kf_ringSmall = H + (t_ringSmall / r_ringSmall)**(L) * (t_ringSmall / l_ringSmall)**(M)

        t_ringBig = (13.5 * Y_ringBig)**(1/2) * moduleBig
        r_ringBig = 0.3 * moduleBig
        l_ringBig = 2.25 * moduleBig
        Kf_ringBig = H + (t_ringBig / r_ringBig)**(L) * (t_ringBig / l_ringBig)**(M)

        # Shigley's Mechanical Engineering Design 9th Edition pg.752
        # Yj Geometry factor
        Yj_planetSmall = Y_planetSmall/Kf_planetSmall
        Yj_planetBig = Y_planetBig/Kf_planetBig
        Yj_sun = Y_sun/Kf_sun
        Yj_ringSmall = Y_ringSmall/Kf_ringSmall
        Yj_ringBig = Y_ringBig/Kf_ringBig 
        
        # Kv Dynamic factor
        # Shigley's Mechanical Engineering Design 9th Edition pg.756
        Qv = 7      # Quality numbers 3 to 7 will include most commercial-quality gears.
        B_planetSmall =  0.25*(12-Qv)**(2/3)
        A_planetSmall = 50 + 56*(1-B_planetSmall)
        Kv_planetSmall = ((A_planetSmall+np.sqrt(200*V_rp_small))/A_planetSmall)**B_planetSmall

        B_planetBig =  0.25*(12-Qv)**(2/3)
        A_planetBig = 50 + 56*(1-B_planetBig)
        Kv_planetBig = ((A_planetBig+np.sqrt(200*max(V_sp_big, V_rp_big)))/A_planetBig)**B_planetBig

        B_sun =  0.25*(12-Qv)**(2/3)
        A_sun = 50 + 56*(1-B_sun)
        Kv_sun = ((A_sun+np.sqrt(200*V_sp_big))/A_sun)**B_sun

        B_ringSmall =  0.25*(12-Qv)**(2/3)
        A_ringSmall = 50 + 56*(1-B_ringSmall)
        Kv_ringSmall = ((A_ringSmall+np.sqrt(200*V_rp_small))/A_ringSmall)**B_planetSmall

        B_ringBig =  0.25*(12-Qv)**(2/3)
        A_ringBig = 50 + 56*(1-B_ringBig)
        Kv_ringBig = ((A_ringBig+np.sqrt(200*V_rp_big))/A_ringBig)**B_planetBig

        # Shigley's Mechanical Engineering Design 9th Edition pg.764
        # Ks Size factor (can be omitted if enough information is not available)
        Ks = 1

        # NPTEL Fatigue Consideration in Design lecture-7 pg.10 Table-7.4 (https://archive.nptel.ac.in/courses/112/106/112106137/)
        # Kh Load-distribution factor (0-50mm, less rigid mountings, less accurate gears)
        Kh = 1.3

        # Shigley's Mechanical Engineering Design 9th Edition pg.764
        # Kb Rim-thickness factor (the gears have a uniform thickness)
        Kb = 1
        
        # AGMA bending stress equation (Shigley's Mechanical Engineering Design 9th Edition pg.746)  
        bMin_planetSmall = (self.FOS * np.abs(Wt_rp_small) * Kv_planetSmall * Ks * Kh * Kb)/(moduleSmall * Yj_planetSmall * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        bMin_planetBig = (self.FOS * np.abs(Wt_rp_big) * Kv_planetBig * Ks * Kh * Kb)/(moduleBig * Yj_planetBig * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        bMin_sun = (self.FOS * np.abs(Wt_sp_big) * Kv_sun * Ks * Kh * Kb) / (moduleBig * Yj_sun * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        bMin_ringSmall = (self.FOS * np.abs(Wt_rp_small) * Kv_ringSmall * Ks * Kh * Kb) / (moduleSmall * Yj_ringSmall * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        bMin_ringBig = (self.FOS * np.abs(Wt_rp_big) * Kv_ringBig * Ks * Kh * Kb) / (moduleBig * Yj_ringBig * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)

        # C_pm = 1.1
        # X_planetSmall = (self.FOS * np.abs(Wt_rp_small) * Kv_planetSmall * Ks * Kb)/(moduleSmall * Y_planetSmall * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        # X_planetBig = (self.FOS * np.abs(Wt_rp_big) * Kv_planetBig * Ks * Kb)/(moduleBig * Y_planetBig * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        # X_sun = (self.FOS * np.abs(Wt_sp_big) * Kv_sun * Ks * Kb) / (moduleBig * Y_sun * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        # X_ringSmall = (self.FOS * np.abs(Wt_rp_small) * Kv_ringSmall * Ks * Kb) / (moduleSmall * Y_ringSmall * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)
        # X_ringBig = (self.FOS * np.abs(Wt_rp_big) * Kv_ringBig * Ks * Kb) / (moduleBig * Y_ringBig * self.wolfromPlanetaryGearbox.maxGearAllowableStressPa * 0.001)

        # co_eff_of_fwSqr = 0.93/10000
        # co_eff_of_fw_planetSmall = -(C_pm/(moduleSmall*NpSmall*10*0.03937)) + 1/(39.37*X_planetSmall) - 0.0158
        # co_eff_of_fw_planetBig = -(C_pm/(moduleBig*NpBig*10*0.03937)) + 1/(39.37*X_planetBig) - 0.0158
        # co_eff_of_fw_sun = -(C_pm/(moduleBig*Ns*10*0.03937)) + 1/(39.37*X_sun) - 0.0158
        # co_eff_of_fw_ringSmall = -(C_pm/(moduleSmall*NrSmall*10*0.03937)) + 1/(39.37*X_ringSmall) - 0.0158
        # co_eff_of_fw_ringBig = -(C_pm/(moduleBig*NrBig*10*0.03937)) + 1/(39.37*X_ringBig) - 0.0158
        # constant = -1.0995

        # bMin_planetSmall = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_planetSmall, constant]))/39.37
        # bMin_planetBig = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_planetBig, constant]))/39.37
        # bMin_sun = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_sun, constant]))/39.37
        # bMin_ringSmall = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_ringSmall, constant]))/39.37
        # bMin_ringBig = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_ringBig, constant]))/39.37

        # if bMin_planetSmall > 0.026:
        #     co_eff_of_fw_planetSmall = -(C_pm/(moduleSmall*NpSmall*10*0.03937)) + 1/(39.37*X_planetSmall) - 0.1533
        #     constant = -1.08575
        #     bMin_planetSmall = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_planetSmall, constant]))/39.37

        # if bMin_planetBig > 0.026:
        #     co_eff_of_fw_planetBig = -(C_pm/(moduleBig*NpBig*10*0.03937)) + 1/(39.37*X_planetBig) - 0.1533
        #     constant = -1.08575
        #     bMin_planetBig = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_planetBig, constant]))/39.37

        # if bMin_ringSmall > 0.026:
        #     co_eff_of_fw_ringSmall = -(C_pm/(moduleSmall*NrSmall*10*0.03937)) + 1/(39.37*X_ringSmall) - 0.1533
        #     constant = -1.08575
        #     bMin_ringSmall = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_ringSmall, constant]))/39.37

        # if bMin_ringBig > 0.026:
        #     co_eff_of_fw_ringBig = -(C_pm/(moduleBig*NrBig*10*0.03937)) + 1/(39.37*X_ringBig) - 0.1533
        #     constant = -1.08575
        #     bMin_ringBig = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_ringBig, constant]))/39.37

        # if bMin_sun > 0.026:
        #     co_eff_of_fw_sun = -(C_pm/(moduleBig*Ns*10*0.03937)) + 1/(39.37*X_sun) - 0.1533
        #     constant = -1.08575
        #     bMin_sun = max(np.roots([co_eff_of_fwSqr, co_eff_of_fw_sun, constant]))/39.37

        # Making the width of ring and planet in the second layer to be same
        if bMin_ringSmall < bMin_planetSmall:
            bMin_ringSmall = bMin_planetSmall
        else:
            bMin_planetSmall = bMin_ringSmall

        # Making the width of ring and planet in the first layer to be same
        if bMin_ringBig < bMin_planetBig:
            bMin_ringBig = bMin_planetBig
        else:
            bMin_planetBig = bMin_ringBig

        self.wolfromPlanetaryGearbox.setfwSunMM         ( bMin_sun*1000 )
        self.wolfromPlanetaryGearbox.setfwPlanetBigMM   ( bMin_planetBig*1000 )
        self.wolfromPlanetaryGearbox.setfwPlanetSmallMM ( bMin_planetSmall*1000 )
        self.wolfromPlanetaryGearbox.setfwRingSmallMM   ( bMin_ringSmall*1000 )
        self.wolfromPlanetaryGearbox.setfwRingBigMM     ( bMin_ringBig*1000 )

        # print("AGMA:")
        # print(f"bMin_planetSmall = {bMin_planetSmall}")
        # print(f"bMin_planetBig = {bMin_planetBig}")
        # print(f"bMin_sun = {bMin_sun}")
        # print(f"bMin_ringSmall = {bMin_ringSmall}")
        # print(f"bMin_ringBig = {bMin_ringBig}")

    def mitStressAnalysisMinFacewidth(self):
        # Check if the constraints are satisfied
        if not self.bipathwolfromPlanetaryGearbox.geometricConstraint():
            print("Geometric constraint not satisfied")
            return
        if not self.bipathwolfromPlanetaryGearbox.meshingConstraint():
            print("Meshing constraint not satisfied")
            return
        if not self.bipathwolfromPlanetaryGearbox.noPlanetInterferenceConstraint():
            print("No planet interference constraint not satisfied")
            return

        Ns          = self.bipathwolfromPlanetaryGearbox.Ns
        NpBig       = self.bipathwolfromPlanetaryGearbox.NpBig
        NpSmall     = self.bipathwolfromPlanetaryGearbox.NpSmall
        NrBig       = self.bipathwolfromPlanetaryGearbox.NrBig
        NrSmall     = self.bipathwolfromPlanetaryGearbox.NrSmall
        numPlanet   = self.bipathwolfromPlanetaryGearbox.numPlanet
        moduleBig   = self.bipathwolfromPlanetaryGearbox.moduleBig
        moduleSmall = self.bipathwolfromPlanetaryGearbox.moduleSmall

        RpBig = NpBig * moduleBig / 2
        RpSmall = NpSmall * moduleSmall / 2
        Rs = Ns * moduleBig / 2
        RrBig = NrBig * moduleBig / 2
        RrSmall = NrSmall * moduleSmall / 2

        wSun       = self.motor.getMaxMotorAngVelRadPerSec()
        wPlanet    = (-Ns / (2*NpBig) ) * wSun
        wCarrier   = (Ns / (Ns + NrBig)) * wSun
        wRingSmall = (Ns * (NpBig - NpSmall) / (2 * NrSmall * NpBig)) * wSun

        [Ft_sp_big, Ft_rp_big, Ft_rp_small]  = self.getToothForces(False)

        # Lewis static load capacity
        _,_,CR_SP1 = self.bipathwolfromPlanetaryGearbox.contactRatio_sunPlanet_stg1()
        _,_,CR_PR1 = self.bipathwolfromPlanetaryGearbox.contactRatio_planetRing_stg1()
        _,_,CR_PR2 = self.bipathwolfromPlanetaryGearbox.contactRatio_planetRing_stg2()

        qe_sp1 = 1 / CR_SP1
        qe_pr1 = 1 / CR_PR1
        qe_pr2 = 1 / CR_PR2

        qk_sp1 = (7.65734266e-08 * Ns**4
                - 2.19500130e-05 * Ns**3
                + 2.33893357e-03 * Ns**2
                - 1.13320908e-01 * Ns
                + 4.44727778)
        qk_pr1 = (7.65734266e-08 * NpBig**4
                - 2.19500130e-05 * NpBig**3
                + 2.33893357e-03 * NpBig**2
                - 1.13320908e-01 * NpBig
                + 4.44727778)
        qk_pr2 = (7.65734266e-08 * NpSmall**4
                - 2.19500130e-05 * NpSmall**3
                + 2.33893357e-03 * NpSmall**2
                - 1.13320908e-01 * NpSmall
                + 4.44727778)

        # Lewis static load capacity
        bMin_sun_mit           = (self.FOS * np.abs(Ft_sp_big  ) * qe_sp1 * qk_sp1 / (self.bipathwolfromPlanetaryGearbox.maxGearAllowableStressPa * moduleBig   * 0.001))
        bMin_planetBig_mit_1   = (self.FOS * np.abs(Ft_sp_big  ) * qe_sp1 * qk_sp1 / (self.bipathwolfromPlanetaryGearbox.maxGearAllowableStressPa * moduleBig   * 0.001))
        bMin_planetBig_mit_2   = (self.FOS * np.abs(Ft_rp_big  ) * qe_pr1 * qk_pr1 / (self.bipathwolfromPlanetaryGearbox.maxGearAllowableStressPa * moduleBig   * 0.001))
        bMin_planetSmall_mit   = (self.FOS * np.abs(Ft_rp_small) * qe_pr2 * qk_pr2 / (self.bipathwolfromPlanetaryGearbox.maxGearAllowableStressPa * moduleSmall * 0.001))
        bMin_ringBig_mit       = (self.FOS * np.abs(Ft_rp_big  ) * qe_pr1 * qk_pr1 / (self.bipathwolfromPlanetaryGearbox.maxGearAllowableStressPa * moduleBig   * 0.001))
        bMin_ringSmall_mit     = (self.FOS * np.abs(Ft_rp_small) * qe_pr2 * qk_pr2 / (self.bipathwolfromPlanetaryGearbox.maxGearAllowableStressPa * moduleSmall * 0.001))

        if (bMin_planetBig_mit_1 > bMin_planetBig_mit_2):
            bMin_planetBig_mit = bMin_planetBig_mit_1
        else:
            bMin_planetBig_mit = bMin_planetBig_mit_2

        #------------- Contraint in planet to accomodate its bearings------------------------------------------
        if ((bMin_planetBig_mit + bMin_planetSmall_mit) * 1000 < (self.planet_bearing_width*2 + self.standard_clearance_1_5mm * 2 / 3)) : 
            if ((bMin_planetBig_mit) * 1000 < (self.planet_bearing_width + self.standard_clearance_1_5mm * 1 / 3)): 
                bMin_planetBig_mit = (self.planet_bearing_width + self.standard_clearance_1_5mm * 1 / 3) / 1000
            if ((bMin_planetSmall_mit) * 1000 < (self.planet_bearing_width + self.standard_clearance_1_5mm * 1 / 3)): 
                bMin_planetSmall_mit = (self.planet_bearing_width + self.standard_clearance_1_5mm * 1 / 3) / 1000
            bMin_ringBig_mit   = bMin_planetBig_mit
            bMin_ringSmall_mit = bMin_planetSmall_mit

        bMin_sun_mitMM         = bMin_sun_mit * 1000
        bMin_planetBig_mitMM   = bMin_planetBig_mit * 1000
        bMin_planetSmall_mitMM = bMin_planetSmall_mit * 1000
        bMin_ringBig_mitMM     = bMin_ringBig_mit * 1000
        bMin_ringSmall_mitMM   = bMin_ringSmall_mit * 1000

        self.bipathwolfromPlanetaryGearbox.setfwSunMM         ( bMin_sun_mit         * 1000 )
        self.bipathwolfromPlanetaryGearbox.setfwPlanetBigMM   ( bMin_planetBig_mit   * 1000 )
        self.bipathwolfromPlanetaryGearbox.setfwPlanetSmallMM ( bMin_planetSmall_mit * 1000 )
        self.bipathwolfromPlanetaryGearbox.setfwRingSmallMM   ( bMin_ringSmall_mit   * 1000 )
        self.bipathwolfromPlanetaryGearbox.setfwRingBigMM     ( bMin_ringBig_mit     * 1000 )
        # FIXME : Newly added content
        Ns2 = self.bipathwolfromPlanetaryGearbox.getFloatingSunTeeth()
        if Ns2 > 0:
            qk_fs = (7.65734266e-08*Ns2**4 - 2.19500130e-05*Ns2**3 + 2.33893357e-03*Ns2**2
                     - 1.13320908e-01*Ns2 + 4.44727778)
            bMin_fs_mm = (self.FOS*np.abs(Ft_rp_small)*qe_pr2*qk_fs
                          / (self.bipathwolfromPlanetaryGearbox.maxGearAllowableStressPa*moduleSmall*0.001)) * 1000
            self.bipathwolfromPlanetaryGearbox.setfwFloatingSunMM(max(bMin_planetSmall_mitMM, bMin_fs_mm))

        return bMin_sun_mitMM, bMin_planetBig_mitMM, bMin_planetSmall_mitMM, bMin_ringBig_mitMM, bMin_ringSmall_mitMM

    def updateFacewidth(self):
        if self.stressAnalysisMethodName == "Lewis":
            self.lewisStressAnalysisMinFacewidth()
        elif self.stressAnalysisMethodName == "AGMA":
            self.AGMAStressAnalysisMinFacewidth()
        elif self.stressAnalysisMethodName == "MIT":
            self.mitStressAnalysisMinFacewidth()

    def getMassKG_3DP(self):
        module1   = self.bipathwolfromPlanetaryGearbox.moduleBig
        module2   = self.bipathwolfromPlanetaryGearbox.moduleSmall
        Ns        = self.bipathwolfromPlanetaryGearbox.Ns
        Np1       = self.bipathwolfromPlanetaryGearbox.NpBig
        Nr1       = self.bipathwolfromPlanetaryGearbox.NrBig
        Np2       = self.bipathwolfromPlanetaryGearbox.NpSmall
        Nr2       = self.bipathwolfromPlanetaryGearbox.NrSmall
        numPlanet = self.bipathwolfromPlanetaryGearbox.numPlanet 

        #----------------------------------
        # Density of Materials
        #----------------------------------
        density_3DP_material = self.bipathwolfromPlanetaryGearbox.densityGears

        #----------------------------------
        # Diameter and Radius
        #----------------------------------
        DiaSunMM     =  Ns * module1
        DiaPlanet1MM = Np1 * module1
        DiaRing1MM   = Nr1 * module1
        DiaPlanet2MM = Np2 * module2
        DiaRing2MM   = Nr2 * module2

        Rs_MM  = DiaSunMM / 2
        Rp1_MM = DiaPlanet1MM / 2
        Rp2_MM = DiaPlanet2MM / 2
        Rr1_MM = DiaRing1MM / 2
        Rr2_MM = DiaRing2MM / 2
        
        Ring1OuterRadiusMM = Rr1_MM + self.ring1RadialWidthMM
        Ring2OuterRadiusMM = Rr2_MM + self.ring2RadialWidthMM

        ring1_radial_thickness = self.ring1RadialWidthMM
        ring2_radial_thickness = self.ring2RadialWidthMM

        #----------------------------------
        # Facewidths
        #----------------------------------         
        sunFwMM     = self.bipathwolfromPlanetaryGearbox.fwSunMM
        planet1FwMM = self.bipathwolfromPlanetaryGearbox.fwPlanetBigMM
        planet2FwMM = self.bipathwolfromPlanetaryGearbox.fwPlanetSmallMM
        ring1FwMM   = self.bipathwolfromPlanetaryGearbox.fwRingBigMM
        ring2FwMM   = self.bipathwolfromPlanetaryGearbox.fwRingSmallMM

        sunFwM     = sunFwMM     * 0.001 
        planet1FwM = planet1FwMM * 0.001
        planet2FwM = planet2FwMM * 0.001
        ring1FwM   = ring1FwMM   * 0.001
        ring2FwM   = ring2FwMM   * 0.001

        #-----------------------------------------
        # Motor Dimensions & Mass
        #-----------------------------------------
        MotorLengthMM = self.motorLengthMM
        MotorDiaMM    = self.motorDiaMM
        MotorMassKG   = self.motorMassKG

        #--------------------------------------
        # Independent variables
        #--------------------------------------
        # To be written in Gearbox(dspg) JSON files
        case_mounting_surface_height = self.case_mounting_surface_height
        standard_clearance_1_5mm     = self.standard_clearance_1_5mm    
        base_plate_thickness         = self.base_plate_thickness        
        Motor_case_thickness         = self.Motor_case_thickness        
        clearance_planet             = self.clearance_planet            
        output_mounting_hole_dia     = self.output_mounting_hole_dia    
        sec_carrier_thickness        = self.sec_carrier_thickness       
        sun_coupler_hub_thickness    = self.sun_coupler_hub_thickness   
        # sun_shaft_bearing_OD       = self.sun_shaft_bearing_OD        
        # carrier_bearing_step_width = self.carrier_bearing_step_width  
        planet_shaft_dia             = self.planet_shaft_dia            
        sun_shaft_bearing_ID         = self.sun_shaft_bearing_ID        
        sun_shaft_bearing_width      = self.sun_shaft_bearing_width     
        planet_bore                  = self.planet_bore                 
        # bearing_retainer_thickness = self.bearing_retainer_thickness 
        carrier_small_ring_inner_bearing_flap = self.carrier_small_ring_inner_bearing_flap # 2
        carrier_small_ring_inner_bearing_ID   = self.carrier_small_ring_inner_bearing_ID # 20
        gear_casing_big_ring_to_bearing_dist  = self.gear_casing_big_ring_to_bearing_dist
        Motor_case_OD_base_to_chamfer = self.Motor_case_OD_base_to_chamfer # 5
        planet_pin_socket_head_dia    = self.planet_pin_socket_head_dia
        carrier_thickness             = self.carrier_thickness # 4
        small_ring_output_wall_thickness = self.small_ring_output_wall_thickness # 5
        gearbox_casing_thickness         = self.gearbox_casing_thickness # 4
        small_ring_gear_casing_thickness = self.small_ring_gear_casing_thickness # 4
        bearingIDClearanceMM             = self.bearingIDClearanceMM

        # To be written in Motor JSON files
        motor_output_hole_PCD = self.motor.motor_output_hole_PCD
        motor_output_hole_dia = self.motor.motor_output_hole_dia

        #-------------------------------
        # Bearings: Bearing1 & Bearing2
        #-------------------------------
        IdRequiredMM      = module1 * (Ns + Np1) + bearingIDClearanceMM 
                                                                               
        Bearing           = bearings_discrete(IdRequiredMM)

        InnerDiaBearingMM = Bearing.getBearingIDMM()
        OuterDiaBearingMM = Bearing.getBearingODMM()
        WidthBearingMM    = Bearing.getBearingWidthMM()
        BearingMassKG     = Bearing.getBearingMassKG()

        # --- Bearing dimensions --- 
        bearing_ID     = InnerDiaBearingMM 
        bearing_OD     = OuterDiaBearingMM 
        bearing_height = WidthBearingMM 

        #-------------------------------------------------------
        # wpg_bearing
        #-------------------------------------------------------   
        bearing_mass   = BearingMassKG 

        #-------------------------------------------------------
        # wpg_carrier_ring_small_bearing
        #-------------------------------------------------------
        carrier_small_ring_inner_bearing = bearings_discrete(carrier_small_ring_inner_bearing_ID)
        carrier_small_ring_inner_bearing_OD = carrier_small_ring_inner_bearing.getBearingODMM()
        carrier_small_ring_inner_bearing_height = carrier_small_ring_inner_bearing.getBearingWidthMM()

        carrier_small_ring_inner_bearing_mass = carrier_small_ring_inner_bearing.getBearingMassKG()

        #-------------------------------------------------------
        # wpg_carrier
        #-------------------------------------------------------
        carrier_OD     = ((Ns + Np1) * module1 + planet_pin_socket_head_dia + standard_clearance_1_5mm * 2)
        carrier_ID     = carrier_small_ring_inner_bearing_OD
        carrier_height = carrier_thickness

        carrier_bearing_mount_ID     = carrier_small_ring_inner_bearing_OD
        carrier_bearing_mount_OD     = standard_clearance_1_5mm * (8/3) + carrier_small_ring_inner_bearing_OD
        carrier_bearing_mount_height = carrier_small_ring_inner_bearing_height - carrier_thickness + standard_clearance_1_5mm

        carrier_shaft_OD     = planet_shaft_dia
        carrier_shaft_height = planet1FwMM  + planet2FwMM + clearance_planet * 2
        carrier_shaft_num    = numPlanet * 2 + numPlanet # assuming support triangle weighs twice as much as shaft

        carrier_volume = (np.pi * (((carrier_OD*0.5)**2) - ((carrier_ID)*0.5)**2) * carrier_height
                        + np.pi * (((carrier_bearing_mount_OD*0.5)**2) - ((carrier_bearing_mount_ID)*0.5)**2) * carrier_bearing_mount_height  
                        + np.pi * ((carrier_shaft_OD*0.5)**2) * carrier_shaft_height * carrier_shaft_num) * 1e-9

        carrier_mass = carrier_volume * density_3DP_material

        #-------------------------------------------------------
        # wpg_motor_casing
        #-------------------------------------------------------
        ring1_OD  = Nr1 * module1 + ring1_radial_thickness*2
        motor_OD = self.motorDiaMM

        if (ring1_OD < motor_OD):
            clearance_motor_and_case = 5
        else: 
            clearance_motor_and_case = (ring1_OD - motor_OD)/2 + 5

        motor_height      = self.motorLengthMM
        Motor_case_height = motor_height + case_mounting_surface_height + standard_clearance_1_5mm

        Motor_case_ID     = motor_OD + clearance_motor_and_case * 2
        Motor_case_OD = Motor_case_ID + Motor_case_thickness * 2

        Motor_case_volume = ( np.pi * ((Motor_case_OD * 0.5)**2) * base_plate_thickness 
                            + np.pi * ((Motor_case_OD * 0.5)**2 - (Motor_case_ID * 0.5)**2) * Motor_case_height) * 1e-9

        Motor_case_mass = Motor_case_volume * density_3DP_material

        #-------------------------------------------------------
        # wpg_gearbox_casing
        # ---
        # Mass of the gearbox casign includes the mass of:
        # 1. Bearing holding structure
        # 2. Spacer wall for ring-2
        # 3. Ring gear-1
        # 4. Case mounting structure
        #-------------------------------------------------------
        ring1_ID     = Nr1 * module2
        ringFwUsedMM = ring1FwMM

        # --- Bearing holding structure --- 
        if ((bearing_OD + output_mounting_hole_dia * 4) > ((Nr2 * module2 + 2 * ring2_radial_thickness) + standard_clearance_1_5mm * 2)):
            bearing_mount_thickness  = output_mounting_hole_dia * 2
        else:
            bearing_mount_thickness = (((
                                        ((Nr2 * module2 + 2 * ring2_radial_thickness) + standard_clearance_1_5mm * 2) 
                                        - (bearing_OD + output_mounting_hole_dia * 4))/2) 
                                        + output_mounting_hole_dia * 2 + standard_clearance_1_5mm)        

        bearing_holding_structure_ID     = bearing_OD
        bearing_holding_structure_OD     = bearing_OD + bearing_mount_thickness * 2
        bearing_holding_structure_height = bearing_height + standard_clearance_1_5mm

        bearing_holding_structure_volume = np.pi * (((bearing_holding_structure_OD*0.5)**2) - 
                                                    ((bearing_holding_structure_ID*0.5)**2)) * bearing_holding_structure_height * 1e-9
        # --- Spacer wall for ring-2 --- 
        spacer_wall_for_ring2_ID     = ((Nr2 * module2 + 2 * ring2_radial_thickness) + standard_clearance_1_5mm * 2)
        spacer_wall_for_ring2_OD     = spacer_wall_for_ring2_ID + gearbox_casing_thickness * 2
        spacer_wall_for_ring2_height = gear_casing_big_ring_to_bearing_dist

        spacer_wall_for_ring2_volume = np.pi * (((spacer_wall_for_ring2_OD*0.5)**2) - 
                                                ((spacer_wall_for_ring2_ID*0.5)**2)) * spacer_wall_for_ring2_height * 1e-9

        # --- Ring gear-1 --- 
        ring_gear1_ID     = (Nr1 * module1)
        ring_gear1_OD     = ring_gear1_ID + ring1_radial_thickness * 2
        ring_gear1_height = ring1FwMM

        ring_gear1_volume = np.pi * (((ring_gear1_OD*0.5)**2) - 
                                     ((ring_gear1_ID*0.5)**2)) * ring_gear1_height * 1e-9

        # --- Case mounting structure --- 
        case_dist = (sec_carrier_thickness 
                     + clearance_planet
                     + sun_coupler_hub_thickness 
                     - case_mounting_surface_height)

        case_mounting_structure_ID     = Motor_case_OD - Motor_case_OD_base_to_chamfer * 2
        case_mounting_structure_OD     = Motor_case_OD
        case_mounting_structure_height = case_dist

        case_mounting_structure_volume  = np.pi * (((case_mounting_structure_OD*0.5)**2) - 
                                                    ((case_mounting_structure_ID*0.5)**2)) * case_mounting_structure_height * 1e-9


        large_fillet_ID     = ring1_OD
        large_fillet_OD     = Motor_case_OD
        large_fillet_height = ring1FwMM/2
        large_fillet_volume = 0.5 * (np.pi * (((large_fillet_OD*0.5)**2) - ((large_fillet_ID)*0.5)**2) * large_fillet_height) * 1e-9


        gearbox_casing_mass = (bearing_holding_structure_volume
                               + spacer_wall_for_ring2_volume
                               + case_mounting_structure_volume 
                               + large_fillet_volume
                               + ring_gear1_volume) * density_3DP_material

        #-------------------------------------------------------
        # wpg_motor
        #-------------------------------------------------------
        motor_mass = self.motorMassKG
        
        #-------------------------------------------------------
        # wpg_planet_bearing
        #-------------------------------------------------------
        planet_bearing_mass          = 1 * 0.001 # kg
        planet_bearing_num           = numPlanet * 2
        planet_bearing_combined_mass = planet_bearing_mass * planet_bearing_num

        #-------------------------------------------------------
        # wpg_planet
        #-------------------------------------------------------
        planet1_volume = (np.pi * ((DiaPlanet1MM*0.5)**2 - (planet_bore*0.5)**2) * planet1FwMM) * 1e-9
        planet2_volume = (np.pi * ((DiaPlanet2MM*0.5)**2 - (planet_bore*0.5)**2) * planet2FwMM) * 1e-9
        planet_mass   = (planet1_volume + planet2_volume) * density_3DP_material

        #-------------------------------------------------------
        # wpg_sec_carrier
        #-------------------------------------------------------
        sec_carrier_OD = ((Ns + Np1) * module1 + planet_shaft_dia + self.planet_shaft_step_offset * 2 + standard_clearance_1_5mm * 2)
        sec_carrier_ID = (DiaSunMM + DiaPlanet1MM) - planet_shaft_dia - 2 * standard_clearance_1_5mm

        sec_carrier_volume = (np.pi * ((sec_carrier_OD*0.5)**2 - (sec_carrier_ID*0.5)**2) * sec_carrier_thickness) * 1e-9
        sec_carrier_mass   = sec_carrier_volume * density_3DP_material

        #-------------------------------------------------------
        # wpg_small_ring_bearing_shaft
        #-------------------------------------------------------
        small_ring_bearing_shaft_dia = carrier_small_ring_inner_bearing_ID
        small_ring_bearing_shaft_height = (bearing_height 
                                         + carrier_thickness
                                         + carrier_small_ring_inner_bearing_flap)
        
        small_ring_bearing_shaft_volume = (np.pi 
                                        * (small_ring_bearing_shaft_dia * 0.5)**2 
                                        *  small_ring_bearing_shaft_height) * 1e-9
        
        small_ring_bearing_shaft_mass = small_ring_bearing_shaft_volume * density_3DP_material

        #-------------------------------------------------------
        # wpg_small_ring
        # ---
        # 1. Ring gear2
        # 2. ring2bearing_spacer_cone_shell
        # 3. ring2bearing_spacer_disc
        # 4. bearing_holding_structure
        # 5. output_wall
        # 6. sun_shaft_bearing_holding_structure
        #-------------------------------------------------------

        # --- Ring gear2 ---
        ring_gear2_ID     = (Nr2 * module2)
        ring_gear2_OD     = ring_gear2_ID + ring2_radial_thickness * 2
        ring_gear2_height = ring2FwMM

        ring_gear2_volume = np.pi * (((ring_gear2_OD*0.5)**2) - 
                                     ((ring_gear2_ID*0.5)**2)) * ring_gear2_height * 1e-9

        # --- ring2bearing_spacer_cone_shell ---
        ring2bearing_spacer_cone_shell_base   = small_ring_gear_casing_thickness
        ring2bearing_spacer_cone_shell_height = carrier_thickness + standard_clearance_1_5mm + clearance_planet
        ring2bearing_spacer_cone_shell_radius = ((ring_gear2_OD + carrier_OD) / 2) /2
        
        ring2bearing_spacer_cone_shell_volume = (2 * np.pi * ring2bearing_spacer_cone_shell_radius
                                                 * ring2bearing_spacer_cone_shell_height
                                                 * ring2bearing_spacer_cone_shell_base) * 1e-9

        # --- ring2bearing_spacer_disc ---
        ring2bearing_spacer_disc_ID     = bearing_ID - 2 * small_ring_gear_casing_thickness
        ring2bearing_spacer_disc_OD     = carrier_OD + small_ring_gear_casing_thickness * 2
        ring2bearing_spacer_disc_height = small_ring_gear_casing_thickness
        
        ring2bearing_spacer_disc_volume = np.pi * (((ring2bearing_spacer_disc_OD*0.5)**2) - 
                                                   ((ring2bearing_spacer_disc_ID*0.5)**2)) * ring2bearing_spacer_disc_height * 1e-9

        # --- bearing_holding_structure ---
        bearing_holding_structure_OD     = bearing_ID
        bearing_holding_structure_ID     = bearing_ID - 2 * small_ring_gear_casing_thickness
        bearing_holding_structure_height = bearing_height + standard_clearance_1_5mm * (2/3)

        bearing_holding_structure_volume = np.pi * (((bearing_holding_structure_OD*0.5)**2) - 
                                                   ((bearing_holding_structure_ID*0.5)**2)) * bearing_holding_structure_height * 1e-9

        # --- output_wall ---
        output_wall_dia    = bearing_ID - 2 * small_ring_gear_casing_thickness
        output_wall_height = small_ring_output_wall_thickness
        output_wall_volume = np.pi * (output_wall_dia / 2)**2 * output_wall_height * 1e-9

        # --- sun_shaft_bearing_holding_structure ---
        # truncated hollow cone Volume = 0.5 * Hollow cylinder volume. 
        # 45deg chamfer (height = width)
        sun_shaft_bearing_holding_structure_ID     = carrier_small_ring_inner_bearing_ID
        sun_shaft_bearing_holding_structure_height = (bearing_height + carrier_thickness - carrier_small_ring_inner_bearing_height)
        sun_shaft_bearing_holding_structure_OD     = (sun_shaft_bearing_holding_structure_ID 
                                                      + sun_shaft_bearing_holding_structure_height * 2)
        
        sun_shaft_bearing_holding_structure_volume = (0.5 
                                                      * np.pi 
                                                      * (((sun_shaft_bearing_holding_structure_OD*0.5)**2) - 
                                                         ((sun_shaft_bearing_holding_structure_ID*0.5)**2)) 
                                                      * sun_shaft_bearing_holding_structure_height * 1e-9)

        small_ring_mass = (ring_gear2_volume 
                         + ring2bearing_spacer_cone_shell_volume 
                         + ring2bearing_spacer_disc_volume
                         + bearing_holding_structure_volume
                         + output_wall_volume
                         + sun_shaft_bearing_holding_structure_volume) * density_3DP_material

        #-------------------------------------------------------
        # wpg_sun_shaft_bearing
        #-------------------------------------------------------
        sun_shaft_bearing_mass       = 1 * 0.001 # kg

        #-------------------------------------------------------
        # wpg_sun
        #-------------------------------------------------------
        sun_hub_dia = motor_output_hole_PCD + motor_output_hole_dia + standard_clearance_1_5mm * 4

        sun_shaft_dia    = sun_shaft_bearing_ID
        sun_shaft_height = sun_shaft_bearing_width + 2 * standard_clearance_1_5mm

        fw_s_used        = (planet1FwMM 
                            + planet2FwMM 
                            + clearance_planet 
                            + sec_carrier_thickness 
                            + 2 * standard_clearance_1_5mm 
                            - carrier_small_ring_inner_bearing_flap)

        sun_hub_volume   = np.pi * ((sun_hub_dia*0.5) ** 2) * sun_coupler_hub_thickness * 1e-9
        sun_gear_volume  = np.pi * ((DiaSunMM * 0.5) ** 2) * fw_s_used * 1e-9
        sun_shaft_volume = np.pi * ((sun_shaft_dia*0.5) ** 2) * sun_shaft_height * 1e-9

        sun_volume       = sun_hub_volume + sun_gear_volume + sun_shaft_volume
        sun_mass         = sun_volume * density_3DP_material

        # FIXME : New content
        Ns2          = self.bipathwolfromPlanetaryGearbox.getFloatingSunTeeth()
        sun_r_plane2 = Rs_MM + (module1 if self.bipathwolfromPlanetaryGearbox.mainSunToothedInPlane2 else -1.25*module1)
        fs_bore_dia  = 2 * (sun_r_plane2 + self.bipathwolfromPlanetaryGearbox.floatingSunBoreClrMM)
        fs_width_mm  = max(planet2FwMM + clearance_planet, self.bipathwolfromPlanetaryGearbox.fwFloatingSunMM)
        floating_sun_mass        = np.pi*((Ns2*module1*0.5)**2 - (fs_bore_dia*0.5)**2)*fs_width_mm*1e-9*density_3DP_material
        idler_mass_total         = planet2_volume * density_3DP_material * numPlanet
        idler_bearing_mass_total = 0.001 * 2 * numPlanet


        Actuator_mass = (carrier_small_ring_inner_bearing_mass + 
                        carrier_mass + 
                        gearbox_casing_mass +
                        bearing_mass +
                        Motor_case_mass + 
                        motor_mass +
                        planet_bearing_combined_mass +
                        planet_mass * numPlanet +
                        sec_carrier_mass +
                        small_ring_bearing_shaft_mass +
                        small_ring_mass +
                        sun_shaft_bearing_mass +
                        sun_mass)

        self.carrier_small_ring_inner_bearing_mass = carrier_small_ring_inner_bearing_mass
        self.carrier_mass                          = carrier_mass
        self.gearbox_casing_mass                   = gearbox_casing_mass
        self.bearing_mass                          = bearing_mass
        self.Motor_case_mass                       = Motor_case_mass
        self.motor_mass                            = motor_mass
        self.planet_bearing_combined_mass          = planet_bearing_combined_mass
        self.planet_mass                           = planet_mass
        self.sec_carrier_mass                      = sec_carrier_mass
        self.small_ring_bearing_shaft_mass         = small_ring_bearing_shaft_mass
        self.small_ring_mass                       = small_ring_mass
        self.sun_shaft_bearing_mass                = sun_shaft_bearing_mass
        self.sun_mass                              = sun_mass

        return Actuator_mass

    def print_mass_of_parts_3DP(self):
        print("carrier_small_ring_inner_bearing_mass :", 1000 * self.carrier_small_ring_inner_bearing_mass)
        print("carrier_mass :", 1000 * self.carrier_mass)                         
        print("gearbox_casing_mass :", 1000 * self.gearbox_casing_mass)            
        print("bearing_mass :", 1000 * self.bearing_mass)      
        print("Motor_case_mass :", 1000 * self.Motor_case_mass)                      
        print("motor_mass :", 1000 * self.motor_mass)                           
        print("planet_bearing_combined_mass :", 1000 * self.planet_bearing_combined_mass)         
        print("planet_mass :", 1000 * self.planet_mass)                          
        print("sec_carrier_mass :", 1000 * self.sec_carrier_mass)                     
        print("small_ring_bearing_shaft_mass :", 1000 * self.small_ring_bearing_shaft_mass)        
        print("small_ring_mass :", 1000 * self.small_ring_mass)                      
        print("sun_shaft_bearing_mass :", 1000 * self.sun_shaft_bearing_mass)               
        print("sun_mass :", 1000 * self.sun_mass)                             




#------------------------------------------------------------
# Class: Optimization of Bipath Wolfrom Planetary Actuator
#------------------------------------------------------------
class optimizationbipathWolfromPlanetaryActuator:
    def __init__(self,
                 design_parameters,
                 gear_standard_parameters,
                 K_Mass                     = 1,
                 K_Eff                      = -2,
                 K_Width                    = 0.2,
                 MODULE_BIG_MIN             = 0.5,
                 MODULE_BIG_MAX             = 1.2,
                 MODULE_SMALL_MIN           = 0.5,
                 MODULE_SMALL_MAX           = 1.2,
                 NUM_PLANET_MIN             = 3,
                 NUM_PLANET_MAX             = 5,
                 NUM_TEETH_SUN_MIN          = 20,
                 NUM_TEETH_PLANET_BIG_MIN   = 20,
                 NUM_TEETH_PLANET_SMALL_MIN = 20,
                 GEAR_RATIO_MIN             = 5,
                 GEAR_RATIO_MAX             = 45,
                 GEAR_RATIO_STEP            = 1.0):
        self.K_Mass                     = K_Mass
        self.K_Eff                      = K_Eff
        self.K_Width                    = K_Width
        self.MODULE_BIG_MIN             = MODULE_BIG_MIN
        self.MODULE_BIG_MAX             = MODULE_BIG_MAX
        self.MODULE_SMALL_MIN           = MODULE_SMALL_MIN
        self.MODULE_SMALL_MAX           = MODULE_SMALL_MAX
        self.NUM_PLANET_MIN             = NUM_PLANET_MIN
        self.NUM_PLANET_MAX             = NUM_PLANET_MAX
        self.NUM_TEETH_SUN_MIN          = NUM_TEETH_SUN_MIN
        self.NUM_TEETH_PLANET_BIG_MIN   = NUM_TEETH_PLANET_BIG_MIN
        self.NUM_TEETH_PLANET_SMALL_MIN = NUM_TEETH_PLANET_SMALL_MIN
        self.GEAR_RATIO_MIN             = GEAR_RATIO_MIN
        self.GEAR_RATIO_MAX             = GEAR_RATIO_MAX
        self.GEAR_RATIO_STEP            = GEAR_RATIO_STEP

        self.Cost                     = 100000
        self.totalGearboxesWithReqGR  = 0
        self.totalFeasibleGearboxes   = 0
        self.cntrIterBeforeCons       = 0
        self.iter                     = 0
        self.gearRatioIter            = self.GEAR_RATIO_MIN
        self.UsePSCasVariable         = 1
        self.design_parameters        = design_parameters
        self.gear_standard_parameters = gear_standard_parameters

        self.gearRatioReq = 0

    def optimizeActuator(self, Actuator = bipathwolfromPlanetaryActuator, UsePSCasVariable = 1, log = 0, csv = 1, printOptParams=1, gearRatioReq = 0):
        startTime = time.time()
        self.UsePSCasVariable = UsePSCasVariable
        self.gearRatioReq = gearRatioReq
        opt_parameters = None
        if UsePSCasVariable == 0:
            opt_parameters = self.optimizeActuatorWithoutPSC(Actuator=Actuator, log=log, csv=csv, printOptParams = printOptParams)
        elif UsePSCasVariable == 1:
            opt_parameters =self.optimizeActuatorWithPSC(Actuator=Actuator, log=log, csv=csv, printOptParams=printOptParams)
        else:
            print("ERROR: \"UsePSCasVariable\" can be either 0 or 1")
        
        # Print the time in the file 
        endTime = time.time()
        totalTime = endTime - startTime
        # print("\n")
        # print("Running Time (sec)")
        # print(totalTime) 

        return totalTime, opt_parameters

    def optimizeActuatorWithoutPSC(self, Actuator = bipathwolfromPlanetaryActuator, log=1, csv=0, printOptParams = 1):
        opt_parameters = None
        if csv and log:
            print("WARNING: Both csv and Log cannot be true")
            print("WARNING: Please set either csv or log to be 0 in \"Optimizer.optimizeActuator(Actuator)\" function")
            print(" ")
            print("ACTION:Making log to be false and csv to be true")
            log = 0
            csv = 1
        elif not csv and not log:
            print("WARNING: Both csv and Log cannot be false")
            print("WARNING: Please set either csv or log to be 1 in \"Optimizer.optimizeActuator(Actuator)\" function")
            print(" ")
            print("ACTION:Making log to be False and csv to be true")
            log = 0
            csv = 1
        
        if csv:
            fileName = f"./results/results_BruteForce_{Actuator.motor.motorName}/WPG_BRUTEFORCE_{Actuator.stressAnalysisMethodName}_{Actuator.motor.motorName}.csv"
        elif log:
            fileName = f"./results/results_BruteForce_{Actuator.motor.motorName}/WPG_BRUTEFORCE_{Actuator.stressAnalysisMethodName}_{Actuator.motor.motorName}_LOG.txt"
            
        with open(fileName, "w") as wolfromLogFile:
            sys.stdout = wolfromLogFile
            if (printOptParams):
                self.printOptimizationParameters(Actuator, log, csv)
                print(" ")
            
            if self.gearRatioReq != 0:
                self.GEAR_RATIO_MIN = self.gearRatioReq - self.GEAR_RATIO_STEP/2
                self.GEAR_RATIO_MAX = self.gearRatioReq + (self.GEAR_RATIO_STEP/2 - 1e-6)

            self.gearRatioIter = self.GEAR_RATIO_MIN
            if log:
                print("*****************************************************************")
                print("FOR MINIMUM GEAR RATIO ", self.gearRatioIter)
                print("*****************************************************************")
                print(" ")
            elif csv:
                # Printing the optimization iterations below
                # print("iter, gearRatio, moduleBig, moduleSmall, Ns, NpBig, NpSmall, NrBig, NrSmall, numPlanet, PSCs, PSCp1, PSCp2, PSCr1, PSCr2,fwSunMM, fwPlanetBigMM, fwPanetSmallMM, fwRingBigMM, fwRingSmallMM,  mass, eff, peakTorque, Cost, torque_density")
                print("iter, gearRatio, moduleBig, moduleSmall, Ns, NpBig, NpSmall, NrBig, NrSmall, numPlanet, fwSunMM, fwPlanetBigMM, fwPanetSmallMM, fwRingBigMM, fwRingSmallMM,  mass, eff, peakTorque, Cost, Torque_Density, Outer_Bearing_mass, Actuator_width")

            while self.gearRatioIter <= self.GEAR_RATIO_MAX:
                opt_done = 0
                self.iter = 0
                self.Cost = 100000
                MinCost = self.Cost

                Actuator.bipathwolfromPlanetaryGearbox.setModuleBig(self.MODULE_BIG_MIN)
                while Actuator.bipathwolfromPlanetaryGearbox.moduleBig <= self.MODULE_BIG_MAX:
                    # Setting Module Small
                    Actuator.bipathwolfromPlanetaryGearbox.setModuleSmall(self.MODULE_SMALL_MIN)
                    while (Actuator.bipathwolfromPlanetaryGearbox.moduleSmall <= self.MODULE_SMALL_MAX):
                        # Setting Ns
                        Actuator.bipathwolfromPlanetaryGearbox.setNs(self.NUM_TEETH_SUN_MIN)
                        while (2*Actuator.bipathwolfromPlanetaryGearbox.getPCRadiusSunM()*1000) <= Actuator.maxGearboxDiameter:
                            # Setting Np Big
                            Actuator.bipathwolfromPlanetaryGearbox.setNpBig(self.NUM_TEETH_PLANET_BIG_MIN)
                            while (2*Actuator.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetBigM()*1000) <= Actuator.maxGearboxDiameter/2:
                                # Setting Np Small
                                Actuator.bipathwolfromPlanetaryGearbox.setNpSmall(self.NUM_TEETH_PLANET_SMALL_MIN)
                                while (2*Actuator.bipathwolfromPlanetaryGearbox.getPCRadiusPlanetSmallM()*1000) <= Actuator.maxGearboxDiameter/2:
                                    # Setting Nr Small
                                    Actuator.bipathwolfromPlanetaryGearbox.setNrSmall(Actuator.bipathwolfromPlanetaryGearbox.NpSmall + 
                                                                                Actuator.bipathwolfromPlanetaryGearbox.NpBig +
                                                                                Actuator.bipathwolfromPlanetaryGearbox.Ns)
                                    # Setting Nr Big
                                    Actuator.bipathwolfromPlanetaryGearbox.setNrBig(2*Actuator.bipathwolfromPlanetaryGearbox.NpBig +
                                                                                Actuator.bipathwolfromPlanetaryGearbox.Ns)
                                    if ((2*Actuator.bipathwolfromPlanetaryGearbox.getPCRadiusRingBigM()*1000) <= Actuator.maxGearboxDiameter):# and Actuator.getIdRequired2MM() <= 100): # and ((2*Actuator.wolfromPlanetaryGearbox.getPCRadiusRingSmallM()*1000) <= maxGearBoxDia):
                                        # TODO: Ask Deepak: What is getIDRequired2MM()? and also tell him to write a more meaningful function name
                                        # Setting number of Planet
                                        Actuator.bipathwolfromPlanetaryGearbox.setNumPlanet(self.NUM_PLANET_MIN)
                                        while Actuator.bipathwolfromPlanetaryGearbox.numPlanet <= self.NUM_PLANET_MAX:
                                            if (Actuator.bipathwolfromPlanetaryGearbox.geometricConstraint() and 
                                                Actuator.bipathwolfromPlanetaryGearbox.meshingConstraint() and 
                                                Actuator.bipathwolfromPlanetaryGearbox.noPlanetInterferenceConstraint()):
                                                self.totalFeasibleGearboxes += 1
                                                # Fiter for the Gear Ratio
                                                if (Actuator.bipathwolfromPlanetaryGearbox.gearRatio() >= self.gearRatioIter and 
                                                    Actuator.bipathwolfromPlanetaryGearbox.gearRatio() <= (self.gearRatioIter + 1)):
                                                    self.totalGearboxesWithReqGR += 1
                                                    
                                                    # Cost Calculation
                                                    Actuator.updateFacewidth()

                                                    self.Cost = self.cost(Actuator=Actuator)
                                                    if self.Cost < MinCost:
                                                        MinCost = self.Cost
                                                        self.iter += 1
                                                        opt_done = 1
                                                        # Actuator.genEquationFile()
                                                        if (self.gearRatioReq == 0):
                                                            Actuator.genEquationFile(motor_name=Actuator.motor.motorName, gearRatioLL=round(self.gearRatioIter, 1), gearRatioUL = (round(self.gearRatioIter + self.GEAR_RATIO_STEP,1)))
                                                        else:
                                                            Actuator.genEquationFile_editCADdirectly()

                                                        opt_parameters = [Actuator.bipathwolfromPlanetaryGearbox.gearRatio(),
                                                                          Actuator.bipathwolfromPlanetaryGearbox.numPlanet,
                                                                          Actuator.bipathwolfromPlanetaryGearbox.Ns,
                                                                          Actuator.bipathwolfromPlanetaryGearbox.NpBig,
                                                                          Actuator.bipathwolfromPlanetaryGearbox.NrBig,
                                                                          Actuator.bipathwolfromPlanetaryGearbox.NpSmall,
                                                                          Actuator.bipathwolfromPlanetaryGearbox.NrSmall,
                                                                          Actuator.bipathwolfromPlanetaryGearbox.moduleBig,
                                                                          Actuator.bipathwolfromPlanetaryGearbox.moduleSmall]
                                                        opt_planetaryGearbox = bipathwolfromPlanetaryGearbox  (design_parameters         = self.design_parameters,
                                                                                                         gear_standard_parameters  = self.gear_standard_parameters,
                                                                                                         Ns                        = Actuator.bipathwolfromPlanetaryGearbox.Ns,
                                                                                                         NpBig                     = Actuator.bipathwolfromPlanetaryGearbox.NpBig,
                                                                                                         NpSmall                   = Actuator.bipathwolfromPlanetaryGearbox.NpSmall,
                                                                                                         NrBig                     = Actuator.bipathwolfromPlanetaryGearbox.NrBig,
                                                                                                         NrSmall                   = Actuator.bipathwolfromPlanetaryGearbox.NrSmall,
                                                                                                         numPlanet                 = Actuator.bipathwolfromPlanetaryGearbox.numPlanet,
                                                                                                         moduleBig                 = Actuator.bipathwolfromPlanetaryGearbox.moduleBig,
                                                                                                         moduleSmall               = Actuator.bipathwolfromPlanetaryGearbox.moduleSmall,
                                                                                                         densityGears              = Actuator.bipathwolfromPlanetaryGearbox.densityGears,
                                                                                                         densityStructure          = Actuator.bipathwolfromPlanetaryGearbox.densityStructure,
                                                                                                         fwSunMM                   = Actuator.bipathwolfromPlanetaryGearbox.fwSunMM,
                                                                                                         fwPlanetBigMM             = Actuator.bipathwolfromPlanetaryGearbox.fwPlanetBigMM,
                                                                                                         fwPlanetSmallMM           = Actuator.bipathwolfromPlanetaryGearbox.fwPlanetSmallMM,
                                                                                                         fwRingBigMM               = Actuator.bipathwolfromPlanetaryGearbox.fwRingBigMM,
                                                                                                         fwRingSmallMM             = Actuator.bipathwolfromPlanetaryGearbox.fwRingSmallMM,
                                                                                                         maxGearAllowableStressMPa = Actuator.bipathwolfromPlanetaryGearbox.maxGearAllowableStressMPa)
                                                        opt_actuator = bipathwolfromPlanetaryActuator(design_parameters        = self.design_parameters,
                                                                                                motor                    = Actuator.motor, 
                                                                                                motor_driver_params      = Actuator.motor_driver_params,
                                                                                                bipathwolfromPlanetaryGearbox  = opt_planetaryGearbox, 
                                                                                                FOS                      = Actuator.FOS, 
                                                                                                serviceFactor            = Actuator.serviceFactor, 
                                                                                                maxGearboxDiameter       = Actuator.maxGearboxDiameter, # mm 
                                                                                                stressAnalysisMethodName = "MIT") # Lewis or AGMA
                                                        
                                                        opt_actuator.updateFacewidth()
                                                        opt_actuator.getMassKG_3DP()
                                            
                                                        # self.printOptimizationResults(Actuator, log, csv)
                                            Actuator.bipathwolfromPlanetaryGearbox.setNumPlanet(Actuator.bipathwolfromPlanetaryGearbox.numPlanet + 1)
                                        # Actuator.wolfromPlanetaryGearbox.setNrBig(Actuator.wolfromPlanetaryGearbox.NrBig + 1)
                                        # Actuator.wolfromPlanetaryGearbox.setNrSmall(Actuator.wolfromPlanetaryGearbox.NrSmall + 1)
                                    Actuator.bipathwolfromPlanetaryGearbox.setNpSmall(Actuator.bipathwolfromPlanetaryGearbox.NpSmall + 1)
                                Actuator.bipathwolfromPlanetaryGearbox.setNpBig(Actuator.bipathwolfromPlanetaryGearbox.NpBig + 1)
                            Actuator.bipathwolfromPlanetaryGearbox.setNs(Actuator.bipathwolfromPlanetaryGearbox.Ns + 1)
                        Actuator.bipathwolfromPlanetaryGearbox.setModuleSmall(Actuator.bipathwolfromPlanetaryGearbox.moduleSmall + 0.100)
                        Actuator.bipathwolfromPlanetaryGearbox.setModuleSmall(round(Actuator.bipathwolfromPlanetaryGearbox.moduleSmall, 1)) # Round Off
                    Actuator.bipathwolfromPlanetaryGearbox.setModuleBig(Actuator.bipathwolfromPlanetaryGearbox.moduleBig + 0.100)
                    Actuator.bipathwolfromPlanetaryGearbox.setModuleBig(round(Actuator.bipathwolfromPlanetaryGearbox.moduleBig, 1)) # Round Off
                if (opt_done == 1):
                    self.printOptimizationResults(opt_actuator, log, csv)  
                self.gearRatioIter += self.GEAR_RATIO_STEP
    
                if log:
                    print("Number of iterations: ", self.iter)
                    print("Total Feasible Gearboxes:", self.totalFeasibleGearboxes)
                    print("Total Gearboxes with requires Gear Ratio:", self.totalGearboxesWithReqGR)
                    print("*****************************************************************")
                    print("----------------------------END----------------------------------")
                    print(" ")

        sys.stdout = sys.__stdout__

        return opt_parameters

    def optimizeActuatorWithPSC(self, Actuator = bipathwolfromPlanetaryActuator, log=1, csv=0, printOptParams = 1):
        opt_parameters = None
        if csv and log:
            print("WARNING: Both csv and Log cannot be true")
            print("WARNING: Please set either csv or log to be 0 in \"Optimizer.optimizeActuator(Actuator)\" function")
            print(" ")
            print("ACTION:Making log to be false and csv to be true")
            log = 0
            csv = 1
        elif not csv and not log:
            print("WARNING: Both csv and Log cannot be false")
            print("WARNING: Please set either csv or log to be 1 in \"Optimizer.optimizeActuator(Actuator)\" function")
            print(" ")
            print("ACTION:Making log to be False and csv to be true")
            log = 0
            csv = 1
        
        if csv:
            fileName = f"./results/results_bilevel_{Actuator.motor.motorName}/WPG_BILEVEL_{Actuator.stressAnalysisMethodName}_{Actuator.motor.motorName}_CSV.csv"
        elif log:
            fileName = f"./results/results_bilevel_{Actuator.motor.motorName}/WPG_BILEVEL_{Actuator.stressAnalysisMethodName}_{Actuator.motor.motorName}_LOG.txt"
        
        with open(fileName, "w") as wolfromLogFile:
            sys.stdout = wolfromLogFile
            self.printOptimizationParameters(Actuator, log, csv)
            
            if log:
                print(" ")
                print("*****************************************************************")
                print("FOR MINIMUM GEAR RATIO ", self.gearRatioIter)
                print("*****************************************************************")
                print(" ")
            elif csv:
                # Printing the optimization iterations below
                print(" ")
                print("iter, gearRatio, moduleBig, moduleSmall, Ns, NpBig, NpSmall, NrBig, NrSmall, numPlanet,PSCs, PSCp1, PSCp2, PSCr1, PSCr2, fwSunMM, fwPlanetBigMM, fwPanetSmallMM, fwRingBigMM, fwRingSmallMM, CD_SP1, CD_PR1, CD_PR2, mass, eff, peakTorque, Cost, Torque_Density")
            while self.gearRatioIter <= self.GEAR_RATIO_MAX: 
                self.iter = 0
                opt_done = 0
                self.Cost = 100000
                MinCost = self.Cost
                opt_parameters = []
                Actuator.wolfromPlanetaryGearbox.setModuleBig(self.MODULE_BIG_MIN)
                while Actuator.wolfromPlanetaryGearbox.moduleBig <= self.MODULE_BIG_MAX:
                    # Setting Module Small
                    Actuator.wolfromPlanetaryGearbox.setModuleSmall(self.MODULE_SMALL_MIN)
                    while (Actuator.wolfromPlanetaryGearbox.moduleSmall <= self.MODULE_SMALL_MAX):
                        # Setting Ns
                        Actuator.wolfromPlanetaryGearbox.setNs(self.NUM_TEETH_SUN_MIN)
                        while (2*Actuator.wolfromPlanetaryGearbox.getPCRadiusSunM()*1000) <= Actuator.maxGearboxDiameter:
                            # Setting Np Big
                            Actuator.wolfromPlanetaryGearbox.setNpBig(self.NUM_TEETH_PLANET_BIG_MIN)
                            while (2*Actuator.wolfromPlanetaryGearbox.getPCRadiusPlanetBigM()*1000) <= Actuator.maxGearboxDiameter/2:
                                # Setting Np Small
                                Actuator.wolfromPlanetaryGearbox.setNpSmall(self.NUM_TEETH_PLANET_SMALL_MIN)
                                while (2*Actuator.wolfromPlanetaryGearbox.getPCRadiusPlanetSmallM()*1000) <= Actuator.maxGearboxDiameter/2:
                                    # Setting Nr Small
                                    Actuator.wolfromPlanetaryGearbox.setNrSmall(Actuator.wolfromPlanetaryGearbox.NpSmall + 
                                                                                Actuator.wolfromPlanetaryGearbox.NpBig +
                                                                                Actuator.wolfromPlanetaryGearbox.Ns)
                                    # Setting Nr Big
                                    Actuator.wolfromPlanetaryGearbox.setNrBig(2*Actuator.wolfromPlanetaryGearbox.NpBig +
                                                                                Actuator.wolfromPlanetaryGearbox.Ns)
                                    if ((2*Actuator.wolfromPlanetaryGearbox.getPCRadiusRingBigM()*1000) <= Actuator.maxGearboxDiameter and Actuator.getIdRequired2MM() <= 100): # and ((2*Actuator.wolfromPlanetaryGearbox.getPCRadiusRingSmallM()*1000) <= maxGearBoxDia):
                                        # TODO: Ask Deepak: What is getIDRequired2MM()? and also tell him to write a more meaningful function name
                                        # Setting number of Planet
                                        Actuator.wolfromPlanetaryGearbox.setNumPlanet(self.NUM_PLANET_MIN)
                                        while Actuator.wolfromPlanetaryGearbox.numPlanet <= self.NUM_PLANET_MAX:
                                            if (Actuator.wolfromPlanetaryGearbox.geometricConstraint() and 
                                                Actuator.wolfromPlanetaryGearbox.meshingConstraint() and 
                                                Actuator.wolfromPlanetaryGearbox.noPlanetInterferenceConstraint()):
                                                self.totalFeasibleGearboxes += 1
                                                # Fiter for the Gear Ratio
                                                if (Actuator.wolfromPlanetaryGearbox.gearRatio() >= self.gearRatioIter and 
                                                    Actuator.wolfromPlanetaryGearbox.gearRatio() <= (self.gearRatioIter + 1)):
                                                    
                                                    self.totalGearboxesWithReqGR += 1
                                                    
                                                    # Cost Calculation
                                                    Actuator.updateFacewidth()
                                                    # massActuator = Actuator.getMassStructureKG()
                                                    massActuator = Actuator.getMassKG_3DP()
                                                    effActuator = Actuator.wolfromPlanetaryGearbox.getEfficiency()
                                                    self.Cost = (self.K_Mass * massActuator) + (self.K_Eff * effActuator)
                                                    
                                                    if self.Cost < MinCost:
                                                        MinCost = self.Cost
                                                        self.iter += 1
                                                        opt_done = 1
                                                        Actuator.genEquationFile()

                                                        opt_parameters = [Actuator.wolfromPlanetaryGearbox.gearRatio(),
                                                                          Actuator.wolfromPlanetaryGearbox.numPlanet,
                                                                          Actuator.wolfromPlanetaryGearbox.Ns,
                                                                          Actuator.wolfromPlanetaryGearbox.NpBig,
                                                                          Actuator.wolfromPlanetaryGearbox.NrBig,
                                                                          Actuator.wolfromPlanetaryGearbox.NpSmall,
                                                                          Actuator.wolfromPlanetaryGearbox.NrSmall,
                                                                          Actuator.wolfromPlanetaryGearbox.moduleBig,
                                                                          Actuator.wolfromPlanetaryGearbox.moduleSmall]
                                                        opt_planetaryGearbox = bipathwolfromPlanetaryGearbox  (design_parameters         = self.design_parameters,
                                                                                                         gear_standard_parameters  = self.gear_standard_parameters,
                                                                                                         Ns                        = Actuator.wolfromPlanetaryGearbox.Ns,
                                                                                                         NpBig                     = Actuator.wolfromPlanetaryGearbox.NpBig,
                                                                                                         NpSmall                   = Actuator.wolfromPlanetaryGearbox.NpSmall,
                                                                                                         NrBig                     = Actuator.wolfromPlanetaryGearbox.NrBig,
                                                                                                         NrSmall                   = Actuator.wolfromPlanetaryGearbox.NrSmall,
                                                                                                         numPlanet                 = Actuator.wolfromPlanetaryGearbox.numPlanet,
                                                                                                         moduleBig                 = Actuator.wolfromPlanetaryGearbox.moduleBig,
                                                                                                         moduleSmall               = Actuator.wolfromPlanetaryGearbox.moduleSmall,
                                                                                                         densityGears              = Actuator.wolfromPlanetaryGearbox.densityGears,
                                                                                                         densityStructure          = Actuator.wolfromPlanetaryGearbox.densityStructure,
                                                                                                         fwSunMM                   = Actuator.wolfromPlanetaryGearbox.fwSunMM,
                                                                                                         fwPlanetBigMM             = Actuator.wolfromPlanetaryGearbox.fwPlanetBigMM,
                                                                                                         fwPlanetSmallMM           = Actuator.wolfromPlanetaryGearbox.fwPlanetSmallMM,
                                                                                                         fwRingBigMM               = Actuator.wolfromPlanetaryGearbox.fwRingBigMM,
                                                                                                         fwRingSmallMM             = Actuator.wolfromPlanetaryGearbox.fwRingSmallMM,
                                                                                                         maxGearAllowableStressMPa = Actuator.wolfromPlanetaryGearbox.maxGearAllowableStressMPa)
                                                        opt_actuator = bipathwolfromPlanetaryActuator(design_parameters        = self.design_parameters,
                                                                                                motor                    = Actuator.motor, 
                                                                                                bipathwolfromPlanetaryGearbox  = opt_planetaryGearbox, 
                                                                                                FOS                      = Actuator.FOS, 
                                                                                                serviceFactor            = Actuator.serviceFactor, 
                                                                                                maxGearboxDiameter       = Actuator.maxGearboxDiameter, # mm 
                                                                                                stressAnalysisMethodName = "Lewis") # Lewis or AGMA
                                            
                                            Actuator.wolfromPlanetaryGearbox.setNumPlanet(Actuator.wolfromPlanetaryGearbox.numPlanet + 1)
                                        # Actuator.wolfromPlanetaryGearbox.setNrBig(Actuator.wolfromPlanetaryGearbox.NrBig + 1)
                                        # Actuator.wolfromPlanetaryGearbox.setNrSmall(Actuator.wolfromPlanetaryGearbox.NrSmall + 1)
                                    Actuator.wolfromPlanetaryGearbox.setNpSmall(Actuator.wolfromPlanetaryGearbox.NpSmall + 1)
                                Actuator.wolfromPlanetaryGearbox.setNpBig(Actuator.wolfromPlanetaryGearbox.NpBig + 1)
                            Actuator.wolfromPlanetaryGearbox.setNs(Actuator.wolfromPlanetaryGearbox.Ns + 1)
                        Actuator.wolfromPlanetaryGearbox.setModuleSmall(Actuator.wolfromPlanetaryGearbox.moduleSmall + 0.100)
                        Actuator.wolfromPlanetaryGearbox.setModuleSmall(round(Actuator.wolfromPlanetaryGearbox.moduleSmall, 1)) # Round Off
                    Actuator.wolfromPlanetaryGearbox.setModuleBig(Actuator.wolfromPlanetaryGearbox.moduleBig + 0.100)
                    Actuator.wolfromPlanetaryGearbox.setModuleBig(round(Actuator.wolfromPlanetaryGearbox.moduleBig, 1)) # Round Off
                if (opt_done == 1):
                    self.wpgOpt = optimal_continuous_PSC_wpg(GEAR_RATIO_MIN = opt_parameters[0],
                                                             numPlanet      = opt_parameters[1],
                                                             Ns_init        = opt_parameters[2],
                                                             Np1_init       = opt_parameters[3],
                                                             Nr1_init       = opt_parameters[4],
                                                             Np2_init       = opt_parameters[5],
                                                             Nr2_init       = opt_parameters[6],
                                                             M1_init        = opt_parameters[7] * 10,
                                                             M2_init        = opt_parameters[8] * 10)
                    _, calc_centerDistForManufacturing = self.wpgOpt.solve()
                    self.wpgOpt.solve(optimizeForManufacturing=True,
                                      centerDistForManufacturing=calc_centerDistForManufacturing)
                    self.printOptimizationResults(opt_actuator, log, csv)  
                self.gearRatioIter += self.GEAR_RATIO_STEP

    
                if log:
                    print("Number of iterations: ", self.iter)
                    print("Total Feasible Gearboxes:", self.totalFeasibleGearboxes)
                    print("Total Gearboxes with requires Gear Ratio:", self.totalGearboxesWithReqGR)
                    print("*****************************************************************")
                    print("----------------------------END----------------------------------")
                    print(" ")

        sys.stdout = sys.__stdout__

        return opt_parameters

    def printOptimizationParameters(self, Actuator = bipathwolfromPlanetaryActuator, log=1, csv=0):
        # Motor Parameters
        maxMotorAngVelRPM       = Actuator.motor.maxMotorAngVelRPM
        maxMotorAngVelRadPerSec = Actuator.motor.maxMotorAngVelRadPerSec
        maxMotorTorque          = Actuator.motor.maxMotorTorque
        maxMotorPower           = Actuator.motor.maxMotorPower
        motorMass               = Actuator.motor.massKG
        motorDia                = Actuator.motor.motorDiaMM
        motorLength             = Actuator.motor.motorLengthMM
        
        # Planetary Gearbox Parameters
        maxGearAllowableStressMPa = Actuator.bipathwolfromPlanetaryGearbox.maxGearAllowableStressMPa
        
        # Gear strength parameters
        FOS                      = Actuator.FOS
        serviceFactor            = Actuator.serviceFactor
        maxGearBoxDia            = Actuator.maxGearboxDiameter
        stressAnalysisMethodName = Actuator.stressAnalysisMethodName
        
        if log:
           # Printing the parameters below
            print("--------------------Motor Parameters--------------------")
            print("maxMotorAngVelRPM:       ", maxMotorAngVelRPM)
            print("maxMotorAngVelRadPerSec: ", maxMotorAngVelRadPerSec)
            print("maxMotorTorque:          ", maxMotorTorque)
            print("maxMotorPower:           ", maxMotorPower)
            print("motorMass:               ", motorMass)
            print("motorDia:                ", motorDia)
            print("motorLength:             ", motorLength)
            print(" ")
            print("--------------Planetary Gearbox Parameters--------------")
            print("maxGearAllowableStressMPa: ", maxGearAllowableStressMPa)
            print(" ")
            print("-----------Gear strength and size parameters------------")
            print("FOS:                     ", FOS)
            print("serviceFactor:           ", serviceFactor)
            print("stressAnalysisMethodName:", stressAnalysisMethodName)
            print("maxGearBoxDia:           ", maxGearBoxDia)
            print(" ")
            print("-----------------Optimization Parameters-----------------")
            print("K_Mass:                     ", self.K_Mass)
            print("K_Eff:                      ", self.K_Eff)
            print("MODULE_BIG_MIN:             ", self.MODULE_BIG_MIN)
            print("MODULE_BIG_MAX:             ", self.MODULE_BIG_MAX)
            print("MODULE_SMALL_MIN:           ", self.MODULE_SMALL_MIN)
            print("MODULE_SMALL_MAX:           ", self.MODULE_SMALL_MAX)
            print("NUM_PLANET_MIN:             ", self.NUM_PLANET_MIN)
            print("NUM_PLANET_MAX:             ", self.NUM_PLANET_MAX)
            print("NUM_TEETH_SUN_MIN:          ", self.NUM_TEETH_SUN_MIN)
            print("NUM_TEETH_PLANET_BIG_MIN:   ", self.NUM_TEETH_PLANET_BIG_MIN)
            print("NUM_TEETH_PLANET_SMALL_MIN: ", self.NUM_TEETH_PLANET_SMALL_MIN)
            print("GEAR_RATIO_MIN:             ", self.GEAR_RATIO_MIN)
            print("GEAR_RATIO_MAX:             ", self.GEAR_RATIO_MAX)
            print("GEAR_RATIO_STEP:            ", self.GEAR_RATIO_STEP)
        elif csv:
            print("Motor Parameters:")
            print("maxMotorAngVelRPM,","maxMotorAngVelRadPerSec,","maxMotorTorque,","maxMotorPower,","motorMass,","motorDia,", "motorLength")
            print(maxMotorAngVelRPM,",", maxMotorAngVelRadPerSec,",", maxMotorTorque,",",maxMotorPower,",",motorMass,",",motorDia,",", motorLength)
            print(" ")
            print("Gear strength and size parameters:")
            print("FOS,", "serviceFactor,", "stressAnalysisMethodName,", "maxGearBoxDia,","maxGearAllowableStressMPa")
            print(FOS,",", serviceFactor,",", stressAnalysisMethodName,",", maxGearBoxDia,",",maxGearAllowableStressMPa)
            print(" ")
            print("Optimization Parameters:")            
            print("K_mass, K_Eff, MODULE_BIG_MIN, MODULE_BIG_MAX, MODULE_SMALL_MIN, MODULE_SMALL_MAX, NUM_PLANET_MIN, NUM_PLANET_MAX, NUM_TEETH_SUN_MIN, NUM_TEETH_PLANET_BIG_MIN, NUM_TEETH_PLANET_SMALL_MIN, GEAR_RATIO_MIN, GEAR_RATIO_MAX, GEAR_RATIO_STEP")
            print(self.K_Mass,",", self.K_Eff,",", self.MODULE_BIG_MIN,",", self.MODULE_BIG_MAX,",", self.MODULE_SMALL_MIN,",", self.MODULE_SMALL_MAX,",",self.NUM_PLANET_MIN,",", self.NUM_PLANET_MAX,",", self.NUM_TEETH_SUN_MIN,",", self.NUM_TEETH_PLANET_BIG_MIN,",",self.NUM_TEETH_PLANET_SMALL_MIN,",", self.GEAR_RATIO_MIN,",", self.GEAR_RATIO_MAX,",", self.GEAR_RATIO_STEP)

    def printOptimizationResults(self, Actuator = bipathwolfromPlanetaryActuator, log=1, csv=0):
        Actuator.setVariables()
        if log:
            # Printing the parameters below
            print("Iteration: ", self.iter)
            Actuator.printParametersLess()
            Actuator.printVolumeAndMassParameters()
            if self.UsePSCasVariable == 1 :
                Opt_PSC_ring1 = self.wpgOpt.model.PSCr1.value
                Opt_PSC_ring2 = self.wpgOpt.model.PSCr2.value
                Opt_PSC_planet1 = self.wpgOpt.model.PSCp1.value
                Opt_PSC_planet2 = self.wpgOpt.model.PSCp2.value
                Opt_PSC_sun = self.wpgOpt.model.PSCs.value
            else :
                Opt_PSC_ring1   = 0
                Opt_PSC_ring2   = 0
                Opt_PSC_planet1 = 0
                Opt_PSC_planet2 = 0
                Opt_PSC_sun     = 0            
            eff = round(Actuator.planetaryGearbox.getEfficiency(), 3)
            if self.UsePSCasVariable == 1 : 
                eff  = round(self.wpgOpt.getEfficiency(Var=False), 3)
                print ("Efficiency with PSC", eff)
                print(f"PSC Values - Ring: {Opt_PSC_ring1}, Planet: {Opt_PSC_planet1}, Ring2: {Opt_PSC_ring2}, Planet2: {Opt_PSC_planet2}, Sun: {Opt_PSC_sun}")
            print(" ")
            print("Cost:", self.Cost)
            print("*****************************************************************")
            print(" ")
            print("Cost:", self.Cost)
            print("*****************************************************************")
        elif csv:
            iter            = self.iter
            gearRatio       = Actuator.bipathwolfromPlanetaryGearbox.gearRatio()
            moduleBig       = Actuator.bipathwolfromPlanetaryGearbox.moduleBig
            moduleSmall     = Actuator.bipathwolfromPlanetaryGearbox.moduleSmall
            Ns              = Actuator.bipathwolfromPlanetaryGearbox.Ns 
            NpBig           = Actuator.bipathwolfromPlanetaryGearbox.NpBig
            NpSmall         = Actuator.bipathwolfromPlanetaryGearbox.NpSmall 
            NrBig           = Actuator.bipathwolfromPlanetaryGearbox.NrBig
            NrSmall         = Actuator.bipathwolfromPlanetaryGearbox.NrSmall 
            numPlanet       = Actuator.bipathwolfromPlanetaryGearbox.numPlanet
            fwSunMM         = round(Actuator.bipathwolfromPlanetaryGearbox.fwSunMM    , 3)
            fwPlanetBigMM   = round(Actuator.bipathwolfromPlanetaryGearbox.fwPlanetBigMM , 3)
            fwPlanetSmallMM = round(Actuator.bipathwolfromPlanetaryGearbox.fwPlanetSmallMM , 3)
            fwRingBigMM     = round(Actuator.bipathwolfromPlanetaryGearbox.fwRingBigMM   , 3)
            fwRingSmallMM   = round(Actuator.bipathwolfromPlanetaryGearbox.fwRingSmallMM   , 3)
            if self.UsePSCasVariable == 1 :
                Opt_PSC_ring1   = self.wpgOpt.model.PSCr1.value
                Opt_PSC_ring2   = self.wpgOpt.model.PSCr2.value
                Opt_PSC_planet1 = self.wpgOpt.model.PSCp1.value
                Opt_PSC_planet2 = self.wpgOpt.model.PSCp2.value
                Opt_PSC_sun     = self.wpgOpt.model.PSCs.value
                Opt_CD_SP1, Opt_CD_PR1, Opt_CD_PR2 = self.wpgOpt.getCenterDistance(Var=False)
            else :
                Opt_PSC_ring1   = 0.0
                Opt_PSC_ring2   = 0.0
                Opt_PSC_planet1 = 0.0
                Opt_PSC_planet2 = 0.0
                Opt_PSC_sun     = 0.0
                Opt_CD_SP1 = ((Ns      + NpBig)/2)   * moduleBig
                Opt_CD_PR1 = ((NrBig   - NpBig)/2)   * moduleBig
                Opt_CD_PR2 = ((NrSmall - NpSmall)/2) * moduleSmall

            # mass       = round(Actuator.getMassStructureKG(), 3)
            mass       = round(Actuator.getMassKG_3DP(), 3)
            eff        = round(Actuator.bipathwolfromPlanetaryGearbox.getEfficiency(), 3)
            if self.UsePSCasVariable == 1 :
                eff  = round(self.wpgOpt.getEfficiency(Var=False), 3)
            peakTorque      = round(Actuator.motor.getMaxMotorTorque()*Actuator.bipathwolfromPlanetaryGearbox.gearRatio(), 3)
            Cost       = Actuator.cost() #self.K_Mass * mass + self.K_Eff * eff
            torque_density  = round(peakTorque/mass, 3)
            Outer_bearing_mass = Actuator.bearing_mass
            Actuator_width = Actuator.actuator_width
            print(iter,",", gearRatio,",",moduleBig,",",moduleSmall,",", Ns,",", NpBig,",", NpSmall,",", NrBig,",",NrSmall,",", numPlanet,",", fwSunMM,",", fwPlanetBigMM,",",fwPlanetSmallMM,",", fwRingBigMM,",",fwRingSmallMM,",", mass, ",", eff,",", peakTorque,",", Cost, ",", torque_density, ",", Outer_bearing_mass, ",", Actuator_width)

    def cost(self, Actuator=bipathwolfromPlanetaryActuator):
        K_gearRatio = 0
        if self.gearRatioReq != 0:
            K_gearRatio = 1

        gearRatio_err = np.sqrt((Actuator.bipathwolfromPlanetaryGearbox.gearRatio() - self.gearRatioReq)**2)

        mass = Actuator.getMassKG_3DP()
        eff = Actuator.bipathwolfromPlanetaryGearbox.getEfficiency()
        width = Actuator.bipathwolfromPlanetaryGearbox.fwPlanetBigMM + Actuator.bipathwolfromPlanetaryGearbox.fwPlanetSmallMM
        cost = (self.K_Mass    * mass 
                + self.K_Eff   * eff 
                + self.K_Width * width 
                + K_gearRatio  * gearRatio_err)
        return cost
    
#end