from spec import C
import json


def conv(slug, title, units, default_a, default_b, about, faq):
    """units: list of (key, label, factor_to_base)."""
    opts = lambda: [(k, l) for k, l, _ in units]
    factors = json.dumps({k: f for k, _, f in units})
    body = ("const f=%s;const r=v*f[a]/f[b];"
            "return [[N(v,8)+' '+a+' =',N(r,10)+' '+b],['Multiply by',N(f[a]/f[b],12)]];" % factors)
    return C("conversion", slug, title, "Convert between " + ", ".join(l.split(" (")[0].lower() for _, l, _ in units[:5]) + " and more.",
             [("v", "Value", 1), ("a", "From", default_a, opts()), ("b", "To", default_b, opts())], body, about, faq)


CONV = [
conv("length-converter", "Length Converter",
     [("m", "Metres (m)", 1), ("km", "Kilometres (km)", 1000), ("cm", "Centimetres (cm)", .01), ("mm", "Millimetres (mm)", .001),
      ("mi", "Miles (mi)", 1609.344), ("yd", "Yards (yd)", .9144), ("ft", "Feet (ft)", .3048), ("in", "Inches (in)", .0254), ("nmi", "Nautical miles (nmi)", 1852)],
     "mi", "km", "All lengths are converted through metres. One mile is exactly 1,609.344 metres and one inch is exactly 2.54 centimetres.",
     [("How many feet are in a mile?", "There are 5,280 feet in a mile.")]),
conv("weight-converter", "Weight and Mass Converter",
     [("kg", "Kilograms (kg)", 1), ("g", "Grams (g)", .001), ("mg", "Milligrams (mg)", 1e-6), ("lb", "Pounds (lb)", .45359237),
      ("oz", "Ounces (oz)", .028349523125), ("st", "Stone (st)", 6.35029318), ("t", "Metric tonnes (t)", 1000)],
     "lb", "kg", "Values are converted through kilograms. One pound is defined as exactly 0.45359237 kg.",
     [("How many pounds are in a kilogram?", "One kilogram is about 2.2046 pounds.")]),
conv("volume-converter", "Volume Converter",
     [("l", "Litres (l)", 1), ("ml", "Millilitres (ml)", .001), ("gal", "US gallons (gal)", 3.785411784), ("qt", "US quarts (qt)", .946352946),
      ("pt", "US pints (pt)", .473176473), ("cup", "US cups (cup)", .2365882365), ("floz", "US fluid ounces (fl oz)", .0295735295625),
      ("tbsp", "Tablespoons (tbsp)", .01478676478125), ("tsp", "Teaspoons (tsp)", .00492892159375), ("m3", "Cubic metres (m3)", 1000)],
     "gal", "l", "Volumes are converted through litres using US customary definitions for gallons, quarts, pints, cups and spoons.",
     [("How many cups are in a gallon?", "A US gallon contains 16 cups.")]),
conv("speed-converter", "Speed Converter",
     [("mps", "Metres per second (m/s)", 1), ("kph", "Kilometres per hour (km/h)", 1/3.6), ("mph", "Miles per hour (mph)", .44704),
      ("knot", "Knots (kn)", 1852/3600), ("fps", "Feet per second (ft/s)", .3048)],
     "mph", "kph", "Speeds are converted through metres per second.",
     [("How many km/h is 60 mph?", "60 mph is about 96.56 km/h.")]),
conv("area-converter", "Area Converter",
     [("m2", "Square metres (m2)", 1), ("km2", "Square kilometres (km2)", 1e6), ("ha", "Hectares (ha)", 1e4), ("acre", "Acres (acre)", 4046.8564224),
      ("ft2", "Square feet (ft2)", .09290304), ("yd2", "Square yards (yd2)", .83612736), ("in2", "Square inches (in2)", .00064516),
      ("mi2", "Square miles (mi2)", 2589988.110336), ("cm2", "Square centimetres (cm2)", 1e-4)],
     "acre", "m2", "Areas are converted through square metres.",
     [("How many square feet are in an acre?", "An acre is 43,560 square feet.")]),
conv("data-storage-converter", "Data Storage Converter",
     [("B", "Bytes (B)", 1), ("KB", "Kilobytes (KB, 1000)", 1e3), ("MB", "Megabytes (MB)", 1e6), ("GB", "Gigabytes (GB)", 1e9), ("TB", "Terabytes (TB)", 1e12),
      ("PB", "Petabytes (PB)", 1e15), ("KiB", "Kibibytes (KiB, 1024)", 1024), ("MiB", "Mebibytes (MiB)", 1048576), ("GiB", "Gibibytes (GiB)", 1073741824),
      ("TiB", "Tebibytes (TiB)", 1099511627776), ("bit", "Bits (bit)", .125)],
     "GB", "MB", "KB, MB and GB use powers of 1000 as drive makers do. KiB, MiB and GiB use powers of 1024 as many operating systems do.",
     [("Why does my 1 TB drive show less space?", "Drives are sold in decimal units (1 TB = 10^12 bytes) while Windows reports binary units, so it shows about 931 GiB.")]),
conv("time-converter", "Time Converter",
     [("ms", "Milliseconds (ms)", .001), ("s", "Seconds (s)", 1), ("min", "Minutes (min)", 60), ("h", "Hours (h)", 3600), ("day", "Days (day)", 86400),
      ("week", "Weeks (week)", 604800), ("month", "Months (avg)", 2629746), ("year", "Years (avg)", 31556952)],
     "h", "min", "Times are converted through seconds. A month is the average of 30.44 days and a year is 365.2425 days.",
     [("How many seconds are in a day?", "86,400 seconds.")]),
conv("pressure-converter", "Pressure Converter",
     [("Pa", "Pascals (Pa)", 1), ("kPa", "Kilopascals (kPa)", 1000), ("bar", "Bar (bar)", 1e5), ("psi", "Pounds per sq inch (psi)", 6894.757293168),
      ("atm", "Atmospheres (atm)", 101325), ("mmHg", "mmHg (torr)", 133.322387415)],
     "psi", "bar", "Pressures are converted through pascals.",
     [("How many psi is one bar?", "One bar is about 14.504 psi.")]),
conv("energy-converter", "Energy Converter",
     [("J", "Joules (J)", 1), ("kJ", "Kilojoules (kJ)", 1000), ("cal", "Calories (cal)", 4.184), ("kcal", "Food calories (kcal)", 4184),
      ("Wh", "Watt-hours (Wh)", 3600), ("kWh", "Kilowatt-hours (kWh)", 3.6e6), ("BTU", "BTU", 1055.05585262)],
     "kcal", "kJ", "Energy is converted through joules.",
     [("Is a food Calorie the same as a kcal?", "Yes. The 'Calorie' on food labels is a kilocalorie (1,000 calories).")]),
C("conversion", "temperature-converter", "Temperature Converter",
  "Convert between Celsius, Fahrenheit and Kelvin.",
  [("v", "Temperature", 100), ("a", "From", "C", [("C", "Celsius (°C)"), ("F", "Fahrenheit (°F)"), ("K", "Kelvin (K)")]), ("b", "To", "F", [("C", "Celsius (°C)"), ("F", "Fahrenheit (°F)"), ("K", "Kelvin (K)")])],
  r"""const c=a=='C'?v:a=='F'?(v-32)*5/9:v-273.15;
const r=b=='C'?c:b=='F'?c*9/5+32:c+273.15;
return [[N(v,6)+' °'+a+' =',N(r,6)+' °'+b],['Celsius',N(c,4)],['Fahrenheit',N(c*9/5+32,4)],['Kelvin',N(c+273.15,4)]];""",
  "Fahrenheit = Celsius x 9/5 + 32. Kelvin = Celsius + 273.15. Values are converted through Celsius.",
  [("At what temperature are Celsius and Fahrenheit equal?", "At -40 degrees.")]),
C("conversion", "fuel-economy-converter", "Fuel Economy Converter (MPG to L/100km)",
  "Convert miles per gallon to litres per 100 km and kilometres per litre.",
  [("mpg", "Miles per gallon (US)", 30)],
  r"""const l=235.214583/mpg;
return [['Litres per 100 km',N(l,2)],['Kilometres per litre',N(100/l,2)],['Imperial MPG',N(mpg*1.200950,2)]];""",
  "L/100km = 235.2146 / MPG (US). The metric figure shows fuel used per distance, so lower is better.",
  [("Why do the units run opposite ways?", "MPG measures distance per fuel (higher is better) while L/100 km measures fuel per distance (lower is better).")]),
]

GRADES = [(4, "A (4.0)"), (3.7, "A- (3.7)"), (3.3, "B+ (3.3)"), (3, "B (3.0)"), (2.7, "B- (2.7)"), (2.3, "C+ (2.3)"),
          (2, "C (2.0)"), (1.7, "C- (1.7)"), (1.3, "D+ (1.3)"), (1, "D (1.0)"), (0, "F (0.0)")]
GPA_INPUTS = []
for i in range(1, 7):
    GPA_INPUTS += [(f"g{i}", f"Course {i} grade", 4 if i < 5 else 0, GRADES),
                   (f"c{i}", f"Course {i} credits (0 if unused)", 3 if i < 5 else 0)]

EVERYDAY = [
C("everyday", "age-calculator", "Age Calculator",
  "Calculate exact age in years, months and days, plus days until the next birthday.",
  [("birth", "Date of birth", "1990-01-01", "date"), ("asof", "Age at date", "today", "date")],
  r"""const b=D(birth),t=D(asof);if(t<b)return 'The date is before the birth date.';
let y=t.getFullYear()-b.getFullYear(),m=t.getMonth()-b.getMonth(),d=t.getDate()-b.getDate();
if(d<0){m--;d+=new Date(t.getFullYear(),t.getMonth(),0).getDate();}
if(m<0){y--;m+=12;}
const days=Math.round((t-b)/864e5);
let nb=new Date(t.getFullYear(),b.getMonth(),b.getDate());if(nb<t)nb=new Date(t.getFullYear()+1,b.getMonth(),b.getDate());
return [['Age',y+' years, '+m+' months, '+d+' days'],['Total days',N(days,0)],['Total weeks',N(Math.floor(days/7),0)],['Next birthday in',Math.round((nb-t)/864e5)+' days'],['Born on a',DS(b).split(',')[0]]];""",
  "The calculator subtracts the birth date from the chosen date, borrowing days and months where needed, so the result matches how people normally state their age.",
  [("Can I calculate age on a future date?", "Yes. Change the 'Age at date' field to any date.")]),

C("everyday", "date-difference-calculator", "Days Between Dates Calculator",
  "Count the days, weeks and business days between two dates.",
  [("start", "Start date", "today", "date"), ("end", "End date", "2027-01-01", "date")],
  r"""let s=D(start),e2=D(end),sign=1;if(e2<s){[s,e2]=[e2,s];sign=-1;}
const days=Math.round((e2-s)/864e5);let wd=0;
for(let i=0;i<days;i++){const x=new Date(s.getFullYear(),s.getMonth(),s.getDate()+i).getDay();if(x!==0&&x!==6)wd++;}
return [['Days',N(days*sign,0)],['Weeks and days',Math.floor(days/7)+' weeks '+days%7+' days'],['Business days (Mon-Fri)',wd],['Approx. months',N(days/30.4375,1)]];""",
  "The difference is the number of midnight-to-midnight days between the two dates. Business days count weekdays only and do not remove public holidays.",
  [("Is the end date included?", "No. The count is the number of days from the start date up to, but not including, the end date.")]),

C("everyday", "add-days-to-date-calculator", "Date Calculator (Add or Subtract Days)",
  "Find the date that is a number of days before or after a given date.",
  [("date", "Start date", "today", "date"), ("days", "Number of days", 30), ("op", "Operation", 1, [(1, "Add days"), (-1, "Subtract days")])],
  r"""const x=D(date);x.setDate(x.getDate()+op*Math.round(days));
return [['Resulting date',DS(x)],['Weeks',N(days/7,1)]];""",
  "The calculator moves the calendar forward or backward by the number of days entered, handling month and year changes and leap years automatically.",
  [("How do I add months instead of days?", "Use the days-between-dates calculator to check your target, or add roughly 30.44 days per month.")]),

C("everyday", "days-until-calculator", "Days Until Calculator",
  "Count down the days until a date such as a birthday, holiday or deadline.",
  [("target", "Target date", "2027-01-01", "date"), ("from", "From", "today", "date")],
  r"""const a=D(from),b=D(target),d=Math.round((b-a)/864e5);
return [[d>=0?'Days remaining':'Days ago',N(Math.abs(d),0)],['Weeks',N(Math.abs(d)/7,1)],['Target date',DS(b)]];""",
  "The result is the number of whole days between today (or another start date) and your target date.",
  [("Does this include weekends?", "Yes. All calendar days are counted. Use the days-between-dates calculator for business days.")]),

C("everyday", "time-duration-calculator", "Hours Between Times Calculator",
  "Calculate hours worked between a start and end time, minus breaks.",
  [("st", "Start time", "09:00", "time"), ("en", "End time", "17:30", "time"), ("brk", "Unpaid break (minutes)", 30)],
  r"""const p=t=>{const [h,m]=t.split(':').map(Number);return h*60+m;};
let d=p(en)-p(st);if(d<0)d+=1440;d-=brk;if(d<0)return 'Break is longer than the shift.';
return [['Time worked',Math.floor(d/60)+' h '+d%60+' min'],['Decimal hours',N(d/60,2)],['Over 5 days',N(d/60*5,2)+' h']];""",
  "The end time is subtracted from the start time, rolling past midnight if needed, then the break is removed.",
  [("What are decimal hours?", "Minutes divided by 60 added to the hours, so 7 h 30 min is 7.5 hours. Payroll uses them to multiply by an hourly rate.")]),

C("everyday", "gpa-calculator", "GPA Calculator",
  "Calculate your grade point average from course grades and credit hours.",
  GPA_INPUTS,
  r"""const g=[g1,g2,g3,g4,g5,g6],c=[c1,c2,c3,c4,c5,c6];let pts=0,cr=0;
for(let i=0;i<6;i++){pts+=g[i]*c[i];cr+=c[i];}
if(!cr)return 'Enter credits for at least one course.';
return [['GPA',N(pts/cr,2)],['Total credits',cr],['Quality points',N(pts,2)]];""",
  "GPA is the sum of (grade points x credit hours) divided by total credit hours. Set credits to 0 for unused rows.",
  [("Weighted vs unweighted GPA?", "Unweighted uses a 4.0 scale for all classes. Weighted GPAs give extra points for honors or AP classes. This calculator is unweighted.")]),

C("everyday", "fuel-cost-calculator", "Fuel Cost Calculator",
  "Estimate the fuel cost of a trip from distance, mpg and gas price.",
  [("dist", "Trip distance (miles)", 300), ("mpg", "Fuel economy (mpg)", 28), ("price", "Fuel price ($ per gallon)", 3.5)],
  r"""const g=dist/mpg;
return [['Trip fuel cost',M(g*price)],['Fuel needed',N(g,2)+' gallons'],['Cost per mile',M(g*price/dist)]];""",
  "Fuel used is distance divided by fuel economy. Multiply by the price per gallon for the trip cost.",
  [("How can I lower fuel costs?", "Keep tires inflated, avoid hard acceleration, remove roof racks and slow down on highways.")]),

C("everyday", "electricity-cost-calculator", "Electricity Cost Calculator",
  "Find out what an appliance costs to run per day, month and year.",
  [("watts", "Power (watts)", 1500), ("hours", "Hours used per day", 4), ("price", "Electricity price ($ per kWh)", 0.16)],
  r"""const k=watts/1000*hours;
return [['Monthly cost',M(k*price*30)],['Daily cost',M(k*price)],['Yearly cost',M(k*price*365)],['Energy per day',N(k,2)+' kWh']];""",
  "Energy in kilowatt-hours equals watts / 1000 x hours. Multiply by your electricity rate for the cost.",
  [("Where do I find an appliance's wattage?", "It is on the label or in the manual. You can also measure it with a plug-in power meter.")]),

C("everyday", "unit-price-calculator", "Unit Price Calculator",
  "Compare two products to see which has the lower price per unit.",
  [("p1", "Product A price ($)", 4.99), ("q1", "Product A quantity", 12), ("p2", "Product B price ($)", 7.49), ("q2", "Product B quantity", 20)],
  r"""const a=p1/q1,b=p2/q2;
return [['Better value',a<b?'Product A':a>b?'Product B':'Same price'],['Product A per unit',M(a)],['Product B per unit',M(b)],['Difference',PCT(Math.abs(a-b)/Math.max(a,b)*100,1)]];""",
  "Unit price is the price divided by quantity. Use the same unit (ounces, count, litres) for both products.",
  [("Is the cheapest unit price always best?", "Not if you will not use it all before it spoils or expires.")]),

C("everyday", "final-grade-calculator", "Final Grade Calculator",
  "Find the score you need on a final exam to reach your target course grade.",
  [("cur", "Current grade (%)", 85), ("w", "Final exam weight (%)", 30), ("want", "Desired course grade (%)", 90)],
  r"""const need=(want-cur*(1-w/100))/(w/100);
return [['Score needed on final',PCT(need,1)],['Feasible?',need>100?'Above 100% - target may be out of reach':need<0?'You already have it':'Yes']];""",
  "Your course grade is current grade x (1 - final weight) + final score x final weight. The calculator solves for the final score.",
  [("What if I need more than 100%?", "Unless extra credit is offered, that grade is out of reach. Aim for the highest achievable grade.")]),

C("everyday", "day-of-week-calculator", "Day of the Week Calculator",
  "Find out which day of the week any date falls on.",
  [("date", "Date", "today", "date")],
  r"""const x=D(date),start=new Date(x.getFullYear(),0,0),doy=Math.round((x-start)/864e5);
return [['Day of the week',DS(x).split(',')[0]],['Full date',DS(x)],['Day of the year',doy],['Leap year?',(x.getFullYear()%4===0&&x.getFullYear()%100!==0)||x.getFullYear()%400===0?'Yes':'No']];""",
  "The weekday is calculated from the Gregorian calendar, so it works for any date, past or future.",
  [("What day was I born?", "Enter your birth date above to see your birth weekday.")]),
]

CONSTRUCTION = [
C("construction", "paint-calculator", "Paint Calculator",
  "Estimate how many gallons of paint you need for a room.",
  [("l", "Room length (ft)", 14), ("w", "Room width (ft)", 12), ("h", "Ceiling height (ft)", 8), ("doors", "Number of doors", 2), ("wins", "Number of windows", 2), ("coats", "Coats", 2), ("cov", "Coverage (sq ft per gallon)", 350)],
  r"""const area=Math.max(2*(l+w)*h-doors*20-wins*15,0),gal=area*coats/cov;
return [['Paint needed',N(Math.ceil(gal*4)/4,2)+' gallons'],['Wall area to paint',N(area,0)+' sq ft'],['Exact amount',N(gal,2)+' gallons']];""",
  "Wall area is the room perimeter times height, minus about 20 sq ft per door and 15 sq ft per window. Gallons = area x coats / coverage per gallon.",
  [("Does this include the ceiling?", "No. Add length x width to the area if you are painting the ceiling too.")]),

C("construction", "concrete-calculator", "Concrete Calculator",
  "Calculate cubic yards and bags of concrete for a slab.",
  [("l", "Length (ft)", 10), ("w", "Width (ft)", 10), ("t", "Thickness (in)", 4)],
  r"""const cf=l*w*t/12,cy=cf/27;
return [['Concrete needed (+10% extra)',N(cy*1.1,2)+' cubic yards'],['Exact volume',N(cy,2)+' cubic yards'],['80 lb bags',N(Math.ceil(cf*1.1/0.6),0)],['60 lb bags',N(Math.ceil(cf*1.1/0.45),0)]];""",
  "Volume equals length x width x thickness, converted to cubic yards. A 10% allowance covers spillage and uneven ground. An 80 lb bag yields about 0.6 cubic feet.",
  [("How thick should a slab be?", "4 inches is common for patios and walkways. Driveways usually need 5-6 inches.")]),

C("construction", "flooring-calculator", "Flooring Calculator",
  "Work out how much flooring to buy including waste, and what it will cost.",
  [("l", "Room length (ft)", 15), ("w", "Room width (ft)", 12), ("waste", "Waste allowance (%)", 10), ("price", "Price ($ per sq ft)", 3.5)],
  r"""const a=l*w,b=a*(1+waste/100);
return [['Flooring to buy',N(b,1)+' sq ft'],['Room area',N(a,1)+' sq ft'],['Estimated cost',M(b*price)]];""",
  "Room area is length x width. Add 5-10% for cuts and mistakes, and 15% or more for diagonal patterns.",
  [("Should I buy extra flooring?", "Yes. Extra boxes cover cuts, damage and future repairs, and dye lots can differ between batches.")]),

C("construction", "tile-calculator", "Tile Calculator",
  "Calculate how many tiles you need for a floor or wall.",
  [("l", "Area length (ft)", 10), ("w", "Area width (ft)", 8), ("tw", "Tile width (in)", 12), ("th", "Tile height (in)", 12), ("waste", "Waste allowance (%)", 10)],
  r"""const area=l*w*144,tile=tw*th,n=Math.ceil(area/tile*(1+waste/100));
return [['Tiles to buy',N(n,0)],['Area',N(l*w,1)+' sq ft'],['Tiles without waste',N(Math.ceil(area/tile),0)]];""",
  "Divide the area by the area of one tile and add a waste allowance for cuts and breakage.",
  [("Does grout spacing matter?", "Slightly. Wide grout lines reduce the number of tiles, but the difference is usually within the waste allowance.")]),

C("construction", "gravel-calculator", "Gravel Calculator",
  "Estimate cubic yards and tons of gravel for a driveway or garden bed.",
  [("l", "Length (ft)", 20), ("w", "Width (ft)", 10), ("d", "Depth (in)", 3)],
  r"""const cy=l*w*d/12/27;
return [['Gravel needed',N(cy,2)+' cubic yards'],['Weight (approx.)',N(cy*1.4,2)+' tons'],['With 10% extra',N(cy*1.1,2)+' cubic yards']];""",
  "Volume is length x width x depth in cubic yards. Gravel weighs about 1.4 tons per cubic yard, depending on type and moisture.",
  [("How deep should gravel be?", "A driveway typically uses 4-6 inches, and a path or garden bed 2-3 inches.")]),

C("construction", "board-feet-calculator", "Board Feet Calculator",
  "Calculate board feet of lumber and the total price.",
  [("t", "Thickness (in)", 2), ("w", "Width (in)", 6), ("l", "Length (ft)", 8), ("q", "Quantity", 10), ("price", "Price per board foot ($)", 4)],
  r"""const bf=t*w*l/12*q;
return [['Board feet',N(bf,2)],['Total cost',M(bf*price)],['Per board',N(t*w*l/12,2)+' bf']];""",
  "One board foot is a piece 1 inch thick, 12 inches wide and 12 inches long (144 cubic inches). Board feet = thickness (in) x width (in) x length (ft) / 12.",
  [("Are nominal sizes accurate?", "No. A '2x4' is actually 1.5 x 3.5 inches, but lumber is usually priced by its nominal size.")]),
]

SCIENCE = [
C("science", "speed-calculator", "Speed, Distance and Time Calculator",
  "Calculate average speed from distance and travel time.",
  [("dist", "Distance (km)", 100), ("h", "Hours", 1), ("m", "Minutes", 30)],
  r"""const t=h+m/60;if(t<=0)return 'Time must be greater than zero.';
return [['Average speed',N(dist/t,2)+' km/h'],['In miles per hour',N(dist/t/1.609344,2)+' mph'],['In metres per second',N(dist/t/3.6,2)+' m/s']];""",
  "Speed = distance / time. Enter the total time in hours and minutes.",
  [("How do I find distance or time?", "Rearrange: distance = speed x time and time = distance / speed.")]),

C("science", "ohms-law-calculator", "Ohm's Law Calculator",
  "Find current and power from voltage and resistance.",
  [("v", "Voltage (V)", 12), ("r", "Resistance (Ω)", 6)],
  r"""const i=v/r;
return [['Current',N(i,4)+' A'],['Power',N(v*i,4)+' W'],['Energy per hour',N(v*i/1000,4)+' kWh']];""",
  "Ohm's law: V = I x R. Power is P = V x I. Given voltage and resistance, current is I = V / R.",
  [("What is Ohm's law?", "It states that the current through a conductor is proportional to the voltage across it and inversely proportional to its resistance.")]),

C("science", "kinetic-energy-calculator", "Kinetic Energy Calculator",
  "Calculate kinetic energy and momentum from mass and velocity.",
  [("m", "Mass (kg)", 70), ("v", "Velocity (m/s)", 10)],
  r"""return [['Kinetic energy',N(0.5*m*v*v,4)+' J'],['Momentum',N(m*v,4)+' kg·m/s'],['In food calories',N(0.5*m*v*v/4184,6)+' kcal']];""",
  "Kinetic energy is KE = ½mv². Doubling the speed quadruples the energy.",
  [("Why does speed matter so much?", "Energy grows with the square of velocity, which is why high-speed crashes are far more destructive.")]),

C("science", "density-calculator", "Density Calculator",
  "Calculate density from mass and volume.",
  [("m", "Mass (g)", 500), ("v", "Volume (cm³)", 250)],
  r"""const d=m/v;
return [['Density',N(d,4)+' g/cm³'],['In kg/m³',N(d*1000,2)],['In lb/ft³',N(d*62.428,2)],['Floats in water?',d<1?'Yes':'No']];""",
  "Density = mass / volume. Water is 1 g/cm³ at 4 °C, so objects with a lower density float.",
  [("What are common densities?", "Water 1.0, aluminium 2.7, iron 7.87 and gold 19.3 g/cm³.")]),

C("science", "force-calculator", "Force Calculator (F = ma)",
  "Calculate force from mass and acceleration using Newton's second law.",
  [("m", "Mass (kg)", 10), ("a", "Acceleration (m/s²)", 9.81)],
  r"""const f=m*a;
return [['Force',N(f,4)+' N'],['In pound-force',N(f*0.224809,4)+' lbf'],['In kilogram-force',N(f/9.80665,4)+' kgf']];""",
  "Newton's second law states F = m x a. One newton accelerates one kilogram at one metre per second squared.",
  [("What is the weight of an object?", "Weight is the gravitational force on it: mass x 9.81 m/s² on Earth.")]),

C("science", "half-life-calculator", "Half-Life Calculator",
  "Calculate how much of a substance remains after a given time.",
  [("n0", "Initial amount", 100), ("hl", "Half-life", 5730), ("t", "Time elapsed (same unit as half-life)", 10000)],
  r"""const f=Math.pow(0.5,t/hl);
return [['Amount remaining',N(n0*f,6)],['Fraction remaining',PCT(f*100,4)],['Half-lives elapsed',N(t/hl,4)]];""",
  "Remaining amount N = N₀ x (½)^(t / half-life). Each half-life halves what is left. The default is carbon-14 (5,730 years).",
  [("Does half-life depend on the amount?", "No. It is constant for a given isotope regardless of the starting quantity.")]),

C("science", "weight-on-other-planets-calculator", "Weight on Other Planets Calculator",
  "See what you would weigh on the Moon, Mars, Jupiter and other worlds.",
  [("w", "Your weight on Earth (kg or lb)", 70)],
  r"""const g={Moon:1.62,Mercury:3.7,Venus:8.87,Mars:3.71,Jupiter:24.79,Saturn:10.44,Uranus:8.69,Neptune:11.15,Pluto:0.62};
return [['On the Moon',N(w*g.Moon/9.80665,1)],...Object.keys(g).filter(k=>k!=='Moon').map(k=>['On '+k,N(w*g[k]/9.80665,1)])];""",
  "Your mass stays constant but weight depends on local gravity. Each result scales your Earth weight by the planet's surface gravity relative to Earth's 9.81 m/s².",
  [("Would I be heavier on Jupiter?", "Yes, about 2.5 times heavier. On the Moon you would weigh about one sixth as much.")]),
]

SPECS = CONV + EVERYDAY + CONSTRUCTION + SCIENCE
