"""Two-way equation calculators.

Each entry replaces an existing calculator (same slug) so that ANY field can be left blank and solved.
Variables: (id, label, units, init). Units: (label, factor_to_base[, offset]); base = (value + offset) * factor.
solve: id -> JS expression over v (base values), or a list of (required ids, expression) alternatives.
"""

# ---- unit tables --------------------------------------------------------------------------
DIST = [("mi", 1609.344), ("km", 1000), ("m", 1), ("ft", .3048), ("nmi", 1852)]
TIME = [("h", 3600), ("min", 60), ("s", 1), ("days", 86400)]
SPEED = [("mph", .44704), ("km/h", 1 / 3.6), ("m/s", 1), ("knots", 1852 / 3600), ("ft/s", .3048)]
LEN = [("m", 1), ("cm", .01), ("mm", .001), ("km", 1000), ("in", .0254), ("ft", .3048)]
MASS = [("kg", 1), ("g", .001), ("lb", .45359237), ("oz", .028349523125)]
FORCE = [("N", 1), ("kN", 1000), ("lbf", 4.4482216152605)]
ENERGY = [("J", 1), ("kJ", 1000), ("cal", 4.184), ("kcal", 4184), ("Wh", 3600), ("kWh", 3.6e6)]
POWER = [("W", 1), ("kW", 1000), ("mW", .001), ("hp", 745.69987158)]
PRESS = [("kPa", 1000), ("Pa", 1), ("atm", 101325), ("bar", 1e5), ("psi", 6894.757293168), ("mmHg", 133.322387415)]
VOL = [("L", .001), ("mL", 1e-6), ("m³", 1), ("cm³", 1e-6), ("gal", .003785411784), ("ft³", .028316846592)]
TEMP = [("°C", 1, 273.15), ("K", 1, 0), ("°F", 5 / 9, 459.67)]
VOLT = [("V", 1), ("mV", 1e-3), ("kV", 1e3)]
AMP = [("A", 1), ("mA", 1e-3)]
OHM = [("Ω", 1), ("kΩ", 1e3), ("MΩ", 1e6)]
FARAD = [("µF", 1e-6), ("nF", 1e-9), ("pF", 1e-12), ("mF", 1e-3), ("F", 1)]
AREA = [("m²", 1), ("cm²", 1e-4), ("ft²", .09290304), ("in²", .00064516)]
G = "9.80665"
EQ = {}


def E(slug, vars, solve, need=None, extra=None, formula=None, title=None, desc=None):
    EQ[slug] = dict(eq=dict(vars=vars, solve=solve, need=need, extra=extra), formula=formula, title=title, desc=desc)


def three(a, b, c, f, fa, fb):
    """Solve for each of three variables given the other two (c = f(a, b))."""
    return {c: f, a: fa, b: fb}


# ======================= motion & mechanics =======================
E("speed-calculator",
  [("d", "Distance", DIST, 150), ("t", "Time", TIME, 3), ("s", "Average speed", SPEED, None)],
  {"d": "v.s*v.t", "t": "v.d/v.s", "s": "v.d/v.t"},
  extra="return [['Speed in mph',N(v.s/.44704,3)],['Speed in km/h',N(v.s*3.6,3)],['Speed in m/s',N(v.s,3)],['Speed in knots',N(v.s/.514444,3)],['Pace per mile',v.s>0?Math.floor(1609.344/v.s/60)+':'+('0'+Math.round(1609.344/v.s%60)).slice(-2):'-']];",
  formula="speed = distance / time, so distance = speed x time and time = distance / speed. Enter any two and the third is solved.",
  title="Speed, Distance and Time Calculator", desc="Enter any two of speed, distance and time and get the third.")

E("pace-calculator",
  [("dist", "Distance", [("km", 1000), ("mi", 1609.344), ("m", 1)], 5), ("time", "Time", [("min", 60), ("h", 3600), ("s", 1)], 25), ("pace", "Pace (decimal minutes, e.g. 8.5 = 8:30)", [("min/km", .06), ("min/mi", 60 / 1609.344)], None)],
  {"dist": "v.time/v.pace", "time": "v.pace*v.dist", "pace": "v.time/v.dist"},
  extra="var f=function(x){var t=Math.round(x);return Math.floor(t/60)+':'+('0'+t%60).slice(-2);};return [['Pace per km',f(v.pace*1000)],['Pace per mile',f(v.pace*1609.344)],['Speed',N(3.6/v.pace,2)+' km/h ('+N(2.23694/v.pace,2)+' mph)'],['5K at this pace',f(v.pace*5000)],['10K at this pace',f(v.pace*10000)]];",
  formula="pace = time / distance. Enter any two of distance, time and pace to solve the third. Pace is entered as decimal minutes; the table below shows it as minutes:seconds.",
  title="Running Pace Calculator", desc="Enter any two of distance, time and pace and get the third.")

E("acceleration-calculator",
  [("u", "Initial velocity", SPEED[::1][2:3] + SPEED[:2] + SPEED[3:], 0), ("w", "Final velocity", SPEED[::1][2:3] + SPEED[:2] + SPEED[3:], 26.8224),
   ("t", "Time", [("s", 1), ("min", 60), ("h", 3600)], 6), ("a", "Acceleration", [("m/s²", 1), ("g", 9.80665), ("ft/s²", .3048)], None)],
  {"a": "(v.w-v.u)/v.t", "u": "v.w-v.a*v.t", "w": "v.u+v.a*v.t", "t": "(v.w-v.u)/v.a"}, need=3,
  extra="var dist=(v.u+v.w)/2*v.t;return [['Distance covered',N(dist,2)+' m'],['Acceleration in g',N(v.a/9.80665,3)+' g']];",
  formula="a = (v - u) / t, where u is initial velocity, v final velocity and t time. Enter any three of the four values.",
  title="Acceleration Calculator", desc="Solve acceleration, initial or final velocity, or time from any three values.")

E("force-calculator",
  [("F", "Force", FORCE, None), ("m", "Mass", MASS, 10), ("a", "Acceleration", [("m/s²", 1), ("g", 9.80665), ("ft/s²", .3048)], 9.80665)],
  three("m", "a", "F", "v.m*v.a", "v.F/v.a", "v.F/v.m"),
  formula="Newton's second law: F = m x a. Enter any two of force, mass and acceleration.",
  title="Force Calculator (F = ma)", desc="Enter any two of force, mass and acceleration and get the third.")

E("kinetic-energy-calculator",
  [("KE", "Kinetic energy", ENERGY, None), ("m", "Mass", MASS, 1500), ("s", "Speed", SPEED[2:3] + SPEED[:2] + SPEED[3:], 25)],
  {"KE": ".5*v.m*v.s*v.s", "m": "2*v.KE/(v.s*v.s)", "s": "Math.sqrt(2*v.KE/v.m)"},
  formula="Kinetic energy KE = 1/2 x m x v squared. Doubling speed quadruples the energy.",
  title="Kinetic Energy Calculator", desc="Enter any two of kinetic energy, mass and speed and get the third.")

E("potential-energy-calculator",
  [("PE", "Potential energy", ENERGY, None), ("m", "Mass", MASS, 10), ("h", "Height", LEN, 20)],
  {"PE": f"v.m*{G}*v.h", "m": f"v.PE/({G}*v.h)", "h": f"v.PE/({G}*v.m)"},
  formula="Gravitational potential energy PE = m x g x h with g = 9.80665 m/s squared.",
  title="Gravitational Potential Energy Calculator", desc="Enter any two of potential energy, mass and height and get the third.")

E("momentum-calculator",
  [("p", "Momentum (kg·m/s)", None, None), ("m", "Mass", MASS, 1500), ("s", "Velocity", SPEED[2:3] + SPEED[:2] + SPEED[3:], 25)],
  three("m", "s", "p", "v.m*v.s", "v.p/v.s", "v.p/v.m"),
  extra="return [['Kinetic energy',N(.5*v.m*v.s*v.s,2)+' J']];",
  formula="Momentum p = m x v. Enter any two of momentum, mass and velocity.",
  title="Momentum Calculator", desc="Enter any two of momentum, mass and velocity and get the third.")

E("pressure-calculator",
  [("P", "Pressure", PRESS, None), ("F", "Force", FORCE, 500), ("A", "Area", AREA, 0.02)],
  three("F", "A", "P", "v.F/v.A", "v.P*v.A", "v.F/v.P"),
  extra="return [['Pressure in psi',N(v.P/6894.757,3)],['Pressure in kPa',N(v.P/1000,3)],['Pressure in atm',N(v.P/101325,5)]];",
  formula="Pressure P = F / A. Enter any two of pressure, force and area.",
  title="Pressure Calculator (Force over Area)", desc="Enter any two of pressure, force and area and get the third.")

E("hookes-law-calculator",
  [("F", "Force", FORCE, None), ("k", "Spring constant (N/m)", None, 200), ("x", "Extension", LEN, 0.15)],
  three("k", "x", "F", "v.k*v.x", "v.F/v.x", "v.F/v.k"),
  extra="return [['Stored energy',N(.5*v.k*v.x*v.x,4)+' J']];",
  formula="Hooke's law: F = k x. Enter any two of force, spring constant and extension.",
  title="Hooke's Law Spring Calculator", desc="Enter any two of force, spring constant and extension and get the third.")

E("wave-speed-calculator",
  [("v0", "Wave speed (m/s)", None, None), ("f", "Frequency (Hz)", None, 440), ("wl", "Wavelength", LEN, 0.78)],
  {"v0": "v.f*v.wl", "f": "v.v0/v.wl", "wl": "v.v0/v.f"},
  extra="return [['Period',N(1/v.f,6)+' s']];",
  formula="Wave speed = frequency x wavelength. Enter any two of the three.",
  title="Wave Speed Calculator", desc="Enter any two of wave speed, frequency and wavelength and get the third.")

E("wavelength-frequency-calculator",
  [("f", "Frequency", [("GHz", 1e9), ("MHz", 1e6), ("kHz", 1e3), ("Hz", 1), ("THz", 1e12)], 2.4), ("wl", "Wavelength", [("m", 1), ("cm", .01), ("mm", .001), ("µm", 1e-6), ("nm", 1e-9), ("km", 1000)], None)],
  {"wl": "299792458/v.f", "f": "299792458/v.wl"}, need=1,
  extra="return [['Photon energy',(6.62607015e-34*v.f).toExponential(4)+' J'],['Photon energy',N(6.62607015e-34*v.f/1.602176634e-19,6)+' eV']];",
  formula="Wavelength = speed of light / frequency, with c = 299,792,458 m/s. Enter either value.",
  title="Wavelength and Frequency Calculator", desc="Convert between frequency and wavelength of light and radio waves.")

E("efficiency-calculator",
  [("eff", "Efficiency (%)", None, None), ("inp", "Input energy or power", None, 1000), ("outp", "Useful output", None, 750)],
  {"eff": "v.outp/v.inp*100", "inp": "v.outp/v.eff*100", "outp": "v.inp*v.eff/100"},
  extra="return [['Wasted',N(v.inp-v.outp,3)]];",
  formula="Efficiency = useful output / input x 100%. Enter any two values (use the same unit for input and output).",
  title="Efficiency Calculator", desc="Enter any two of efficiency, input and output and get the third.")

E("gear-ratio-calculator",
  [("r", "Gear ratio (driven : driving)", None, None), ("drv", "Driving gear teeth", None, 15), ("drn", "Driven gear teeth", None, 45)],
  three("drv", "drn", "r", "v.drn/v.drv", "v.drn/v.r", "v.r*v.drv"),
  extra="return [['Type',v.r>1?'Reduction (more torque, less speed)':v.r<1?'Overdrive (more speed, less torque)':'1:1']];",
  formula="Gear ratio = driven teeth / driving teeth. Enter any two values.",
  title="Gear Ratio Calculator", desc="Enter any two of gear ratio, driving teeth and driven teeth and get the third.")

E("horsepower-calculator",
  [("P", "Power", [("hp", 745.69987158), ("kW", 1000), ("W", 1)], None), ("T", "Torque", [("lb-ft", 1.3558179483314), ("N·m", 1)], 300), ("rpm", "Engine speed (RPM)", None, 5000)],
  {"P": "v.T*v.rpm*2*Math.PI/60", "T": "v.P*60/(2*Math.PI*v.rpm)", "rpm": "v.P*60/(2*Math.PI*v.T)"},
  formula="Power = torque x angular speed. In US units, horsepower = torque (lb-ft) x RPM / 5252.",
  title="Horsepower from Torque Calculator", desc="Enter any two of horsepower, torque and RPM and get the third.")

E("torque-calculator",
  [("T", "Torque", [("N·m", 1), ("lb-ft", 1.3558179483314), ("lb-in", .1129848290276)], None), ("F", "Force (perpendicular)", FORCE, 200), ("r", "Lever arm length", LEN, 0.3)],
  three("F", "r", "T", "v.F*v.r", "v.T/v.r", "v.T/v.F"),
  formula="Torque = force x perpendicular lever arm. Enter any two of torque, force and lever arm length.",
  title="Torque Calculator", desc="Enter any two of torque, force and lever arm and get the third.")

E("work-power-calculator",
  [("W", "Work / energy", ENERGY, None), ("F", "Force", FORCE, 50), ("d", "Distance", LEN, 10), ("P", "Power", POWER, None), ("t", "Time", [("s", 1), ("min", 60), ("h", 3600)], 5)],
  {"W": [(("F", "d"), "v.F*v.d"), (("P", "t"), "v.P*v.t")], "F": [(("W", "d"), "v.W/v.d")], "d": [(("W", "F"), "v.W/v.F")],
   "P": [(("W", "t"), "v.W/v.t")], "t": [(("W", "P"), "v.W/v.P")]}, need=3,
  formula="Work W = F x d and power P = W / t. Enter any three values (for example force, distance and time).",
  title="Work and Power Calculator", desc="Enter any three of work, force, distance, power and time and solve the rest.")

E("centripetal-force-calculator",
  [("F", "Centripetal force", FORCE, None), ("m", "Mass", MASS, 1000), ("s", "Speed", SPEED[2:3] + SPEED[:2] + SPEED[3:], 20), ("r", "Radius", LEN, 50)],
  {"F": "v.m*v.s*v.s/v.r", "m": "v.F*v.r/(v.s*v.s)", "s": "Math.sqrt(v.F*v.r/v.m)", "r": "v.m*v.s*v.s/v.F"}, need=3,
  formula="Centripetal force F = m x v squared / r. Enter any three of the four values.",
  title="Centripetal Force Calculator", desc="Solve force, mass, speed or radius for circular motion from any three values.")

E("coulombs-law-calculator",
  [("F", "Force (N)", None, None), ("q1", "Charge 1", [("µC", 1e-6), ("nC", 1e-9), ("pC", 1e-12), ("C", 1)], 2), ("q2", "Charge 2", [("µC", 1e-6), ("nC", 1e-9), ("pC", 1e-12), ("C", 1)], 3), ("r", "Distance", LEN, 0.5)],
  {"F": "8.9875517923e9*v.q1*v.q2/(v.r*v.r)", "q1": "v.F*v.r*v.r/(8.9875517923e9*v.q2)", "q2": "v.F*v.r*v.r/(8.9875517923e9*v.q1)", "r": "Math.sqrt(8.9875517923e9*v.q1*v.q2/v.F)"}, need=3,
  formula="Coulomb's law: F = k x q1 x q2 / r squared, with k = 8.9876 x 10^9 N·m²/C². Enter any three of the four values.",
  title="Coulomb's Law Calculator", desc="Solve electric force, a charge, or distance from any three values.")

E("gravitational-force-calculator",
  [("F", "Gravitational force (N)", None, None), ("m1", "Mass 1", [("Earth masses", 5.972e24), ("kg", 1), ("Moon masses", 7.342e22), ("Sun masses", 1.989e30)], 1),
   ("m2", "Mass 2", [("Moon masses", 7.342e22), ("kg", 1), ("Earth masses", 5.972e24), ("Sun masses", 1.989e30)], 1), ("r", "Distance between centers", [("km", 1000), ("m", 1), ("mi", 1609.344), ("AU", 1.495978707e11)], 384400)],
  {"F": "6.6743e-11*v.m1*v.m2/(v.r*v.r)", "m1": "v.F*v.r*v.r/(6.6743e-11*v.m2)", "m2": "v.F*v.r*v.r/(6.6743e-11*v.m1)", "r": "Math.sqrt(6.6743e-11*v.m1*v.m2/v.F)"}, need=3,
  formula="Newton's law of gravitation: F = G x m1 x m2 / r squared, with G = 6.6743 x 10^-11. Enter any three values.",
  title="Gravitational Force Calculator", desc="Solve gravitational force, a mass, or distance from any three values.")

E("escape-velocity-calculator",
  [("ve", "Escape velocity", [("km/s", 1000), ("m/s", 1), ("mph", .44704)], None), ("M", "Mass of body", [("Earth masses", 5.972e24), ("kg", 1), ("Moon masses", 7.342e22), ("Sun masses", 1.989e30)], 1), ("r", "Radius", [("km", 1000), ("m", 1), ("mi", 1609.344)], 6371)],
  {"ve": "Math.sqrt(2*6.6743e-11*v.M/v.r)", "M": "v.ve*v.ve*v.r/(2*6.6743e-11)", "r": "2*6.6743e-11*v.M/(v.ve*v.ve)"},
  formula="Escape velocity = sqrt(2GM / r). Enter any two values.",
  title="Escape Velocity Calculator", desc="Solve escape velocity, mass or radius from any two values.")

E("mass-energy-calculator",
  [("E", "Energy", [("J", 1), ("kWh", 3.6e6), ("MJ", 1e6), ("kJ", 1000)], None), ("m", "Mass", [("g", .001), ("kg", 1), ("mg", 1e-6)], 1)],
  {"E": "v.m*299792458*299792458", "m": "v.E/(299792458*299792458)"}, need=1,
  formula="Einstein's equation E = m c squared, with c = 299,792,458 m/s. Enter either energy or mass.",
  title="Mass-Energy Equivalence (E = mc²) Calculator", desc="Convert between mass and energy with E = mc².")

E("half-life-calculator",
  [("N", "Amount remaining", None, None), ("N0", "Initial amount", None, 100), ("T", "Half-life", [("years", 1), ("days", 1 / 365.25), ("hours", 1 / 8766), ("seconds", 1 / 31557600)], 5730), ("t", "Elapsed time", [("years", 1), ("days", 1 / 365.25), ("hours", 1 / 8766), ("seconds", 1 / 31557600)], 11460)],
  {"N": "v.N0*Math.pow(.5,v.t/v.T)", "N0": "v.N/Math.pow(.5,v.t/v.T)", "t": "v.T*Math.log(v.N0/v.N)/Math.LN2", "T": "v.t*Math.LN2/Math.log(v.N0/v.N)"}, need=3,
  formula="N = N0 x (1/2)^(t / half-life). Enter any three of the four values.",
  title="Half-Life Calculator", desc="Solve remaining amount, starting amount, half-life or elapsed time from any three values.")

# ======================= electricity =======================
E("ohms-law-calculator",
  [("V", "Voltage", VOLT, 12), ("I", "Current", AMP, None), ("R", "Resistance", OHM, 4), ("P", "Power", [("W", 1), ("mW", 1e-3), ("kW", 1e3)], None)],
  {"V": [(("I", "R"), "v.I*v.R"), (("P", "I"), "v.P/v.I"), (("P", "R"), "Math.sqrt(v.P*v.R)")],
   "I": [(("V", "R"), "v.V/v.R"), (("P", "V"), "v.P/v.V"), (("P", "R"), "Math.sqrt(v.P/v.R)")],
   "R": [(("V", "I"), "v.V/v.I"), (("V", "P"), "v.V*v.V/v.P"), (("P", "I"), "v.P/(v.I*v.I)")],
   "P": [(("V", "I"), "v.V*v.I"), (("V", "R"), "v.V*v.V/v.R"), (("I", "R"), "v.I*v.I*v.R")]}, need=2,
  formula="V = I x R and P = V x I. Enter any two of voltage, current, resistance and power to solve the other two.",
  title="Ohm's Law Calculator", desc="Enter any two of voltage, current, resistance and power and get the others.")

E("watts-amps-volts-calculator",
  [("P", "Power", [("W", 1), ("kW", 1e3)], 1800), ("V", "Voltage", VOLT, 120), ("I", "Current", AMP, None), ("pf", "Power factor (1 for DC)", None, 1)],
  {"P": "v.V*v.I*v.pf", "V": "v.P/(v.I*v.pf)", "I": "v.P/(v.V*v.pf)", "pf": "v.P/(v.V*v.I)"}, need=3,
  formula="Real power P = V x I x power factor. For DC circuits the power factor is 1. Enter any three values.",
  title="Watts, Amps and Volts Calculator", desc="Convert between watts, amps, volts and power factor for DC and AC circuits.")

E("led-resistor-calculator",
  [("R", "Resistor", OHM, None), ("vs", "Supply voltage (V)", None, 5), ("vf", "LED forward voltage (V)", None, 2), ("I", "LED current", [("mA", 1e-3), ("A", 1)], 20)],
  {"R": "(v.vs-v.vf)/v.I", "vs": "v.vf+v.R*v.I", "vf": "v.vs-v.R*v.I", "I": "(v.vs-v.vf)/v.R"}, need=3,
  extra="return [['Resistor power',N((v.vs-v.vf)*v.I*1000,1)+' mW']];",
  formula="R = (Vsupply - Vforward) / I. Enter any three of the four values.",
  title="LED Resistor Calculator", desc="Solve the resistor, supply voltage, LED voltage or current from any three values.")

E("capacitor-energy-calculator",
  [("E", "Stored energy", [("J", 1), ("mJ", 1e-3)], None), ("C", "Capacitance", FARAD, 470), ("V", "Voltage (V)", None, 25)],
  {"E": ".5*v.C*v.V*v.V", "C": "2*v.E/(v.V*v.V)", "V": "Math.sqrt(2*v.E/v.C)"},
  extra="return [['Charge',N(v.C*v.V*1000,4)+' mC']];",
  formula="E = 1/2 x C x V squared. Enter any two of energy, capacitance and voltage.",
  title="Capacitor Energy Calculator", desc="Enter any two of energy, capacitance and voltage and get the third.")

E("rc-time-constant-calculator",
  [("tau", "Time constant τ", [("ms", 1e-3), ("s", 1), ("µs", 1e-6)], None), ("R", "Resistance", OHM[1:2] + OHM[:1] + OHM[2:], 10), ("C", "Capacitance", FARAD, 10)],
  three("R", "C", "tau", "v.R*v.C", "v.tau/v.C", "v.tau/v.R"),
  extra="return [['Cutoff frequency',N(1/(2*Math.PI*v.tau),3)+' Hz'],['99% charged after',N(4.605*v.tau*1000,3)+' ms']];",
  formula="τ = R x C. Enter any two of time constant, resistance and capacitance.",
  title="RC Time Constant Calculator", desc="Enter any two of time constant, resistance and capacitance and get the third.")

E("electricity-cost-calculator",
  [("cost", "Cost ($)", None, None), ("watts", "Appliance power", [("W", 1), ("kW", 1000)], 1500), ("hours", "Hours of use", None, 8), ("price", "Electricity price ($ per kWh)", None, 0.16)],
  {"cost": "v.watts/1000*v.hours*v.price", "watts": "v.cost*1000/(v.hours*v.price)", "hours": "v.cost*1000/(v.watts*v.price)", "price": "v.cost*1000/(v.watts*v.hours)"}, need=3,
  extra="return [['Energy used',N(v.watts/1000*v.hours,3)+' kWh'],['If used this many hours every day: per month',M(v.cost*30)],['Per year',M(v.cost*365)]];",
  formula="Cost = kW x hours x price per kWh. Enter any three of the four values.",
  title="Electricity Cost Calculator", desc="Solve cost, power, hours or electricity price from any three values.")

# ======================= gas, heat, chemistry =======================
E("boyles-law-calculator",
  [("P1", "Initial pressure", PRESS, 100), ("V1", "Initial volume", VOL, 5), ("P2", "Final pressure", PRESS, 250), ("V2", "Final volume", VOL, None)],
  {"V2": "v.P1*v.V1/v.P2", "P1": "v.P2*v.V2/v.V1", "V1": "v.P2*v.V2/v.P1", "P2": "v.P1*v.V1/v.V2"}, need=3,
  formula="Boyle's law: P1 x V1 = P2 x V2 at constant temperature. Enter any three of the four values.",
  title="Boyle's Law Calculator", desc="Solve pressure or volume of a gas at constant temperature from any three values.")

E("charles-law-calculator",
  [("V1", "Initial volume", VOL, 10), ("T1", "Initial temperature", TEMP, 20), ("V2", "Final volume", VOL, None), ("T2", "Final temperature", TEMP, 80)],
  {"V2": "v.V1*v.T2/v.T1", "V1": "v.V2*v.T1/v.T2", "T1": "v.V1*v.T2/v.V2", "T2": "v.V2*v.T1/v.V1"}, need=3,
  formula="Charles's law: V1 / T1 = V2 / T2 with temperature in kelvin (the calculator converts for you). Enter any three values.",
  title="Charles's Law Calculator", desc="Solve gas volume or temperature at constant pressure from any three values.")

E("ideal-gas-law-calculator",
  [("P", "Pressure", PRESS[2:3] + PRESS[:2] + PRESS[3:], 1), ("V", "Volume", VOL, None), ("n", "Moles of gas", None, 1), ("T", "Temperature", TEMP, 0)],
  {"P": "v.n*8.314462618*v.T/v.V", "V": "v.n*8.314462618*v.T/v.P", "n": "v.P*v.V/(8.314462618*v.T)", "T": "v.P*v.V/(v.n*8.314462618)"}, need=3,
  formula="Ideal gas law: PV = nRT with R = 8.314462618 J/(mol·K). Enter any three of pressure, volume, moles and temperature.",
  title="Ideal Gas Law Calculator", desc="Solve pressure, volume, moles or temperature from any three values.")

E("specific-heat-calculator",
  [("Q", "Heat energy", ENERGY[:4], None), ("m", "Mass", MASS[1:2] + MASS[:1] + MASS[2:], 500), ("c", "Specific heat", [("J/(g·°C)", 1000), ("J/(kg·K)", 1), ("cal/(g·°C)", 4184)], 4.186), ("dT", "Temperature change", [("°C", 1), ("°F", 5 / 9)], 40)],
  {"Q": "v.m*v.c*v.dT", "m": "v.Q/(v.c*v.dT)", "c": "v.Q/(v.m*v.dT)", "dT": "v.Q/(v.m*v.c)"}, need=3,
  formula="Q = m x c x ΔT. Water has a specific heat of 4.186 J/(g·°C). Enter any three of the four values.",
  title="Specific Heat Calculator", desc="Solve heat energy, mass, specific heat or temperature change from any three values.")

E("density-calculator",
  [("rho", "Density", [("g/cm³", 1000), ("kg/m³", 1), ("lb/ft³", 16.01846337)], None), ("m", "Mass", MASS[1:2] + MASS[:1] + MASS[2:], 500), ("V", "Volume", [("cm³", 1e-6), ("L", .001), ("mL", 1e-6), ("m³", 1), ("ft³", .028316846592), ("gal", .003785411784)], 250)],
  three("m", "V", "rho", "v.m/v.V", "v.rho*v.V", "v.m/v.rho"),
  extra="return [['Specific gravity (water = 1)',N(v.rho/1000,4)]];",
  formula="Density = mass / volume. Enter any two of density, mass and volume.",
  title="Density Calculator", desc="Enter any two of density, mass and volume and get the third.")

E("mole-calculator",
  [("n", "Moles (mol)", None, None), ("m", "Mass (g)", None, 36), ("M", "Molar mass (g/mol)", None, 18.015)],
  three("m", "M", "n", "v.m/v.M", "v.n*v.M", "v.m/v.n"),
  extra="return [['Particles',(v.n*6.02214076e23).toExponential(4)]];",
  formula="Moles n = mass / molar mass. One mole contains 6.02214076 x 10^23 particles.",
  title="Mole Calculator (Grams to Moles)", desc="Enter any two of moles, mass and molar mass and get the third.")

E("percent-yield-calculator",
  [("y", "Percent yield (%)", None, None), ("act", "Actual yield", None, 8.2), ("theo", "Theoretical yield", None, 10.5)],
  three("act", "theo", "y", "v.act/v.theo*100", "v.y*v.theo/100", "v.act*100/v.y"),
  formula="Percent yield = actual yield / theoretical yield x 100. Enter any two values.",
  title="Percent Yield Calculator", desc="Enter any two of percent yield, actual yield and theoretical yield and get the third.")

E("dilution-calculator",
  [("c1", "Stock concentration C1", None, 10), ("v1", "Stock volume needed V1", None, None), ("c2", "Final concentration C2", None, 2), ("v2", "Final volume V2", None, 100)],
  {"v1": "v.c2*v.v2/v.c1", "c1": "v.c2*v.v2/v.v1", "c2": "v.c1*v.v1/v.v2", "v2": "v.c1*v.v1/v.c2"}, need=3,
  extra="return [['Diluent to add',N(v.v2-v.v1,4)+' (same volume unit)']];",
  formula="C1 x V1 = C2 x V2. Enter any three of the four values (use consistent units for each pair).",
  title="Dilution Calculator (C1V1 = C2V2)", desc="Solve a concentration or volume for a dilution from any three values.")

E("ph-calculator",
  [("ph", "pH", None, 7), ("H", "[H+] concentration (mol/L)", None, None), ("poh", "pOH", None, None), ("OH", "[OH-] concentration (mol/L)", None, None)],
  {"ph": [(("H",), "-Math.log10(v.H)"), (("poh",), "14-v.poh")], "H": [(("ph",), "Math.pow(10,-v.ph)")],
   "poh": [(("OH",), "-Math.log10(v.OH)"), (("ph",), "14-v.ph")], "OH": [(("poh",), "Math.pow(10,-v.poh)")]}, need=1,
  extra="return [['Solution is',v.ph<7?'Acidic':v.ph>7?'Basic':'Neutral']];",
  formula="pH = -log10[H+] and pH + pOH = 14 at 25 °C. Enter any one value.",
  title="pH Calculator", desc="Convert between pH, pOH and ion concentration.")

# ======================= geometry =======================
E("pythagorean-theorem-calculator",
  [("a", "Side a", None, 3), ("b", "Side b", None, 4), ("c", "Hypotenuse c", None, None)],
  {"c": "Math.sqrt(v.a*v.a+v.b*v.b)", "a": "Math.sqrt(v.c*v.c-v.b*v.b)", "b": "Math.sqrt(v.c*v.c-v.a*v.a)"},
  extra="var A=Math.atan2(v.a,v.b)*180/Math.PI;return [['Area',N(v.a*v.b/2,4)],['Perimeter',N(v.a+v.b+v.c,4)],['Angle A',N(A,3)+' degrees'],['Angle B',N(90-A,3)+' degrees']];",
  formula="a squared + b squared = c squared. Enter any two sides of a right triangle to find the third.",
  title="Pythagorean Theorem Calculator", desc="Enter any two sides of a right triangle and get the third, plus area and angles.")

E("circle-calculator",
  [("r", "Radius", None, 5), ("d", "Diameter", None, None), ("C", "Circumference", None, None), ("A", "Area", None, None)],
  {"r": [(("d",), "v.d/2"), (("C",), "v.C/(2*Math.PI)"), (("A",), "Math.sqrt(v.A/Math.PI)")], "d": [(("r",), "2*v.r")],
   "C": [(("r",), "2*Math.PI*v.r")], "A": [(("r",), "Math.PI*v.r*v.r")]}, need=1,
  formula="C = 2 x pi x r and A = pi x r squared. Enter any one of radius, diameter, circumference or area.",
  title="Circle Calculator", desc="Enter any one of radius, diameter, circumference or area and get the rest.")

E("rectangle-calculator",
  [("l", "Length", LEN[5:6] + LEN[:5], 12), ("w", "Width", LEN[5:6] + LEN[:5], 8), ("A", "Area", [("ft²", .09290304), ("m²", 1), ("cm²", 1e-4), ("in²", .00064516)], None)],
  three("l", "w", "A", "v.l*v.w", "v.A/v.w", "v.A/v.l"),
  extra="return [['Perimeter',N(2*(v.l+v.w)/.3048,3)+' ft ('+N(2*(v.l+v.w),3)+' m)'],['Diagonal',N(Math.hypot(v.l,v.w)/.3048,3)+' ft ('+N(Math.hypot(v.l,v.w),3)+' m)']];",
  formula="Area = length x width. Enter any two of length, width and area.",
  title="Rectangle Calculator", desc="Enter any two of length, width and area and get the third, plus perimeter and diagonal.")

E("sphere-volume-calculator",
  [("r", "Radius", None, 5), ("V", "Volume", None, None), ("S", "Surface area", None, None)],
  {"r": [(("V",), "Math.cbrt(3*v.V/(4*Math.PI))"), (("S",), "Math.sqrt(v.S/(4*Math.PI))")], "V": [(("r",), "4/3*Math.PI*v.r*v.r*v.r")], "S": [(("r",), "4*Math.PI*v.r*v.r")]}, need=1,
  formula="V = 4/3 x pi x r cubed and surface area = 4 x pi x r squared. Enter any one of radius, volume or surface area.",
  title="Sphere Volume and Surface Area Calculator", desc="Enter any one of radius, volume or surface area of a sphere and get the rest.")

E("cylinder-volume-calculator",
  [("r", "Radius", None, 3), ("h", "Height", None, 10), ("V", "Volume", None, None)],
  {"V": "Math.PI*v.r*v.r*v.h", "h": "v.V/(Math.PI*v.r*v.r)", "r": "Math.sqrt(v.V/(Math.PI*v.h))"},
  extra="return [['Lateral surface area',N(2*Math.PI*v.r*v.h,4)],['Total surface area',N(2*Math.PI*v.r*(v.r+v.h),4)]];",
  formula="V = pi x r squared x h. Enter any two of radius, height and volume.",
  title="Cylinder Volume and Surface Area Calculator", desc="Enter any two of radius, height and volume of a cylinder and get the third.")

E("cone-volume-calculator",
  [("r", "Base radius", None, 4), ("h", "Height", None, 9), ("V", "Volume", None, None)],
  {"V": "Math.PI*v.r*v.r*v.h/3", "h": "3*v.V/(Math.PI*v.r*v.r)", "r": "Math.sqrt(3*v.V/(Math.PI*v.h))"},
  extra="var s=Math.hypot(v.r,v.h);return [['Slant height',N(s,4)],['Total surface area',N(Math.PI*v.r*(v.r+s),4)]];",
  formula="V = pi x r squared x h / 3. Enter any two of radius, height and volume.",
  title="Cone Volume and Surface Area Calculator", desc="Enter any two of radius, height and volume of a cone and get the third.")

E("cube-calculator",
  [("s", "Side length", None, 5), ("V", "Volume", None, None), ("S", "Surface area", None, None)],
  {"s": [(("V",), "Math.cbrt(v.V)"), (("S",), "Math.sqrt(v.S/6)")], "V": [(("s",), "v.s*v.s*v.s")], "S": [(("s",), "6*v.s*v.s")]}, need=1,
  extra="return [['Face diagonal',N(v.s*Math.SQRT2,4)],['Space diagonal',N(v.s*Math.sqrt(3),4)]];",
  formula="V = s cubed and surface area = 6 x s squared. Enter any one of side, volume or surface area.",
  title="Cube Volume and Diagonal Calculator", desc="Enter any one of side, volume or surface area of a cube and get the rest.")

E("trapezoid-area-calculator",
  [("a", "Parallel side a", None, 8), ("b", "Parallel side b", None, 5), ("h", "Height", None, 4), ("A", "Area", None, None)],
  {"A": "(v.a+v.b)/2*v.h", "h": "2*v.A/(v.a+v.b)", "a": "2*v.A/v.h-v.b", "b": "2*v.A/v.h-v.a"}, need=3,
  formula="Area = (a + b) / 2 x h. Enter any three of the four values.",
  title="Trapezoid Area Calculator", desc="Solve the area, height or a parallel side of a trapezoid from any three values.")

E("proportion-calculator",
  [("a", "A", None, 3), ("b", "B", None, 4), ("c", "C", None, 9), ("d", "D", None, None)],
  {"d": "v.b*v.c/v.a", "a": "v.b*v.c/v.d", "b": "v.a*v.d/v.c", "c": "v.a*v.d/v.b"}, need=3,
  formula="A / B = C / D. Enter any three values and the fourth is found by cross-multiplication.",
  title="Proportion Calculator", desc="Solve A/B = C/D for any missing value.")

E("aspect-ratio-calculator",
  [("w1", "Original width", None, 1920), ("h1", "Original height", None, 1080), ("w2", "New width", None, 1280), ("h2", "New height", None, None)],
  {"h2": "v.h1*v.w2/v.w1", "w2": "v.w1*v.h2/v.h1", "w1": "v.w2*v.h1/v.h2", "h1": "v.w1*v.h2/v.w2"}, need=3,
  extra="var g=function(a,b){return b?g(b,a%b):a;};var d=g(Math.round(v.w1),Math.round(v.h1));return [['Aspect ratio',Math.round(v.w1)/d+':'+Math.round(v.h1)/d],['Decimal',N(v.w1/v.h1,4)]];",
  formula="Keeping the ratio width : height constant, new height = original height x new width / original width. Enter any three values.",
  title="Aspect Ratio Calculator", desc="Scale an image or screen: enter any three of the four dimensions and get the fourth.")

E("ppi-calculator",
  [("ppi", "Pixel density (PPI)", None, None), ("w", "Width (pixels)", None, 2560), ("h", "Height (pixels)", None, 1440), ("d", "Diagonal (inches)", None, 27)],
  {"ppi": "Math.hypot(v.w,v.h)/v.d", "d": "Math.hypot(v.w,v.h)/v.ppi", "w": "Math.sqrt(v.ppi*v.ppi*v.d*v.d-v.h*v.h)", "h": "Math.sqrt(v.ppi*v.ppi*v.d*v.d-v.w*v.w)"}, need=3,
  extra="var dg=Math.hypot(v.w,v.h);return [['Physical width',N(v.d*v.w/dg,2)+' in'],['Physical height',N(v.d*v.h/dg,2)+' in'],['Total pixels',N(v.w*v.h,0)]];",
  formula="PPI = sqrt(width squared + height squared) / diagonal. Enter any three values.",
  title="PPI Calculator (Pixel Density)", desc="Solve pixel density, resolution or screen size from any three values.")

E("download-time-calculator",
  [("size", "File size", [("GB", 1e9), ("MB", 1e6), ("TB", 1e12), ("KB", 1e3)], 5), ("sp", "Connection speed", [("Mbps", 125000), ("Gbps", 1.25e8), ("Kbps", 125), ("MB/s", 1e6)], 100), ("time", "Time", [("min", 60), ("s", 1), ("h", 3600)], None)],
  {"time": "v.size/v.sp", "size": "v.sp*v.time", "sp": "v.size/v.time"},
  formula="Time = file size / speed. Speeds in megabits per second are divided by 8 to give megabytes per second. Real downloads are usually 5-10% slower because of overhead.",
  title="Download Time Calculator", desc="Enter any two of file size, speed and time and get the third.")

E("bmi-calculator",
  [("bmi", "BMI (kg/m²)", None, None), ("w", "Weight", MASS[:1] + MASS[2:3], 70), ("h", "Height", [("cm", .01), ("m", 1), ("in", .0254), ("ft", .3048)], 175)],
  {"bmi": "v.w/(v.h*v.h)", "w": "v.bmi*v.h*v.h", "h": "Math.sqrt(v.w/v.bmi)"},
  extra="var b=v.bmi;return [['Category',b<18.5?'Underweight':b<25?'Healthy weight':b<30?'Overweight':'Obese'],['Healthy weight range for this height',N(18.5*v.h*v.h,1)+' - '+N(24.9*v.h*v.h,1)+' kg ('+N(18.5*v.h*v.h*2.2046,0)+' - '+N(24.9*v.h*v.h*2.2046,0)+' lb)']];",
  formula="BMI = weight (kg) / height (m) squared. Leave the BMI blank to calculate it, or enter a target BMI and a height to find the matching weight.",
  title="BMI Calculator", desc="Calculate BMI from weight and height, or find the weight or height for a target BMI.")

# ======================= money & percentages =======================
E("percentage-calculator",
  [("p", "Percentage (%)", None, 15), ("y", "Of this number", None, 200), ("z", "Result", None, None)],
  {"z": "v.p*v.y/100", "y": "v.z*100/v.p", "p": "v.z/v.y*100"},
  formula="Result = percentage / 100 x number. Enter any two: find a percentage of a number, what percent one number is of another, or the number from a known percentage.",
  title="Percentage Calculator", desc="Find X% of Y, what percent one number is of another, or the whole from a part and a percent.")

E("percent-change-calculator",
  [("old", "Old value", None, 80), ("nw", "New value", None, 100), ("ch", "Change (%)", None, None)],
  {"ch": "(v.nw/v.old-1)*100", "nw": "v.old*(1+v.ch/100)", "old": "v.nw/(1+v.ch/100)"},
  extra="return [['Difference',N(v.nw-v.old,4)]];",
  formula="Percent change = (new - old) / old x 100. Enter any two of old value, new value and percent change.",
  title="Percent Change Calculator", desc="Enter any two of old value, new value and percent change and get the third.")

E("discount-calculator",
  [("orig", "Original price ($)", None, 120), ("d", "Discount (%)", None, 25), ("sale", "Sale price ($)", None, None)],
  {"sale": "v.orig*(1-v.d/100)", "orig": "v.sale/(1-v.d/100)", "d": "(1-v.sale/v.orig)*100"},
  extra="return [['You save',M(v.orig-v.sale)]];",
  formula="Sale price = original price x (1 - discount%). Enter any two of original price, discount and sale price.",
  title="Discount Calculator", desc="Enter any two of original price, discount % and sale price and get the third.")

E("sales-tax-calculator",
  [("pre", "Price before tax ($)", None, 100), ("rate", "Sales tax rate (%)", None, 8.25), ("tot", "Total with tax ($)", None, None)],
  {"tot": "v.pre*(1+v.rate/100)", "pre": "v.tot/(1+v.rate/100)", "rate": "(v.tot/v.pre-1)*100"},
  extra="return [['Sales tax',M(v.tot-v.pre)]];",
  formula="Total = price x (1 + tax rate). Enter any two of price, rate and total to add tax, remove tax from a total, or find the rate.",
  title="Sales Tax Calculator", desc="Add sales tax, remove it from a total, or find the tax rate from any two values.")

E("vat-calculator",
  [("net", "Price excluding VAT", None, 100), ("rate", "VAT rate (%)", None, 20), ("gross", "Price including VAT", None, None)],
  {"gross": "v.net*(1+v.rate/100)", "net": "v.gross/(1+v.rate/100)", "rate": "(v.gross/v.net-1)*100"},
  extra="return [['VAT amount',N(v.gross-v.net,2)]];",
  formula="Gross = net x (1 + VAT rate). Enter any two of net, rate and gross to add VAT, remove VAT, or find the rate.",
  title="VAT Calculator", desc="Add or remove VAT, or find the rate, from any two values.")

E("gst-calculator",
  [("net", "Price excluding GST", None, 100), ("rate", "GST rate (%)", None, 10), ("gross", "Price including GST", None, None)],
  {"gross": "v.net*(1+v.rate/100)", "net": "v.gross/(1+v.rate/100)", "rate": "(v.gross/v.net-1)*100"},
  extra="return [['GST amount',N(v.gross-v.net,2)]];",
  formula="Gross = net x (1 + GST rate). Enter any two of net, rate and gross.",
  title="GST Calculator", desc="Add or remove GST, or find the rate, from any two values.")

E("simple-interest-calculator",
  [("I", "Interest earned ($)", None, None), ("P", "Principal ($)", None, 5000), ("r", "Annual rate (%)", None, 4.5), ("t", "Time", [("years", 1), ("months", 1 / 12)], 3)],
  {"I": "v.P*v.r*v.t/100", "P": "v.I*100/(v.r*v.t)", "r": "v.I*100/(v.P*v.t)", "t": "v.I*100/(v.P*v.r)"}, need=3,
  extra="return [['Total amount',M(v.P+v.I)]];",
  formula="Simple interest I = P x r x t. Enter any three of the four values.",
  title="Simple Interest Calculator", desc="Solve interest, principal, rate or time from any three values.")

E("salary-calculator",
  [("annual", "Annual pay ($)", None, None), ("hourly", "Hourly rate ($)", None, 25), ("hrs", "Hours per week", None, 40), ("wks", "Weeks per year", None, 52)],
  {"annual": "v.hourly*v.hrs*v.wks", "hourly": "v.annual/(v.hrs*v.wks)", "hrs": "v.annual/(v.hourly*v.wks)", "wks": "v.annual/(v.hourly*v.hrs)"}, need=3,
  extra="return [['Monthly',M(v.annual/12)],['Biweekly',M(v.annual/26)],['Weekly',M(v.annual/v.wks)],['Daily (5 days)',M(v.annual/v.wks/5)]];",
  formula="Annual pay = hourly rate x hours per week x weeks per year. Enter any three values, for example an annual salary, hours and weeks to find the hourly wage.",
  title="Salary Calculator (Hourly to Annual and Back)", desc="Convert hourly pay to annual salary, or annual salary to an hourly rate.")

E("fuel-cost-calculator",
  [("cost", "Fuel cost ($)", None, None), ("dist", "Distance (miles)", None, 300), ("mpg", "Fuel economy (mpg)", None, 28), ("price", "Price per gallon ($)", None, 3.5)],
  {"cost": "v.dist/v.mpg*v.price", "dist": "v.cost*v.mpg/v.price", "mpg": "v.dist*v.price/v.cost", "price": "v.cost*v.mpg/v.dist"}, need=3,
  extra="return [['Gallons needed',N(v.dist/v.mpg,2)],['Cost per mile',M(v.cost/v.dist)]];",
  formula="Cost = distance / mpg x price per gallon. Enter any three of the four values.",
  title="Fuel Cost Calculator", desc="Solve trip fuel cost, distance, mpg or fuel price from any three values.")

E("mpg-calculator",
  [("mpg", "Fuel economy (mpg)", None, None), ("mi", "Distance (miles)", None, 350), ("gal", "Fuel used (gallons)", None, 12.5)],
  three("mi", "gal", "mpg", "v.mi/v.gal", "v.mpg*v.gal", "v.mi/v.mpg"),
  extra="return [['Liters per 100 km',N(235.215/v.mpg,2)],['Kilometers per liter',N(v.mpg*.425144,3)]];",
  formula="mpg = miles / gallons. Enter any two of mpg, miles and gallons.",
  title="MPG Calculator", desc="Enter any two of mpg, miles driven and gallons used and get the third.")

E("temperature-converter",
  [("c", "Celsius (°C)", None, 100), ("f", "Fahrenheit (°F)", None, None), ("k", "Kelvin (K)", None, None)],
  {"c": [(("f",), "(v.f-32)*5/9"), (("k",), "v.k-273.15")], "f": [(("c",), "v.c*9/5+32")], "k": [(("c",), "v.c+273.15")]}, need=1,
  formula="°F = °C x 9/5 + 32 and K = °C + 273.15. Type a temperature in any box and the other two update.",
  title="Temperature Converter (Celsius, Fahrenheit, Kelvin)", desc="Convert between Celsius, Fahrenheit and Kelvin: type in any box.")

# ======================= duplicates removed =======================
DELETE = [
    "circumference-calculator",      # same as circle-calculator
    "right-triangle-calculator",     # covered by pythagorean-theorem-calculator
    "met-calories-calculator",       # duplicate of calories-burned-calculator
    "heart-rate-zones-calculator",   # duplicate of heart-rate-calculator
    "target-weight-date-calculator", # duplicate of weight-loss-calculator
    "extra-payment-loan-calculator", # duplicate of mortgage-payoff-calculator
    "work-hours-calculator",         # duplicate of time-duration-calculator
    "bill-split-calculator",         # duplicate of tip-calculator (which splits bills)
    "pace-converter",                # covered by two-way pace-calculator
    "salary-to-hourly-calculator",   # covered by two-way salary-calculator
    "reverse-sales-tax-calculator",  # covered by two-way sales-tax-calculator
    "markup-calculator",             # covered by two-way margin-calculator
    "margin-to-markup-calculator",   # covered by two-way margin-calculator
]

E("margin-calculator",
  [("cost", "Cost ($)", None, 60), ("price", "Selling price ($)", None, None), ("margin", "Profit margin (%)", None, None), ("mk", "Markup (%)", None, 25)],
  {"price": [(("cost", "mk"), "v.cost*(1+v.mk/100)"), (("cost", "margin"), "v.cost/(1-v.margin/100)")],
   "cost": [(("price", "mk"), "v.price/(1+v.mk/100)"), (("price", "margin"), "v.price*(1-v.margin/100)")],
   "margin": [(("cost", "price"), "(v.price-v.cost)/v.price*100"), (("mk",), "v.mk/(1+v.mk/100)")],
   "mk": [(("cost", "price"), "(v.price/v.cost-1)*100"), (("margin",), "v.margin/(1-v.margin/100)")]}, need=2,
  extra="return [['Profit',M(v.price-v.cost)]];",
  formula="Margin = profit / price and markup = profit / cost. Enter any two of cost, price, margin and markup (for example margin alone with cost) to solve the rest.",
  title="Profit Margin and Markup Calculator", desc="Convert between cost, price, margin and markup: enter any two and get the others.")
