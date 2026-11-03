import Opt_bipathWolfromPlanetaryGBOptimisation as drv

A = drv.Actuator_U8
g = A.bipathwolfromPlanetaryGearbox
g.setModuleBig(0.5); g.setModuleSmall(0.5)
g.setNs(56); g.setNpBig(48); g.setNpSmall(28)
g.setNrBig(152); g.setNrSmall(132); g.setNumPlanet(4)
print("rules ok:", g.geometricConstraint(), g.meshingConstraint(), g.noPlanetInterferenceConstraint())

for beta in [0.5, 0.625, 0.75, 1.0]:
    A.design_params["bypass_load_share"] = beta
    A.updateFacewidth()
    F = A.getToothForces()
    mass = A.getMassKG_3DP()
    print(f"beta {beta}: direct {abs(F[2]):.0f} N, bypass {abs(A.Ft_bypass):.0f} N | "
          f"ring_s {g.fwRingSmallMM:.2f}  fs {g.fwFloatingSunMM:.2f}  idler {g.fwIdlerMM:.2f}  "
          f"planet_b {g.fwPlanetBigMM:.2f} mm | mass {mass*1000:.0f} g")