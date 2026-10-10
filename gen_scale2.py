"""More programmatic families: birth-year age pages, race pace charts, holiday countdowns."""
import datetime
from spec import C
from gen_scale import table

SPECS = []

# ---------------------------------------------------------------- born in year
AGE_GROUP = ("birth-year-age-calculators", "Age Calculators by Birth Year", "How old are you? Age, generation and Chinese zodiac for each birth year.")
ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
AGE_BODY = r"""const b=D(dob),t=new Date();t.setHours(0,0,0,0);let a=t.getFullYear()-b.getFullYear();if(t<new Date(t.getFullYear(),b.getMonth(),b.getDate()))a--;if(a<0)return 'Date of birth is in the future.';const days=Math.round((t-b)/864e5);let nx=new Date(t.getFullYear(),b.getMonth(),b.getDate());if(nx<t)nx=new Date(t.getFullYear()+1,b.getMonth(),b.getDate());const mo=(t.getFullYear()-b.getFullYear())*12+t.getMonth()-b.getMonth()-(t.getDate()<b.getDate()?1:0);return [['Your age',a+' years'],['In months',N(mo,0)],['Days alive',N(days,0)],['Weeks alive',N(days/7,0)],['Next birthday',DS(nx)],['Days until birthday',N(Math.round((nx-t)/864e5),0)]];"""


def generation(y):
    if y <= 1927: return "Greatest Generation"
    if y <= 1945: return "Silent Generation"
    if y <= 1964: return "Baby Boomer"
    if y <= 1980: return "Generation X"
    if y <= 1996: return "Millennial"
    if y <= 2012: return "Generation Z"
    return "Generation Alpha"


for y in range(1930, 2016):
    an = ANIMALS[(y - 4) % 12]
    el = ELEMENTS[((y - 4) % 10) // 2]
    gen = generation(y)
    rows = [(f"Turn {a}", str(y + a)) for a in (13, 16, 18, 21, 30, 40, 50, 60, 65, 70, 80, 90, 100)]
    extra = (f"<h2>Born in {y}: key facts</h2>\n" + table(["Fact", "Detail"], [("Generation", gen), ("Chinese zodiac", f"{el} {an}"), ("Leap year", "Yes" if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0 else "No")]) +
             f"<h2>Milestone ages for people born in {y}</h2>\n" + table(["Milestone", "Year"], rows) +
             "<p>Chinese zodiac animals change at Lunar New Year, which falls in late January or February, so people born in January or early February may belong to the previous animal. Age shown by the calculator depends on today's date and your exact birthday.</p>\n")
    SPECS.append(C("everyday", f"born-in-{y}-how-old-am-i", f"Born in {y}: How Old Am I?",
                   f"Find your exact age if you were born in {y}, plus days alive and your next birthday. {gen}, {el} {an}.",
                   [("dob", "Date of birth", f"{y}-06-15", "date")], AGE_BODY,
                   f"Age is the number of full years since your birth date. People born in {y} belong to {gen} and the Chinese zodiac year of the {el} {an}. Enter your exact birthday for an exact age.",
                   [(f"What generation is someone born in {y}?", f"{gen}."), (f"What is the Chinese zodiac for {y}?", f"{el} {an} (the zodiac year begins at Lunar New Year).")],
                   extra, None, AGE_GROUP))

# ---------------------------------------------------------------- race pace charts
PACE_GROUP = ("race-pace-charts", "Race Pace Charts", "Pace per mile and per kilometer needed for 5K, 10K, half marathon and marathon finish times.")
PACE_BODY = r"""const s=hh*3600+mm*60+ss;if(s<=0||dist<=0)return 'Enter a finish time.';const pkm=s/dist,pmi=pkm*1.609344;const f=x=>Math.floor(x/3600)>0?Math.floor(x/3600)+':'+String(Math.floor(x%3600/60)).padStart(2,'0')+':'+String(Math.round(x%60)).padStart(2,'0'):Math.floor(x/60)+':'+String(Math.round(x%60)).padStart(2,'0');return [['Pace per mile',f(pmi)],['Pace per kilometer',f(pkm)],['Speed',N(3600/pmi,2)+' mph / '+N(3600/pkm,2)+' km/h'],['5K at this pace',f(pkm*5)],['10K at this pace',f(pkm*10)],['Half marathon at this pace',f(pkm*21.0975)],['Marathon at this pace',f(pkm*42.195)]];"""


def fpace(x):
    x = round(x)
    return f"{x // 3600}:{x % 3600 // 60:02d}:{x % 60:02d}" if x >= 3600 else f"{x // 60}:{x % 60:02d}"


def race(label, dist, secs, slug_stub, tlabel):
    pkm = secs / dist
    pmi = pkm * 1.609344
    marks = [(f"{k} km", fpace(pkm * k)) for k in (1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40) if k <= dist]
    marks += [(f"{k} miles", fpace(pmi * k)) for k in (1, 2, 3, 5, 10, 13.1, 20, 26.2) if k * 1.609344 <= dist + 0.05]
    marks.append((f"Finish ({label})", fpace(secs)))
    extra = (f"<h2>Pace needed for a {tlabel} {label}</h2>\n" + table(["Measure", "Value"], [("Pace per mile", fpace(pmi)), ("Pace per kilometer", fpace(pkm)), ("Speed (mph)", f"{3600 / pmi:.2f}"), ("Speed (km/h)", f"{3600 / pkm:.2f}")]) +
             f"<h2>Split times at a constant pace</h2>\n" + table(["Distance", "Time"], marks) +
             "<p>Splits assume an even pace. Most runners benefit from starting slightly slower and finishing strong (a negative split).</p>\n")
    SPECS.append(C("health", f"{slug_stub}-pace-{tlabel.replace(':', '-')}", f"{label} Pace for a {tlabel} Finish Time",
                   f"To run a {label} in {tlabel} you need {fpace(pmi)} per mile ({fpace(pkm)} per km). See split times.",
                   [("hh", "Hours", int(secs // 3600)), ("mm", "Minutes", int(secs % 3600 // 60)), ("ss", "Seconds", int(secs % 60)),
                    ("dist", "Distance", dist, [(5, "5K"), (10, "10K"), (21.0975, "Half marathon"), (42.195, "Marathon")])], PACE_BODY,
                   f"Pace = finish time / distance. A {label} is {dist:g} km ({dist / 1.609344:.2f} miles), so {tlabel} works out to {fpace(pmi)} per mile or {fpace(pkm)} per kilometer.",
                   [(f"What pace is a {tlabel} {label}?", f"{fpace(pmi)} per mile ({fpace(pkm)} per km)."),
                    ("How fast is that in mph?", f"About {3600 / pmi:.2f} mph.")], extra, None, PACE_GROUP))


for m in range(15, 51):
    race("5K", 5, m * 60, "5k", f"{m}:00")
for m in range(30, 101, 2):
    race("10K", 10, m * 60, "10k", f"{m}:00")
for t in range(70, 191, 5):
    race("Half Marathon", 21.0975, t * 60, "half-marathon", f"{t // 60}:{t % 60:02d}:00")
for t in range(150, 391, 5):
    race("Marathon", 42.195, t * 60, "marathon", f"{t // 60}:{t % 60:02d}:00")

# ---------------------------------------------------------------- holiday countdowns
HOL_GROUP = ("holiday-countdowns", "Holiday Countdown Calculators", "How many days until Christmas, Thanksgiving, Halloween and other holidays.")


def nth_weekday(y, m, wd, n):
    d = datetime.date(y, m, 1)
    d += datetime.timedelta((wd - d.weekday()) % 7)
    return d + datetime.timedelta(7 * (n - 1))


def last_weekday(y, m, wd):
    d = datetime.date(y + (m == 12), m % 12 + 1, 1) - datetime.timedelta(1)
    return d - datetime.timedelta((d.weekday() - wd) % 7)


def easter(y):
    a = y % 19; b = y // 100; c = y % 100; d = b // 4; e = b % 4; f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30; i = c // 4; k = c % 4; l = (32 + 2 * e + 2 * i - h - k) % 7; m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31; da = (h + l - 7 * m + 114) % 31 + 1
    return datetime.date(y, mo, da)


JS_NTH = "const nth=(y,m,w,n)=>{const d=new Date(y,m,1);d.setDate(1+(w-d.getDay()+7)%7+7*(n-1));return d;};const last=(y,m,w)=>{const d=new Date(y,m+1,0);d.setDate(d.getDate()-(d.getDay()-w+7)%7);return d;};"
JS_EASTER = "const easter=y=>{const a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=(h+l-7*m+114)%31+1;return new Date(y,mo-1,da);};"
HOLS = [
    ("christmas", "Christmas", "new Date(y,11,25)", lambda y: datetime.date(y, 12, 25)),
    ("christmas-eve", "Christmas Eve", "new Date(y,11,24)", lambda y: datetime.date(y, 12, 24)),
    ("new-years-eve", "New Year's Eve", "new Date(y,11,31)", lambda y: datetime.date(y, 12, 31)),
    ("new-year", "New Year's Day", "new Date(y,0,1)", lambda y: datetime.date(y, 1, 1)),
    ("valentines-day", "Valentine's Day", "new Date(y,1,14)", lambda y: datetime.date(y, 2, 14)),
    ("st-patricks-day", "St. Patrick's Day", "new Date(y,2,17)", lambda y: datetime.date(y, 3, 17)),
    ("april-fools-day", "April Fools' Day", "new Date(y,3,1)", lambda y: datetime.date(y, 4, 1)),
    ("easter", "Easter", "easter(y)", easter),
    ("earth-day", "Earth Day", "new Date(y,3,22)", lambda y: datetime.date(y, 4, 22)),
    ("cinco-de-mayo", "Cinco de Mayo", "new Date(y,4,5)", lambda y: datetime.date(y, 5, 5)),
    ("mothers-day", "Mother's Day (US)", "nth(y,4,0,2)", lambda y: nth_weekday(y, 5, 6, 2)),
    ("memorial-day", "Memorial Day", "last(y,4,1)", lambda y: last_weekday(y, 5, 0)),
    ("fathers-day", "Father's Day (US)", "nth(y,5,0,3)", lambda y: nth_weekday(y, 6, 6, 3)),
    ("juneteenth", "Juneteenth", "new Date(y,5,19)", lambda y: datetime.date(y, 6, 19)),
    ("fourth-of-july", "the Fourth of July", "new Date(y,6,4)", lambda y: datetime.date(y, 7, 4)),
    ("labor-day", "Labor Day (US)", "nth(y,8,1,1)", lambda y: nth_weekday(y, 9, 0, 1)),
    ("halloween", "Halloween", "new Date(y,9,31)", lambda y: datetime.date(y, 10, 31)),
    ("veterans-day", "Veterans Day", "new Date(y,10,11)", lambda y: datetime.date(y, 11, 11)),
    ("thanksgiving", "Thanksgiving (US)", "nth(y,10,4,4)", lambda y: nth_weekday(y, 11, 3, 4)),
    ("black-friday", "Black Friday", "(()=>{const d=nth(y,10,4,4);d.setDate(d.getDate()+1);return d;})()", lambda y: nth_weekday(y, 11, 3, 4) + datetime.timedelta(1)),
    ("mlk-day", "Martin Luther King Jr. Day", "nth(y,0,1,3)", lambda y: nth_weekday(y, 1, 0, 3)),
    ("presidents-day", "Presidents' Day", "nth(y,1,1,3)", lambda y: nth_weekday(y, 2, 0, 3)),
    ("groundhog-day", "Groundhog Day", "new Date(y,1,2)", lambda y: datetime.date(y, 2, 2)),
]
for stub, name, js, py in HOLS:
    rows = [(str(y), py(y).strftime("%A, %B %d").replace(" 0", " ")) for y in range(2026, 2033)]
    body = (JS_NTH + JS_EASTER + f"const f=y=>{js};const t=new Date();t.setHours(0,0,0,0);let d=f(t.getFullYear());if(d<t)d=f(t.getFullYear()+1);"
            f"const days=Math.round((d-t)/864e5);return [['Days until {name.replace(chr(39), chr(92) + chr(39))}',days===0?'It is today!':N(days,0)],['Date',DS(d)],['Weeks',N(days/7,1)],['Hours',N(days*24,0)],['Minutes',N(days*1440,0)]];")
    extra = f"<h2>{name} dates for the next several years</h2>\n" + table(["Year", "Date"], rows)
    title = f"How Many Days Until {name}?"
    SPECS.append(C("everyday", f"days-until-{stub}", title, f"Live countdown showing the days, weeks and hours left until {name}.",
                   [], body, f"The countdown compares today's date with the next occurrence of {name}. If the holiday has passed this year it counts to next year's date. Moving holidays such as Easter or Thanksgiving are calculated from their calendar rules.",
                   [(f"When is {name} next year?", f"See the table above for dates over the coming years."), (f"Does the countdown update daily?", "Yes, it uses the date on your device each time you load the page.")],
                   extra, None, HOL_GROUP))
