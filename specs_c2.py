from spec import C
import json

# --- Unit conversion pair pages, generated from unit tables -------------------------
# (key, plural name, abbreviation, singular name, factor to base)
TABLES = {
 "length": ("m", [
  ("mm", "millimeters", "mm", "millimeter", .001), ("cm", "centimeters", "cm", "centimeter", .01), ("m", "meters", "m", "meter", 1),
  ("km", "kilometers", "km", "kilometer", 1000), ("in", "inches", "in", "inch", .0254), ("ft", "feet", "ft", "foot", .3048),
  ("yd", "yards", "yd", "yard", .9144), ("mi", "miles", "mi", "mile", 1609.344)]),
 "mass": ("kg", [
  ("mg", "milligrams", "mg", "milligram", 1e-6), ("g", "grams", "g", "gram", .001), ("kg", "kilograms", "kg", "kilogram", 1),
  ("oz", "ounces", "oz", "ounce", .028349523125), ("lb", "pounds", "lb", "pound", .45359237), ("st", "stone", "st", "stone", 6.35029318),
  ("t", "metric tons", "t", "metric ton", 1000)]),
 "volume": ("l", [
  ("ml", "milliliters", "ml", "milliliter", .001), ("l", "liters", "L", "liter", 1), ("tsp", "teaspoons", "tsp", "teaspoon", .00492892159375),
  ("tbsp", "tablespoons", "tbsp", "tablespoon", .01478676478125), ("floz", "fluid ounces", "fl oz", "fluid ounce", .0295735295625),
  ("cup", "cups", "cup", "cup", .2365882365), ("pt", "pints", "pt", "pint", .473176473), ("qt", "quarts", "qt", "quart", .946352946),
  ("gal", "gallons", "gal", "gallon", 3.785411784)]),
 "area": ("m2", [
  ("sqin", "square inches", "in²", "square inch", .00064516), ("sqft", "square feet", "ft²", "square foot", .09290304),
  ("sqyd", "square yards", "yd²", "square yard", .83612736), ("sqm", "square meters", "m²", "square meter", 1),
  ("acre", "acres", "acres", "acre", 4046.8564224), ("ha", "hectares", "ha", "hectare", 10000), ("sqkm", "square kilometers", "km²", "square kilometer", 1e6)]),
 "speed": ("mps", [
  ("mph", "miles per hour", "mph", "mile per hour", .44704), ("kph", "kilometers per hour", "km/h", "kilometer per hour", 1 / 3.6),
  ("mps", "meters per second", "m/s", "meter per second", 1), ("knot", "knots", "kn", "knot", 1852 / 3600), ("fps", "feet per second", "ft/s", "foot per second", .3048)]),
 "time": ("s", [
  ("s", "seconds", "s", "second", 1), ("min", "minutes", "min", "minute", 60), ("h", "hours", "h", "hour", 3600), ("day", "days", "days", "day", 86400),
  ("week", "weeks", "weeks", "week", 604800), ("month", "months", "months", "month", 2629746), ("year", "years", "years", "year", 31556952)]),
 "data": ("B", [
  ("B", "bytes", "B", "byte", 1), ("KB", "kilobytes", "KB", "kilobyte", 1e3), ("MB", "megabytes", "MB", "megabyte", 1e6),
  ("GB", "gigabytes", "GB", "gigabyte", 1e9), ("TB", "terabytes", "TB", "terabyte", 1e12)]),
 "pressure": ("Pa", [
  ("Pa", "pascals", "Pa", "pascal", 1), ("kPa", "kilopascals", "kPa", "kilopascal", 1000), ("bar", "bar", "bar", "bar", 1e5),
  ("psi", "psi", "psi", "psi", 6894.757293168), ("atm", "atmospheres", "atm", "atmosphere", 101325), ("mmHg", "mmHg", "mmHg", "mmHg", 133.322387415)]),
 "energy": ("J", [
  ("J", "joules", "J", "joule", 1), ("kJ", "kilojoules", "kJ", "kilojoule", 1000), ("cal", "calories", "cal", "calorie", 4.184),
  ("kcal", "kilocalories", "kcal", "kilocalorie", 4184), ("Wh", "watt hours", "Wh", "watt hour", 3600), ("kWh", "kilowatt hours", "kWh", "kilowatt hour", 3.6e6),
  ("BTU", "BTU", "BTU", "BTU", 1055.05585262)]),
 "power": ("W", [
  ("W", "watts", "W", "watt", 1), ("kW", "kilowatts", "kW", "kilowatt", 1000), ("hp", "horsepower", "hp", "horsepower", 745.69987158),
  ("BTUh", "BTU per hour", "BTU/h", "BTU per hour", 0.29307107)]),
 "force": ("N", [
  ("N", "newtons", "N", "newton", 1), ("kN", "kilonewtons", "kN", "kilonewton", 1000), ("lbf", "pound-force", "lbf", "pound-force", 4.4482216152605),
  ("kgf", "kilogram-force", "kgf", "kilogram-force", 9.80665)]),
 "angle": ("rad", [
  ("deg", "degrees", "°", "degree", 3.141592653589793 / 180), ("rad", "radians", "rad", "radian", 1), ("grad", "gradians", "grad", "gradian", 3.141592653589793 / 200)]),
}


TABLES["length"][1].extend([
  ("nm", "nanometers", "nm", "nanometer", 1e-9), ("um", "micrometers", "µm", "micrometer", 1e-6), ("nmi", "nautical miles", "nmi", "nautical mile", 1852),
  ("furlong", "furlongs", "furlongs", "furlong", 201.168), ("mil", "mils", "mil", "mil", 2.54e-5), ("ly", "light years", "ly", "light year", 9.4607304725808e15),
  ("fathom", "fathoms", "fathoms", "fathom", 1.8288)])
TABLES["mass"][1].extend([
  ("ug", "micrograms", "µg", "microgram", 1e-9), ("ct", "carats", "ct", "carat", 2e-4), ("gr", "grains", "gr", "grain", 6.479891e-5),
  ("ston", "short tons", "short tons", "short ton", 907.18474), ("lton", "long tons", "long tons", "long ton", 1016.0469088), ("slug", "slugs", "slugs", "slug", 14.59390294)])
TABLES["volume"][1].extend([
  ("m3", "cubic meters", "m³", "cubic meter", 1000), ("cm3", "cubic centimeters", "cm³", "cubic centimeter", .001), ("cuin", "cubic inches", "in³", "cubic inch", .016387064),
  ("cuft", "cubic feet", "ft³", "cubic foot", 28.316846592), ("cuyd", "cubic yards", "yd³", "cubic yard", 764.554857984),
  ("igal", "imperial gallons", "imp gal", "imperial gallon", 4.54609), ("iqt", "imperial quarts", "imp qt", "imperial quart", 1.1365225),
  ("ipt", "imperial pints", "imp pt", "imperial pint", .56826125), ("bbl", "oil barrels", "bbl", "oil barrel", 158.987294928)])
TABLES["area"][1].extend([
  ("sqmm", "square millimeters", "mm²", "square millimeter", 1e-6), ("sqcm", "square centimeters", "cm²", "square centimeter", 1e-4),
  ("sqmi", "square miles", "mi²", "square mile", 2589988.110336)])
TABLES["speed"][1].extend([
  ("mach", "mach", "Mach", "Mach", 340.29), ("cms", "centimeters per second", "cm/s", "centimeter per second", .01),
  ("kmps", "kilometers per second", "km/s", "kilometer per second", 1000)])
TABLES["time"][1].extend([
  ("ms", "milliseconds", "ms", "millisecond", 1e-3), ("us", "microseconds", "µs", "microsecond", 1e-6), ("ns", "nanoseconds", "ns", "nanosecond", 1e-9),
  ("decade", "decades", "decades", "decade", 315569520), ("century", "centuries", "centuries", "century", 3155695200)])
TABLES["data"][1].extend([
  ("bit", "bits", "bits", "bit", .125), ("Kbit", "kilobits", "Kb", "kilobit", 125), ("Mbit", "megabits", "Mb", "megabit", 125000), ("Gbit", "gigabits", "Gb", "gigabit", 1.25e8),
  ("PB", "petabytes", "PB", "petabyte", 1e15), ("KiB", "kibibytes", "KiB", "kibibyte", 1024), ("MiB", "mebibytes", "MiB", "mebibyte", 1048576),
  ("GiB", "gibibytes", "GiB", "gibibyte", 1073741824), ("TiB", "tebibytes", "TiB", "tebibyte", 1099511627776)])
TABLES["pressure"][1].extend([
  ("torr", "torr", "Torr", "torr", 133.322368421), ("inHg", "inches of mercury", "inHg", "inch of mercury", 3386.389),
  ("MPa", "megapascals", "MPa", "megapascal", 1e6), ("mbar", "millibars", "mbar", "millibar", 100)])
TABLES["energy"][1].extend([
  ("MJ", "megajoules", "MJ", "megajoule", 1e6), ("GJ", "gigajoules", "GJ", "gigajoule", 1e9), ("therm", "therms", "therms", "therm", 105480400),
  ("ftlb", "foot-pounds", "ft-lb", "foot-pound", 1.3558179483314)])
TABLES["power"][1].extend([
  ("mW", "milliwatts", "mW", "milliwatt", 1e-3), ("MW", "megawatts", "MW", "megawatt", 1e6),
  ("ftlbs", "foot-pounds per second", "ft-lb/s", "foot-pound per second", 1.3558179483314), ("PS", "metric horsepower", "PS", "metric horsepower", 735.49875)])
TABLES["force"][1].extend([
  ("dyn", "dynes", "dyn", "dyne", 1e-5), ("ozf", "ounce-force", "ozf", "ounce-force", .27801385), ("kip", "kips", "kip", "kip", 4448.2216152605)])
TABLES["angle"][1].extend([
  ("amin", "arcminutes", "arcmin", "arcminute", 3.141592653589793 / 10800), ("asec", "arcseconds", "arcsec", "arcsecond", 3.141592653589793 / 648000),
  ("turn", "turns", "turns", "turn", 2 * 3.141592653589793)])
TABLES["frequency"] = ("Hz", [
  ("Hz", "hertz", "Hz", "hertz", 1), ("kHz", "kilohertz", "kHz", "kilohertz", 1e3), ("MHz", "megahertz", "MHz", "megahertz", 1e6),
  ("GHz", "gigahertz", "GHz", "gigahertz", 1e9), ("rpm", "revolutions per minute", "rpm", "revolution per minute", 1 / 60)])
TABLES["torque"] = ("Nm", [
  ("Nm", "newton meters", "N·m", "newton meter", 1), ("lbft", "pound-feet", "lb-ft", "pound-foot", 1.3558179483314),
  ("lbin", "pound-inches", "lb-in", "pound-inch", .1129848290276), ("kgfm", "kilogram-force meters", "kgf·m", "kilogram-force meter", 9.80665),
  ("ozin", "ounce-inches", "oz-in", "ounce-inch", .00706155176), ("Nmm", "newton millimeters", "N·mm", "newton millimeter", .001)])
TABLES["density"] = ("kgm3", [
  ("kgm3", "kilograms per cubic meter", "kg/m³", "kilogram per cubic meter", 1), ("gcm3", "grams per cubic centimeter", "g/cm³", "gram per cubic centimeter", 1000),
  ("lbft3", "pounds per cubic foot", "lb/ft³", "pound per cubic foot", 16.01846337), ("lbin3", "pounds per cubic inch", "lb/in³", "pound per cubic inch", 27679.9047),
  ("lbgal", "pounds per gallon", "lb/gal", "pound per gallon", 119.826427)])
TABLES["flow"] = ("m3s", [
  ("lpm", "liters per minute", "L/min", "liter per minute", 1 / 60000), ("gpm", "gallons per minute", "gal/min", "gallon per minute", 6.30901964e-5),
  ("m3h", "cubic meters per hour", "m³/h", "cubic meter per hour", 1 / 3600), ("cfm", "cubic feet per minute", "cfm", "cubic foot per minute", 4.719474432e-4),
  ("lps", "liters per second", "L/s", "liter per second", 1e-3), ("m3s", "cubic meters per second", "m³/s", "cubic meter per second", 1)])
TABLES["accel"] = ("mps2", [
  ("mps2", "meters per second squared", "m/s²", "meter per second squared", 1), ("g", "standard gravities", "g", "standard gravity", 9.80665),
  ("fps2", "feet per second squared", "ft/s²", "foot per second squared", .3048)])


def fmt(x):
    from decimal import Decimal
    if x == 0:
        return "0"
    if abs(x) < 1e-4 or abs(x) >= 1e15:
        return f"{x:.6g}"
    d = Decimal(f"{x:.8g}")
    s = format(d, "f")
    if "." in s:
        a, b = s.split(".")
        b = b.rstrip("0")
        return f"{int(a):,}" + ("." + b if b else "")
    return f"{int(s):,}"


def slugify(s):
    return s.lower().replace(" ", "-").replace("²", "2")


def tc(s):
    t = s.title().replace("Mmhg", "mmHg").replace("Btu", "BTU").replace(" Per ", " per ").replace("Psi", "PSI")
    return t


KIND_INFO = {
 "length": ("length", "length-converter", "Length measures the distance between two points. The meter is the SI base unit; inches, feet, yards and miles are US customary and imperial units, all defined exactly in terms of the meter (1 inch = 2.54 cm exactly)."),
 "mass": ("weight and mass", "weight-converter", "Mass measures the amount of matter in an object. The kilogram is the SI base unit; ounces, pounds and stone are customary units defined exactly in terms of the kilogram (1 lb = 0.45359237 kg)."),
 "volume": ("volume", "volume-converter", "Volume measures how much space a liquid or container holds. The liter is the common metric unit; gallons, quarts, pints, cups and spoons here are US customary units, which differ from imperial ones."),
 "area": ("area", "area-converter", "Area measures a flat surface. The square meter is the SI unit; square feet and acres are widely used for property, flooring and land."),
 "speed": ("speed", "speed-converter", "Speed is distance travelled per unit of time. Meters per second is the SI unit; miles per hour and kilometers per hour are used on roads, and knots at sea and in aviation."),
 "time": ("time", "time-converter", "Time is measured in seconds in the SI system. Months and years here use average lengths (a year is 365.2425 days), so results for them are averages."),
 "data": ("digital storage", "data-storage-converter", "These conversions use decimal (SI) prefixes where 1 KB = 1,000 bytes. Some operating systems use binary multiples of 1,024 instead, so reported sizes can differ slightly."),
 "pressure": ("pressure", "pressure-converter", "Pressure is force per unit area. The pascal is the SI unit; psi is common for tires and plumbing, bar and atm in weather and engineering, and mmHg in medicine."),
 "energy": ("energy", "energy-converter", "Energy is measured in joules in the SI system. Calories describe food energy, kilowatt hours appear on electricity bills, and BTU is used for heating and cooling."),
 "power": ("power", None, "Power is the rate of energy use. The watt is the SI unit; horsepower is common for engines and BTU per hour for heating and cooling equipment."),
 "force": ("force", None, "Force is measured in newtons in the SI system. Pound-force and kilogram-force are common in engineering and everyday weight contexts."),
 "angle": ("angle", None, "Angles can be measured in degrees (360 per full turn), radians (2π per full turn) or gradians (400 per full turn)."),
}
KIND_INFO.update({
 "frequency": ("frequency", None, "Frequency counts cycles per second. The hertz is the SI unit; rpm counts rotations per minute and is used for engines, motors and fans."),
 "torque": ("torque", None, "Torque is rotational force. The newton meter is the SI unit; pound-feet are common for engines and wheel nuts, and pound-inches or ounce-inches for small fasteners and motors."),
 "density": ("density", None, "Density is mass per unit volume. Water is about 1,000 kg/m³ (1 g/cm³ or 62.4 lb/ft³) at 4 °C."),
 "flow": ("flow rate", None, "Flow rate is the volume of fluid moving per unit of time. Liters per minute and gallons per minute are common for pumps and plumbing, and cfm for air handling."),
 "accel": ("acceleration", None, "Acceleration is the rate of change of speed. Standard gravity (g) is exactly 9.80665 m/s²."),
 "temperature": ("temperature", "temperature-converter", "Celsius and Kelvin share the same step size, while a Fahrenheit degree is 5/9 as large. Water freezes at 0 °C (32 °F, 273.15 K) and boils at 100 °C (212 °F, 373.15 K) at sea level."),
})
GROUP_NAMES = {"length": "Length", "mass": "Weight and Mass", "volume": "Volume", "area": "Area", "speed": "Speed", "time": "Time", "data": "Digital Storage",
               "pressure": "Pressure", "energy": "Energy", "power": "Power", "force": "Force", "angle": "Angle", "frequency": "Frequency",
               "torque": "Torque", "density": "Density", "flow": "Flow Rate", "accel": "Acceleration", "temperature": "Temperature"}


def kind_group(kind):
    return (f"{kind}-conversions", f"{GROUP_NAMES[kind]} Conversions",
            f"All {GROUP_NAMES[kind].lower()} unit conversions with formulas and reference tables.")


def _tbl(rows, h1, h2):
    body = "".join(f"<tr><td>{x}</td><td>{y}</td></tr>" for x, y in rows)
    return f'<table class="ref"><thead><tr><th>{h1}</th><th>{h2}</th></tr></thead><tbody>{body}</tbody></table>'


def pair_extra(kind, a, b, units):
    ka, na, aa, sa, fa = a
    kb, nb, ab, sb, fb = b
    F = fa / fb
    label, general, blurb = KIND_INFO[kind]
    vals = [1, 2, 5, 10, 20, 25, 50, 100, 250, 500, 1000]
    fwd = _tbl([(f"{v:,} {aa}", f"{fmt(v * F)} {ab}") for v in vals], na.title(), nb.title())
    rev = _tbl([(f"{v:,} {ab}", f"{fmt(v / F)} {aa}") for v in vals], nb.title(), na.title())
    ex = 12.5
    out = (f"<h2>{tc(na)} to {tc(nb)} formula</h2>\n"
           f"<p><b>{nb.capitalize()} = {na} &times; {fmt(F)}</b></p>\n"
           f"<p>Worked example: convert {ex} {na} to {nb}. Multiply {ex} &times; {fmt(F)} = <b>{fmt(ex * F)} {ab}</b>. "
           f"To go the other way, multiply {nb} by {fmt(1 / F)} (or divide by {fmt(F)}).</p>\n"
           f"<h2>{tc(na)} to {tc(nb)} conversion table</h2>\n{fwd}\n"
           f"<h2>{tc(nb)} to {tc(na)} conversion table</h2>\n{rev}\n"
           f"<h2>About {label} units</h2>\n<p>{blurb}</p>\n")
    return out


def pair_related(kind, a, b, units):
    rel = [f"{slugify(b[1])}-to-{slugify(a[1])}"]
    rel += [f"{slugify(a[1])}-to-{slugify(u[1])}" for u in units if u[0] not in (a[0], b[0])]
    rel += [f"{slugify(u[1])}-to-{slugify(b[1])}" for u in units if u[0] not in (a[0], b[0])]
    general = KIND_INFO[kind][1]
    return ([general] if general else []) + rel


def pair_spec(kind, a, b, units=None):
    ka, na, aa, sa, fa = a
    kb, nb, ab, sb, fb = b
    F = fa / fb
    title = f"{tc(na)} to {tc(nb)} Converter"
    slug = f"{slugify(na)}-to-{slugify(nb)}"
    desc = f"Convert {na} to {nb} instantly. 1 {aa} = {fmt(F)} {ab}."
    body = ("const F=%r;const r=v*F;return [[SF(v)+' %s =',SF(r)+' %s'],"
            "['Formula','%s = %s × '+SF(F)],['Reverse','1 %s = '+SF(1/F)+' %s']," % (F, aa, ab, ab, aa, ab, aa)
            + "...[1,2,5,10,25,50,100,1000].map(x=>[SF(x)+' %s',SF(x*F)+' %s'])];" % (aa, ab))
    about = (f"To convert {na} to {nb}, multiply the number of {na} by {fmt(F)}. One {sa} equals {fmt(F)} {nb}, "
             f"and one {sb} equals {fmt(1 / F)} {na}. The table shows common values.")
    faqs = [(f"How many {nb} are in one {sa}?", f"There are {fmt(F)} {nb} in one {sa}."),
            (f"How many {na} are in one {sb}?", f"There are {fmt(1 / F)} {na} in one {sb}.")]
    extra = pair_extra(kind, a, b, units) if units else ""
    related = pair_related(kind, a, b, units) if units else None
    return C("conversion", slug, title, desc, [("v", f"Value in {na} ({aa})", 1)], body, about, faqs, extra, related, kind_group(kind))


def temp_extra(a, b, na, nb, aa, ab, f, t):
    pts = {"C": [-40, -20, 0, 10, 20, 25, 30, 37, 50, 100, 150, 200], "F": [-40, 0, 32, 50, 68, 72, 86, 98.6, 212, 350, 400, 450],
           "K": [0, 100, 200, 250, 273.15, 293.15, 300, 310.15, 373.15, 500, 1000]}[a]
    def conv(v):
        c = {"C": v, "F": (v - 32) * 5 / 9, "K": v - 273.15}[a]
        return {"C": c, "F": c * 9 / 5 + 32, "K": c + 273.15}[b]
    rows = "".join(f"<tr><td>{v:g} {aa}</td><td>{conv(v):.2f}".rstrip("0").rstrip(".") + f" {ab}</td></tr>" for v in pts)
    return (f"<h2>{na} to {nb} conversion table</h2>\n<table class=\"ref\"><thead><tr><th>{na}</th><th>{nb}</th></tr></thead><tbody>{rows}</tbody></table>\n"
            f"<h2>About temperature scales</h2>\n<p>{KIND_INFO['temperature'][2]}</p>\n")


def temp_specs():
    names = {"C": ("Celsius", "°C"), "F": ("Fahrenheit", "°F"), "K": ("Kelvin", "K")}
    f = {"C": "v", "F": "(v-32)*5/9", "K": "v-273.15"}
    t = {"C": "c", "F": "c*9/5+32", "K": "c+273.15"}
    out = []
    for a in "CFK":
        for b in "CFK":
            if a == b:
                continue
            na, aa = names[a]
            nb, ab = names[b]
            body = ("const c=%s;const conv=x=>{const c=%s;return %s;};const r=conv(v);"
                    "return [[N(v,6)+' %s =',N(r,6)+' %s'],...[-40,0,20,37,100].map(x=>{const cc=%s;return [N(x)+' %s',N(%s,4)+' %s'];})];"
                    % (f[a], f[a].replace("v", "x"), t[b], aa, ab, f[a].replace("v", "x"), aa, t[b].replace("c", "cc"), ab))
            formulas = {("C", "F"): "°F = °C × 9/5 + 32", ("F", "C"): "°C = (°F − 32) × 5/9", ("C", "K"): "K = °C + 273.15",
                        ("K", "C"): "°C = K − 273.15", ("F", "K"): "K = (°F − 32) × 5/9 + 273.15", ("K", "F"): "°F = (K − 273.15) × 9/5 + 32"}
            out.append(C("conversion", f"{na.lower()}-to-{nb.lower()}", f"{na} to {nb} Converter",
                         f"Convert {na} to {nb} instantly with the exact formula.",
                         [("v", f"Temperature in {aa}", 100 if a == "C" else 212 if a == "F" else 373.15)], body,
                         f"The conversion formula is {formulas[(a, b)]}. The table lists reference points such as freezing and boiling.",
                         [(f"What is the formula for {na} to {nb}?", formulas[(a, b)] + "."),
                          ("What temperature is the same in Celsius and Fahrenheit?", "-40 degrees is the same in both scales.")],
                         temp_extra(a, b, na, nb, aa, ab, f, t),
                         [f"{names[b][0].lower()}-to-{names[a][0].lower()}"] + [f"{names[x][0].lower()}-to-{names[y][0].lower()}" for x in "CFK" for y in "CFK" if x != y and (x, y) not in ((a, b), (b, a))] + ["temperature-converter"],
                         kind_group("temperature")))
    return out


PAIRS = []
for kind, (base, units) in TABLES.items():
    for a in units:
        for b in units:
            if a[0] != b[0]:
                PAIRS.append(pair_spec(kind, a, b, units))
PAIRS += temp_specs()

# --- Handwritten everyday / tools -------------------------------------------------------
EXTRA = [
C("everyday", "time-calculator", "Time Calculator (Add or Subtract Time)",
  "Add or subtract hours and minutes.",
  [("h1", "Hours (1st)", 5), ("m1", "Minutes (1st)", 45), ("op", "Operation", 1, [(1, "+ Add"), (-1, "− Subtract")]), ("h2", "Hours (2nd)", 2), ("m2", "Minutes (2nd)", 30)],
  r"""const t=(h1*60+m1)+op*(h2*60+m2),a=Math.abs(t);return [['Result',(t<0?'-':'')+Math.floor(a/60)+' h '+a%60+' min'],['Decimal hours',N(t/60,4)],['Total minutes',t]];""",
  "Both times are converted to minutes, combined, then converted back to hours and minutes.",
  [("How do I add times that cross an hour?", "Add the minutes, carry every 60 minutes into one hour.")]),
C("everyday", "hours-to-decimal-calculator", "Hours and Minutes to Decimal Calculator",
  "Convert time to decimal hours and back for timesheets.",
  [("h", "Hours", 7), ("m", "Minutes", 45), ("dec", "Decimal hours to convert back", 7.75)],
  r"""const hh=Math.floor(dec),mm=Math.round((dec-hh)*60);return [['Decimal hours',N(h+m/60,4)],[N(dec,4)+' decimal hours as h:mm',hh+' h '+mm+' min'],['Minutes as decimal','15 min = 0.25, 30 min = 0.5, 45 min = 0.75']];""",
  "Decimal hours = hours + minutes / 60. To reverse it, multiply the decimal part by 60.",
  [("Why use decimal hours?", "Payroll multiplies pay rate by decimal hours.")]),
C("everyday", "week-number-calculator", "Week Number Calculator",
  "Find the ISO week number and day of the year for any date.",
  [("date", "Date", "today", "date")],
  r"""const d=D(date),t=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())),dn=t.getUTCDay()||7;t.setUTCDate(t.getUTCDate()+4-dn);const y0=new Date(Date.UTC(t.getUTCFullYear(),0,1)),wk=Math.ceil(((t-y0)/864e5+1)/7);
const doy=Math.round((d-new Date(d.getFullYear(),0,0))/864e5);return [['ISO week number',wk],['ISO year',t.getUTCFullYear()],['Day of the year',doy],['Weekday',DS(d).split(',')[0]]];""",
  "ISO 8601 weeks start on Monday, and week 1 is the week containing the first Thursday of the year.",
  [("Can week 53 exist?", "Yes, in some years.")]),
C("everyday", "business-days-calculator", "Business Days Calculator",
  "Count working days between two dates, minus holidays.",
  [("start", "Start date", "today", "date"), ("end", "End date", "2027-01-01", "date"), ("hol", "Holidays to exclude", 0)],
  r"""let s=D(start),e=D(end);if(e<s)[s,e]=[e,s];let n=0;for(let d=new Date(s);d<e;d.setDate(d.getDate()+1)){const w=d.getDay();if(w!==0&&w!==6)n++;}
return [['Business days',Math.max(n-hol,0)],['Calendar days',Math.round((e-s)/864e5)],['Weekend days',Math.round((e-s)/864e5)-n]];""",
  "Business days count Monday through Friday between the dates (start included, end excluded), minus any holidays you enter.",
  [("Does it know public holidays?", "No. Enter the number of holidays that fall on weekdays.")]),
C("everyday", "zodiac-sign-calculator", "Zodiac Sign Calculator",
  "Find your Western zodiac sign from your birth date.",
  [("date", "Birth date", "1995-06-15", "date")],
  r"""const d=D(date),m=d.getMonth()+1,day=d.getDate(),z=[['Capricorn',12,22],['Aquarius',1,20],['Pisces',2,19],['Aries',3,21],['Taurus',4,20],['Gemini',5,21],['Cancer',6,21],['Leo',7,23],['Virgo',8,23],['Libra',9,23],['Scorpio',10,23],['Sagittarius',11,22]];
let s='Capricorn';for(const [n,mm,dd] of z){if(m>mm||(m===mm&&day>=dd))s=n;}if(m===1&&day<20)s='Capricorn';
const el={Aries:'Fire',Leo:'Fire',Sagittarius:'Fire',Taurus:'Earth',Virgo:'Earth',Capricorn:'Earth',Gemini:'Air',Libra:'Air',Aquarius:'Air',Cancer:'Water',Scorpio:'Water',Pisces:'Water'}[s];return [['Zodiac sign',s],['Element',el]];""",
  "Western astrology assigns a sign by the date of birth within roughly one-month ranges. It is a cultural tradition, not science.",
  [("Do dates vary by year?", "Cusp dates can shift by a day depending on the year.")]),
C("everyday", "chinese-zodiac-calculator", "Chinese Zodiac Calculator",
  "Find your Chinese zodiac animal and element from your birth year.",
  [("y", "Birth year", 1990)],
  r"""y=Math.round(y);const an=['Rat','Ox','Tiger','Rabbit','Dragon','Snake','Horse','Goat','Monkey','Rooster','Dog','Pig'],el=['Wood','Fire','Earth','Metal','Water'];return [['Animal',an[((y-4)%12+12)%12]],['Element',el[Math.floor((((y-4)%10)+10)%10/2)]],['Note','People born in January or early February may belong to the previous lunar year']];""",
  "The Chinese zodiac cycles through 12 animals and 5 elements. The year is based on the lunar new year, so early-year births can belong to the prior sign.",
  [("When does the Chinese year start?", "On the lunar new year, between late January and mid-February.")]),
C("everyday", "word-counter", "Word Counter",
  "Count words, characters, sentences and reading time of any text.",
  [("text", "Your text", "Paste or type your text here. This counter updates as you type.", "textarea")],
  r"""const w=text.trim().split(/\s+/).filter(Boolean).length,ch=text.length,chn=text.replace(/\s/g,'').length,se=(text.match(/[.!?]+(\s|$)/g)||[]).length,pa=text.split(/\n+/).filter(x=>x.trim()).length;
return [['Words',w],['Characters',ch],['Characters (no spaces)',chn],['Sentences',se],['Paragraphs',pa],['Reading time',N(w/225,1)+' min'],['Speaking time',N(w/130,1)+' min']];""",
  "Words are counted as groups of characters separated by whitespace. Reading time assumes 225 words per minute and speaking time 130.",
  [("Is my text stored?", "No. Counting happens in your browser.")]),
C("everyday", "download-time-calculator", "Download Time Calculator",
  "Estimate how long a download or upload takes.",
  [("size", "File size", 10), ("u", "Unit", 1000, [(1, "MB"), (1000, "GB"), (1e6, "TB")]), ("sp", "Connection speed (Mbps)", 100)],
  r"""const bits=size*u*8e6,s=bits/(sp*1e6),h=Math.floor(s/3600),m=Math.floor(s%3600/60),sec=Math.round(s%60);return [['Download time',h+' h '+m+' min '+sec+' s'],['Total seconds',N(s,1)],['Real speed in MB/s',N(sp/8,2)]];""",
  "Time = file size in megabits / speed in Mbps. Real speeds are usually 5-20% lower due to overhead.",
  [("Why is my download slower?", "Server limits, Wi-Fi quality and network congestion.")]),
C("everyday", "aspect-ratio-calculator", "Aspect Ratio Calculator",
  "Find the aspect ratio of a screen or image and scale it.",
  [("w", "Width", 1920), ("h", "Height", 1080), ("nw", "New width", 1280)],
  r"""const g=GCD(Math.round(w),Math.round(h));return [['Aspect ratio',w/g+':'+h/g],['Decimal',N(w/h,4)],['New height for new width',N(nw*h/w,2)],['Megapixels',N(w*h/1e6,2)]];""",
  "Divide width and height by their GCD for the ratio. To resize, keep the ratio and compute new height = new width x height / width.",
  [("Common ratios?", "16:9 for video, 4:3 for older screens, 3:2 for photos.")]),
C("everyday", "ppi-calculator", "PPI Calculator (Pixel Density)",
  "Calculate screen pixel density and physical size.",
  [("w", "Width (pixels)", 2560), ("h", "Height (pixels)", 1440), ("d", "Diagonal (inches)", 27)],
  r"""const dp=Math.hypot(w,h),ppi=dp/d,ww=w/ppi,hh=h/ppi;return [['Pixel density',N(ppi,1)+' PPI'],['Physical width',N(ww,2)+' in ('+N(ww*2.54,1)+' cm)'],['Physical height',N(hh,2)+' in ('+N(hh*2.54,1)+' cm)'],['Total pixels',N(w*h/1e6,2)+' MP']];""",
  "PPI = √(width² + height²) / diagonal. Higher PPI means sharper images.",
  [("What PPI looks sharp?", "Around 110 at arm's length for monitors, 300+ for phones.")]),
C("everyday", "mileage-reimbursement-calculator", "Mileage Reimbursement Calculator",
  "Calculate mileage reimbursement at the IRS standard rate.",
  [("mi", "Business miles", 1200), ("rate", "Rate ($ per mile)", 0.70)],
  r"""return [['Reimbursement',M(mi*rate)],['Per month (12)',M(mi*rate/12)]];""",
  "Reimbursement is miles x rate. The 2025 IRS business rate is 70 cents per mile; check the IRS for the current year.",
  [("Can I deduct mileage?", "Self-employed people can often deduct it. Employees usually cannot under current US federal law.")]),
C("everyday", "car-depreciation-calculator", "Car Depreciation Calculator",
  "Estimate how much value a car loses each year.",
  [("p", "Purchase price ($)", 35000), ("r", "Annual depreciation (%)", 15), ("y", "Years", 5)],
  r"""const v=n=>p*Math.pow(1-r/100,n);return [['Value after '+y+' years',M(v(y))],['Total depreciation',M(p-v(y))],['After 1 year',M(v(1))],['After 3 years',M(v(3))],['After 5 years',M(v(5))]];""",
  "A declining-balance estimate: each year the car loses a fixed percentage of its remaining value. New cars often lose about 15-20% in year one.",
  [("Which cars hold value best?", "Reliable trucks and some SUVs and sports cars.")]),
C("everyday", "mpg-calculator", "MPG Calculator",
  "Calculate fuel economy from distance and fuel used.",
  [("mi", "Miles driven", 350), ("gal", "Gallons used", 12)],
  r"""const m=mi/gal;return [['Fuel economy',N(m,1)+' mpg'],['Litres per 100 km',N(235.215/m,2)],['Cost per mile at $3.50/gal',M(3.5/m)]];""",
  "MPG = miles / gallons. Fill the tank both times for accurate tracking.",
  [("What is good MPG?", "Over 30 mpg for gas cars is considered good.")]),
C("everyday", "weighted-grade-calculator", "Weighted Grade Calculator",
  "Combine assignment categories into an overall course grade.",
  [("g1", "Homework grade (%)", 92), ("w1", "Homework weight (%)", 20), ("g2", "Quizzes grade (%)", 85), ("w2", "Quizzes weight (%)", 20), ("g3", "Midterm grade (%)", 78), ("w3", "Midterm weight (%)", 25), ("g4", "Final grade (%)", 88), ("w4", "Final weight (%)", 35)],
  r"""const w=w1+w2+w3+w4;if(!w)return 'Weights cannot all be zero.';const g=(g1*w1+g2*w2+g3*w3+g4*w4)/w;const L=g>=90?'A':g>=80?'B':g>=70?'C':g>=60?'D':'F';return [['Course grade',PCT(g,2)],['Letter',L],['Total weight',w+'%']];""",
  "Weighted grade = Σ(grade x weight) / Σ(weights).",
  [("Do weights have to add to 100?", "They should, but the calculator normalizes if they do not.")]),
C("everyday", "test-grade-calculator", "Test Grade Calculator",
  "Convert test points to a percentage and letter grade.",
  [("c", "Points earned", 42), ("t", "Total points", 50)],
  r"""const p=c/t*100;const L=p>=97?'A+':p>=93?'A':p>=90?'A-':p>=87?'B+':p>=83?'B':p>=80?'B-':p>=77?'C+':p>=73?'C':p>=70?'C-':p>=67?'D+':p>=60?'D':'F';return [['Percentage',PCT(p,2)],['Letter grade',L],['Points missed',t-c]];""",
  "Percentage = points earned / total points x 100, mapped to a standard letter scale.",
  [("Are letter scales the same everywhere?", "No. Schools differ, so check your syllabus.")]),
C("everyday", "recipe-scaler", "Recipe Scaler",
  "Scale a recipe up or down for a different number of servings.",
  [("o", "Original servings", 4), ("n", "Desired servings", 10), ("amt", "Ingredient amount", 1.5)],
  r"""const f=n/o;return [['Scaled amount',N(amt*f,3)],['Scale factor','×'+N(f,3)],['Note','Adjust cooking time and pan size for big changes']];""",
  "Multiply every ingredient by desired servings / original servings.",
  [("Do spices scale linearly?", "Not always. Season to taste when scaling by large factors.")]),
C("everyday", "ev-charging-cost-calculator", "EV Charging Cost Calculator",
  "Estimate the cost to charge an electric car and cost per mile.",
  [("kwh", "Energy added (kWh)", 60), ("p", "Electricity price ($/kWh)", 0.16), ("eff", "Efficiency (miles per kWh)", 3.5), ("mi", "Miles to drive", 300)],
  r"""return [['Cost to charge',M(kwh*p)],['Cost per mile',M(p/eff)],['Cost for '+mi+' miles',M(mi/eff*p)],['Range from that charge',N(kwh*eff,0)+' miles']];""",
  "Charging cost = kWh x price. Cost per mile = price / (miles per kWh).",
  [("Is public charging more expensive?", "Yes, DC fast charging usually costs several times more than home charging.")]),
C("everyday", "volumetric-weight-calculator", "Volumetric Weight Calculator",
  "Find the chargeable weight of a parcel for shipping.",
  [("l", "Length (cm)", 50), ("w", "Width (cm)", 40), ("h", "Height (cm)", 30), ("div", "Divisor", 5000, [(5000, "5000 (most couriers)"), (4000, "4000"), (6000, "6000")]), ("act", "Actual weight (kg)", 8)],
  r"""const v=l*w*h/div;return [['Chargeable weight',N(Math.max(v,act),2)+' kg'],['Volumetric weight',N(v,2)+' kg'],['Actual weight',N(act,2)+' kg']];""",
  "Carriers charge the greater of actual and volumetric weight. Volumetric = L x W x H / divisor.",
  [("Why does it exist?", "Light but bulky parcels take up cargo space, so carriers charge for volume.")]),
C("everyday", "cups-to-grams-calculator", "Cups to Grams Calculator",
  "Convert cups of common ingredients to grams.",
  [("cups", "Cups", 1), ("ing", "Ingredient", 125, [(125, "All-purpose flour"), (200, "Granulated sugar"), (213, "Brown sugar (packed)"), (120, "Powdered sugar"), (227, "Butter"), (237, "Water"), (245, "Milk"), (340, "Honey"), (185, "Rice (uncooked)"), (90, "Rolled oats"), (85, "Cocoa powder")])],
  r"""return [['Grams',N(cups*ing,1)+' g'],['Ounces',N(cups*ing/28.3495,2)+' oz'],['Grams per cup',ing]];""",
  "Dry ingredients vary in density, so grams per cup depend on the ingredient. Values are common baking averages.",
  [("Why weigh ingredients?", "Weighing is more accurate than measuring by volume.")]),
C("conversion", "hex-to-rgb-converter", "HEX to RGB Color Converter",
  "Convert a HEX color code to RGB and HSL.",
  [("hex", "HEX color", "#3498db", "text")],
  r"""let h=hex.trim().replace('#','');if(h.length===3)h=h.split('').map(c=>c+c).join('');if(!/^[0-9a-fA-F]{6}$/.test(h))return 'Enter a valid HEX color like #3498db.';
const r=parseInt(h.slice(0,2),16),g=parseInt(h.slice(2,4),16),b=parseInt(h.slice(4,6),16),R=r/255,G=g/255,B=b/255,mx=Math.max(R,G,B),mn=Math.min(R,G,B),l=(mx+mn)/2,d=mx-mn;
let s=d===0?0:d/(1-Math.abs(2*l-1)),hh=d===0?0:mx===R?((G-B)/d)%6:mx===G?(B-R)/d+2:(R-G)/d+4;hh=Math.round((hh*60+360)%360);
return [['RGB','rgb('+r+', '+g+', '+b+')'],['HSL','hsl('+hh+', '+Math.round(s*100)+'%, '+Math.round(l*100)+'%)'],['HEX','#'+h.toUpperCase()]];""",
  "A HEX code encodes red, green and blue as three two-digit hexadecimal numbers (00-FF).",
  [("What does #FFFFFF mean?", "White: all three channels at maximum.")]),
C("conversion", "rgb-to-hex-converter", "RGB to HEX Color Converter",
  "Convert RGB values to a HEX color code.",
  [("r", "Red (0-255)", 52), ("g", "Green (0-255)", 152), ("b", "Blue (0-255)", 219)],
  r"""const c=v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0').toUpperCase();return [['HEX','#'+c(r)+c(g)+c(b)],['RGB','rgb('+Math.round(r)+', '+Math.round(g)+', '+Math.round(b)+')']];""",
  "Each channel 0-255 is written as two hexadecimal digits and joined.",
  [("What are web-safe colors?", "An old 216-color palette; modern screens show all 16.7 million.")]),
C("conversion", "cooking-temperature-converter", "Oven Temperature Converter",
  "Convert oven temperatures between Fahrenheit, Celsius and gas mark.",
  [("f", "Temperature (°F)", 350)],
  r"""const c=(f-32)*5/9;const gm=f<275?'1/4':f<300?'1':f<325?'2':f<350?'3':f<375?'4':f<400?'5':f<425?'6':f<450?'7':f<475?'8':'9';return [['Celsius',N(c,0)+' °C'],['Fan oven (approx.)',N(c-20,0)+' °C'],['Gas mark (approx.)',gm]];""",
  "Celsius = (°F - 32) x 5/9. Fan ovens run about 20 °C cooler. Gas marks are approximate.",
  [("350°F in Celsius?", "About 177 °C, commonly set to 180 °C.")]),
C("conversion", "shoe-size-converter", "Shoe Size Converter",
  "Convert US men's shoe sizes to UK and EU sizes (approximate).",
  [("us", "US men's size", 9)],
  r"""return [['UK size',N(us-0.5,1)],['EU size',N(us+33,1)],['Foot length',N(us*0.8467+18.9,1)+' cm (approx.)'],['US women\'s equivalent',N(us+1.5,1)]];""",
  "Sizing systems differ by brand. These are widely used approximations, so check the brand's size chart.",
  [("Do brands vary?", "Yes, by up to a half size or more.")]),
]

SPECS = PAIRS + EXTRA
