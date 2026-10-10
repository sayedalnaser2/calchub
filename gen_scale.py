"""Programmatic calculator families. Each page gets its own computed tables and a working calculator."""
import math
from spec import C
from specs_c2 import fmt, kind_group

SPECS = []


def money(x, d=0):
    return f"${x:,.{d}f}"


def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="ref"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>\n'


def pmt(P, apr, n):
    r = apr / 1200
    return P / n if r == 0 else P * r / (1 - (1 + r) ** -n)


def bal(P, apr, n, k):
    r = apr / 1200
    p = pmt(P, apr, n)
    return P - p * k if r == 0 else P * (1 + r) ** k - p * ((1 + r) ** k - 1) / r


# ---------------------------------------------------------------- fuel economy
def fuel():
    # base: km per litre
    U = [("mpgus", "miles per gallon (US)", "mpg", "mile per gallon (US)", "x*0.425143707", "v/0.425143707"),
         ("mpguk", "miles per gallon (UK)", "mpg UK", "mile per gallon (UK)", "x*0.354006189", "v/0.354006189"),
         ("kml", "kilometers per liter", "km/L", "kilometer per liter", "x", "v"),
         ("l100", "liters per 100 kilometers", "L/100km", "liter per 100 kilometers", "100/x", "100/v")]
    for a in U:
        for b in U:
            if a[0] == b[0]:
                continue
            body = (f"const k=(x=>{a[4]})(v);const conv=v=>{b[5]};const r=conv(k);"
                    f"return [[N(v,4)+' {a[2]} =',N(r,4)+' {b[2]}'],"
                    f"...[10,15,20,25,30,35,40,50].map(x=>{{const kk=(x=>{a[4]})(x);return [N(x)+' {a[2]}',N(conv(kk),3)+' {b[2]}'];}})];")
            rows = []
            for x in (10, 15, 20, 25, 30, 35, 40, 50):
                k = {"mpgus": x * .425143707, "mpguk": x * .354006189, "kml": x, "l100": 100 / x}[a[0]]
                r = {"mpgus": k / .425143707, "mpguk": k / .354006189, "kml": k, "l100": 100 / k}[b[0]]
                rows.append((f"{x} {a[2]}", f"{r:.2f} {b[2]}"))
            extra = (f"<h2>{a[1].title()} to {b[1].title()} conversion table</h2>\n" + table([a[1].title(), b[1].title()], rows) +
                     "<h2>About fuel economy units</h2>\n<p>Fuel economy is reported as distance per volume of fuel (mpg, km/L) in the US, UK and much of Asia, "
                     "and as volume per distance (L/100 km) in Europe, Canada and Australia. Higher is better for distance-per-volume units, lower is better for L/100 km. "
                     "US and UK gallons differ (3.785 L vs 4.546 L), so mpg values are not interchangeable.</p>\n")
            slug = f"{a[1].split(' (')[0].replace(' ', '-')}-{a[0][-2:]}-to-{b[1].split(' (')[0].replace(' ', '-')}-{b[0][-2:]}"
            slug = f"{a[0]}-to-{b[0]}-fuel-economy"
            SPECS.append(C("conversion", slug, f"{a[1].title()} to {b[1].title()} Converter",
                           f"Convert {a[1]} to {b[1]} instantly.", [("v", f"Fuel economy in {a[1]}", 30)], body,
                           f"Fuel economy units are converted through kilometers per liter. The inverse relationship between distance-per-volume and volume-per-distance units means L/100 km = 100 / (km/L).",
                           [(f"What is 30 {a[2]} in {b[2]}?", f"30 {a[2]} is about " + next(r for x, r in rows if x.startswith("30 ")) + "."),
                            ("Which fuel economy unit is best?", "None is better; they measure the same thing. Use whichever your region's vehicles and fuel prices are quoted in.")],
                           extra, None, ("fuel-economy-conversions", "Fuel Economy Conversions", "Convert between mpg (US and UK), km/L and L/100 km.")))


fuel()

# ---------------------------------------------------------------- salary
HOUR_BODY = r"""const y=rate*hrs*wks;return [['Annual salary',M(y)],['Monthly',M(y/12)],['Biweekly',M(y/26)],['Weekly',M(rate*hrs)],['Daily (5 days)',M(rate*hrs/5)]];"""
SALARY_GROUP = ("salary-conversions", "Salary and Wage Conversions", "Convert hourly wages, monthly pay and annual salaries.")


def hourly(n):
    y = n * 2080
    rows = [(f"{h} hours", money(n * h, 2), money(n * h * 52 / 12, 0), money(n * h * 52, 0)) for h in (20, 25, 30, 35, 40, 45, 50)]
    extra = (f"<h2>${n} an hour at different hours per week</h2>\n" + table(["Hours per week", "Weekly", "Monthly", "Annual"], rows) +
             f"<h2>Take-home pay illustration</h2>\n<p>Gross pay of {money(y)} a year is before taxes and deductions. If roughly 20% were withheld, "
             f"take-home pay would be about {money(y * .8)} a year or {money(y * .8 / 12)} a month. Your real withholding depends on filing status, state and benefits.</p>\n")
    SPECS.append(C("finance", f"{n}-dollars-an-hour-is-how-much-a-year", f"${n} an Hour Is How Much a Year?",
                   f"${n} an hour is {money(y)} a year at 40 hours a week. Adjust hours and weeks for weekly, monthly and biweekly pay.",
                   [("rate", "Hourly rate ($)", n), ("hrs", "Hours per week", 40), ("wks", "Weeks worked per year", 52)], HOUR_BODY,
                   f"Annual pay is the hourly rate times hours per week times weeks per year. At ${n} an hour and 40 hours a week for 52 weeks, that is {money(y)}. Monthly pay divides the annual figure by 12.",
                   [(f"How much is ${n} an hour per month?", f"About {money(y / 12)} per month before taxes, at 40 hours a week."),
                    (f"How much is ${n} an hour biweekly?", f"About {money(n * 80)} every two weeks before taxes, at 40 hours a week.")],
                   extra, None, SALARY_GROUP))


for n in list(range(8, 101)) + list(range(105, 151, 5)):
    hourly(n)

YEAR_BODY = r"""const h=sal/(hrs*52);return [['Hourly wage',M(h)],['Monthly',M(sal/12)],['Biweekly',M(sal/26)],['Weekly',M(sal/52)],['Daily (5 days)',M(sal/260)]];"""


def yearly(n):
    rows = [(f"{h} hours", money(n / (h * 52), 2)) for h in (30, 35, 40, 45, 50)]
    extra = (f"<h2>{money(n)} a year as an hourly wage</h2>\n" + table(["Hours per week", "Hourly wage"], rows) +
             f"<h2>Other pay periods</h2>\n" + table(["Period", "Gross pay"], [("Monthly", money(n / 12, 2)), ("Semi-monthly", money(n / 24, 2)), ("Biweekly", money(n / 26, 2)), ("Weekly", money(n / 52, 2)), ("Daily (5 days)", money(n / 260, 2))]))
    SPECS.append(C("finance", f"{n}-a-year-is-how-much-per-hour", f"{money(n)} a Year Is How Much an Hour?",
                   f"{money(n)} a year is {money(n / 2080, 2)} an hour at 40 hours a week. See monthly, biweekly and weekly pay.",
                   [("sal", "Annual salary ($)", n), ("hrs", "Hours per week", 40)], YEAR_BODY,
                   f"Hourly pay is annual salary divided by the hours worked in a year. A full-time year is 40 hours x 52 weeks = 2,080 hours, so {money(n)} / 2,080 = {money(n / 2080, 2)} an hour, before taxes.",
                   [(f"What is {money(n)} a year per hour?", f"{money(n / 2080, 2)} an hour at 40 hours a week."),
                    (f"What is {money(n)} a year per month?", f"{money(n / 12, 2)} per month before taxes.")], extra, None, SALARY_GROUP))


for n in list(range(20000, 100001, 1000)) + list(range(105000, 300001, 5000)):
    yearly(n)

MONTH_BODY = r"""return [['Annual pay',M(mo*12)],['Weekly',M(mo*12/52)],['Biweekly',M(mo*12/26)],['Hourly (40 h/week)',M(mo*12/2080)]];"""


def monthly(n):
    extra = "<h2>Pay breakdown</h2>\n" + table(["Period", "Gross pay"], [("Annual", money(n * 12)), ("Weekly", money(n * 12 / 52, 2)), ("Biweekly", money(n * 12 / 26, 2)), ("Daily (5 days)", money(n * 12 / 260, 2)), ("Hourly at 40 h/week", money(n * 12 / 2080, 2)), ("Hourly at 35 h/week", money(n * 12 / 1820, 2))])
    SPECS.append(C("finance", f"{n}-a-month-is-how-much-a-year", f"{money(n)} a Month Is How Much a Year?",
                   f"{money(n)} a month is {money(n * 12)} a year, or {money(n * 12 / 2080, 2)} an hour at 40 hours a week.",
                   [("mo", "Monthly pay ($)", n)], MONTH_BODY,
                   f"Annual pay is monthly pay times 12. {money(n)} x 12 = {money(n * 12)}. Dividing by 2,080 working hours gives the hourly equivalent.",
                   [(f"How much is {money(n)} a month per hour?", f"About {money(n * 12 / 2080, 2)} an hour at 40 hours a week."),
                    (f"How much is {money(n)} a month per week?", f"About {money(n * 12 / 52, 2)} a week.")], extra, None, SALARY_GROUP))


for n in range(1000, 20001, 500):
    monthly(n)

# ---------------------------------------------------------------- mortgage / auto / invest
LOAN_GROUP = ("loan-payment-calculators", "Loan Payment Calculators", "Monthly payment calculators for specific mortgage and car loan amounts.")
MORT_BODY = r"""const r=rate/1200,n=term*12;const p=r===0?amt/n:amt*r/(1-Math.pow(1+r,-n));const tot=p*n;return [['Monthly principal and interest',M(p)],['Monthly with tax and insurance',M(p+ti/12)],['Total interest',M(tot-amt)],['Total of payments',M(tot)]];"""


def mortgage(n):
    rows = []
    for rate in (4, 5, 6, 6.5, 7, 8, 9):
        rows.append((f"{rate}%", money(pmt(n, rate, 180), 0), money(pmt(n, rate, 240), 0), money(pmt(n, rate, 360), 0)))
    p = pmt(n, 6.5, 360)
    brow = [(f"Year {y}", money(bal(n, 6.5, 360, y * 12), 0), money(n - bal(n, 6.5, 360, y * 12), 0)) for y in (1, 5, 10, 15, 20, 25, 30)]
    extra = (f"<h2>Monthly payment on a {money(n)} mortgage</h2>\n<p>Principal and interest only, by rate and term:</p>\n" +
             table(["Interest rate", "15 years", "20 years", "30 years"], rows) +
             f"<h2>Loan balance over time (6.5%, 30 years)</h2>\n" + table(["After", "Remaining balance", "Principal paid"], brow) +
             f"<p>At 6.5% over 30 years the payment is {money(p, 2)} a month and total interest is {money(p * 360 - n)}.</p>\n")
    SPECS.append(C("finance", f"{n}-mortgage-payment-calculator", f"{money(n)} Mortgage Payment Calculator",
                   f"Monthly payment on a {money(n)} mortgage at any rate and term, including taxes and insurance.",
                   [("amt", "Loan amount ($)", n), ("rate", "Interest rate (%)", 6.5), ("term", "Term (years)", 30, [(15, "15 years"), (20, "20 years"), (30, "30 years")]),
                    ("ti", "Property tax + insurance per year ($)", round(n * .015))], MORT_BODY,
                   f"Monthly principal and interest comes from the standard amortization formula P x r / (1 - (1 + r)^-n), with r the monthly rate and n the number of payments. A {money(n)} loan at 6.5% for 30 years costs {money(p, 2)} a month before taxes and insurance.",
                   [(f"What is the monthly payment on a {money(n)} mortgage?", f"At 6.5% for 30 years, {money(p, 2)} a month for principal and interest."),
                    (f"How much interest will I pay on {money(n)}?", f"At 6.5% over 30 years, about {money(p * 360 - n)} in total interest.")],
                   extra, None, LOAN_GROUP))


for n in list(range(50000, 1000001, 10000)) + list(range(1100000, 2000001, 100000)):
    mortgage(n)

AUTO_BODY = r"""const r=rate/1200,n=term*12;const p=r===0?amt/n:amt*r/(1-Math.pow(1+r,-n));return [['Monthly payment',M(p)],['Total interest',M(p*n-amt)],['Total of payments',M(p*n)]];"""


def auto(n):
    rows = [(f"{t} months", *[money(pmt(n, rt, t), 0) for rt in (3, 5, 7, 9)]) for t in (36, 48, 60, 72, 84)]
    p = pmt(n, 7, 60)
    extra = f"<h2>Monthly payment on a {money(n)} car loan</h2>\n" + table(["Term", "3%", "5%", "7%", "9%"], rows) + f"<p>At 7% over 60 months, the payment is {money(p, 2)} and total interest is {money(p * 60 - n)}.</p>\n"
    SPECS.append(C("finance", f"{n}-car-loan-payment-calculator", f"{money(n)} Car Loan Payment Calculator",
                   f"Monthly payment and total interest on a {money(n)} auto loan.",
                   [("amt", "Loan amount ($)", n), ("rate", "Interest rate (APR %)", 7), ("term", "Term (years)", 5, [(3, "3 years"), (4, "4 years"), (5, "5 years"), (6, "6 years"), (7, "7 years")])], AUTO_BODY,
                   f"The payment uses the amortization formula P x r / (1 - (1 + r)^-n). A {money(n)} loan at 7% for 60 months costs {money(p, 2)} a month.",
                   [(f"What is the payment on a {money(n)} car loan?", f"About {money(p, 2)} a month at 7% for 5 years."),
                    ("Is a longer loan cheaper?", "It lowers the monthly payment but increases total interest.")], extra, None, LOAN_GROUP))


for n in list(range(5000, 60001, 1000)) + list(range(65000, 100001, 5000)):
    auto(n)

INV_BODY = r"""const r=rate/1200,k=yrs*12;const fv=r===0?mo*k:mo*(Math.pow(1+r,k)-1)/r;return [['Future value',M(fv)],['Total contributed',M(mo*k)],['Growth earned',M(fv-mo*k)]];"""
INV_GROUP = ("investment-growth-calculators", "Investment Growth Calculators", "See what regular investing and lump sums can grow to.")


def fvm(m, rate, yrs):
    r = rate / 1200
    k = yrs * 12
    return m * k if r == 0 else m * ((1 + r) ** k - 1) / r


def invest(n):
    rows = [(f"{y} years", *[money(fvm(n, rt, y)) for rt in (5, 7, 10)]) for y in (5, 10, 20, 30, 40)]
    f30 = fvm(n, 7, 30)
    extra = f"<h2>What {money(n)} a month grows to</h2>\n" + table(["Time", "5% return", "7% return", "10% return"], rows) + "<p>Returns are illustrations with monthly compounding, not guarantees. Real investments fluctuate.</p>\n"
    SPECS.append(C("finance", f"investing-{n}-a-month-calculator", f"Investing {money(n)} a Month: How Much Will You Have?",
                   f"{money(n)} invested every month grows to {money(f30)} in 30 years at 7%.",
                   [("mo", "Monthly investment ($)", n), ("rate", "Annual return (%)", 7), ("yrs", "Years", 30)], INV_BODY,
                   f"The future value of regular deposits is M x ((1 + r)^k - 1) / r with a monthly rate r and k months. {money(n)} a month for 30 years at 7% grows to about {money(f30)}, of which {money(n * 360)} is your own money.",
                   [(f"How much is {money(n)} a month after 30 years?", f"About {money(f30)} at 7% a year."),
                    ("What return should I assume?", "Long-run stock market averages are often quoted around 7% after inflation to 10% before it, but actual returns vary widely.")],
                   extra, None, INV_GROUP))


for n in (25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 700, 750, 800, 1000, 1200, 1500, 2000, 2500, 3000):
    invest(n)

LUMP_BODY = r"""const fv=amt*Math.pow(1+rate/1200,yrs*12);return [['Future value',M(fv)],['Growth earned',M(fv-amt)],['Growth multiple',N(fv/amt,2)+'x']];"""


def lump(n):
    rows = [(f"{y} years", *[money(n * (1 + rt / 1200) ** (12 * y)) for rt in (4, 6, 8, 10)]) for y in (5, 10, 20, 30)]
    f = n * (1 + .07 / 12) ** 120
    extra = f"<h2>What {money(n)} grows to</h2>\n" + table(["Time", "4%", "6%", "8%", "10%"], rows)
    SPECS.append(C("finance", f"{n}-compound-interest-calculator", f"{money(n)} Compound Interest Calculator",
                   f"See what {money(n)} grows to with monthly compounding.",
                   [("amt", "Starting amount ($)", n), ("rate", "Annual interest rate (%)", 7), ("yrs", "Years", 10)], LUMP_BODY,
                   f"With monthly compounding, FV = P x (1 + r/12)^(12 x years). {money(n)} at 7% for 10 years grows to about {money(f)}.",
                   [(f"How long to double {money(n)}?", "Divide 72 by the annual rate for a quick estimate: about 10 years at 7%."),
                    ("Does compounding frequency matter?", "Slightly. More frequent compounding earns a little more.")], extra, None, INV_GROUP))


for n in (1000, 2500, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 75000, 100000, 150000, 200000, 250000, 500000, 1000000):
    lump(n)

# ---------------------------------------------------------------- BMI / ideal weight
HEALTH_GROUP = ("bmi-by-height", "BMI Calculators by Height", "Body mass index charts and calculators for each height.")
IDEAL_GROUP = ("ideal-weight-by-height", "Ideal Weight by Height", "Ideal body weight estimates for each height.")


def bmi_ranges_lb(hin):
    return {k: v * hin * hin / 703 for k, v in (("a", 18.5), ("b", 25), ("c", 30), ("d", 35), ("e", 40))}


def bmi_extra(hin, unit_cm=False):
    r = bmi_ranges_lb(hin)
    rows = [("Underweight", f"under {r['a']:.0f} lb ({r['a'] * .4536:.0f} kg)", "below 18.5"),
            ("Healthy weight", f"{r['a']:.0f} to {r['b']:.0f} lb ({r['a'] * .4536:.0f} to {r['b'] * .4536:.0f} kg)", "18.5 to 24.9"),
            ("Overweight", f"{r['b']:.0f} to {r['c']:.0f} lb ({r['b'] * .4536:.0f} to {r['c'] * .4536:.0f} kg)", "25 to 29.9"),
            ("Obesity class 1", f"{r['c']:.0f} to {r['d']:.0f} lb ({r['c'] * .4536:.0f} to {r['d'] * .4536:.0f} kg)", "30 to 34.9"),
            ("Obesity class 2", f"{r['d']:.0f} to {r['e']:.0f} lb ({r['d'] * .4536:.0f} to {r['e'] * .4536:.0f} kg)", "35 to 39.9"),
            ("Obesity class 3", f"over {r['e']:.0f} lb ({r['e'] * .4536:.0f} kg)", "40 and above")]
    return ("<h2>BMI weight ranges for this height</h2>\n" + table(["Category", "Weight", "BMI"], rows) +
            "<p>BMI is a screening tool. It does not measure body fat directly and can misclassify very muscular people, older adults and some ethnic groups. Talk to a doctor about your health.</p>\n")


BMI_LB = r"""const b=703*lb/(h*h);const c=b<18.5?'Underweight':b<25?'Healthy weight':b<30?'Overweight':'Obese';return [['Your BMI',N(b,1)],['Category',c],['Healthy range for this height',N(18.5*h*h/703,0)+' - '+N(24.9*h*h/703,0)+' lb']];"""
BMI_KG = r"""const b=kg/Math.pow(cm/100,2);const c=b<18.5?'Underweight':b<25?'Healthy weight':b<30?'Overweight':'Obese';return [['Your BMI',N(b,1)],['Category',c],['Healthy range for this height',N(18.5*Math.pow(cm/100,2),0)+' - '+N(24.9*Math.pow(cm/100,2),0)+' kg']];"""


def bmi_in(hin):
    ft, i = divmod(hin, 12)
    cm = hin * 2.54
    mid = round(22 * hin * hin / 703)
    SPECS.append(C("health", f"bmi-for-{ft}-ft-{i}-in", f"BMI for {ft} ft {i} in ({cm:.0f} cm)",
                   f"Check your BMI at {ft} ft {i} in and see the healthy weight range for this height.",
                   [("lb", "Weight (lb)", mid), ("h", "Height (inches)", hin)], BMI_LB,
                   f"BMI = 703 x weight (lb) / height (in) squared. At {ft} ft {i} in ({hin} inches), a healthy BMI of 18.5-24.9 corresponds to {18.5 * hin * hin / 703:.0f}-{24.9 * hin * hin / 703:.0f} lb.",
                   [(f"What is a healthy weight at {ft} ft {i} in?", f"Roughly {18.5 * hin * hin / 703:.0f} to {24.9 * hin * hin / 703:.0f} lb for a BMI between 18.5 and 24.9."),
                    ("Is BMI accurate?", "It is a rough screening measure; body composition and age matter.")],
                   bmi_extra(hin), None, HEALTH_GROUP))


def bmi_cm(cm):
    hin = cm / 2.54
    SPECS.append(C("health", f"bmi-for-{cm}-cm", f"BMI for {cm} cm ({int(hin // 12)} ft {hin % 12:.1f} in)",
                   f"Check your BMI at {cm} cm and see the healthy weight range for this height.",
                   [("kg", "Weight (kg)", round(22 * (cm / 100) ** 2)), ("cm", "Height (cm)", cm)], BMI_KG,
                   f"BMI = weight (kg) / height (m) squared. At {cm} cm, a healthy BMI of 18.5-24.9 corresponds to {18.5 * (cm / 100) ** 2:.0f}-{24.9 * (cm / 100) ** 2:.0f} kg.",
                   [(f"What is a healthy weight at {cm} cm?", f"Roughly {18.5 * (cm / 100) ** 2:.0f} to {24.9 * (cm / 100) ** 2:.0f} kg."),
                    ("Which BMI is considered overweight?", "25 to 29.9 is classed as overweight; 30 and above as obese.")],
                   bmi_extra(hin), None, HEALTH_GROUP))


for hin in range(56, 83):
    bmi_in(hin)
for cm in range(140, 211):
    bmi_cm(cm)

IDEAL_BODY = r"""const o=h-60;const d=sex?50+2.3*o:45.5+2.3*o,rb=sex?52+1.9*o:49+1.7*o,m=sex?56.2+1.41*o:53.1+1.36*o,hw=sex?48+2.7*o:45.5+2.2*o;const a=(d+rb+m+hw)/4;return [['Average of four formulas',N(a*2.2046,0)+' lb ('+N(a,0)+' kg)'],['Devine',N(d*2.2046,0)+' lb'],['Robinson',N(rb*2.2046,0)+' lb'],['Miller',N(m*2.2046,0)+' lb'],['Hamwi',N(hw*2.2046,0)+' lb']];"""


def ideal(hin):
    ft, i = divmod(hin, 12)
    o = hin - 60
    res = {}
    for sex in ("Men", "Women"):
        m = sex == "Men"
        f = [("Devine", (50 if m else 45.5) + 2.3 * o), ("Robinson", (52 if m else 49) + (1.9 if m else 1.7) * o),
             ("Miller", (56.2 if m else 53.1) + (1.41 if m else 1.36) * o), ("Hamwi", (48 if m else 45.5) + (2.7 if m else 2.2) * o)]
        res[sex] = f
    rows = [(n, f"{a * 2.2046:.0f} lb ({a:.0f} kg)", f"{b * 2.2046:.0f} lb ({b:.0f} kg)") for (n, a), (_, b) in zip(res["Men"], res["Women"])]
    avg_m = sum(x for _, x in res["Men"]) / 4
    avg_w = sum(x for _, x in res["Women"]) / 4
    extra = f"<h2>Ideal weight at {ft} ft {i} in by formula</h2>\n" + table(["Formula", "Men", "Women"], rows) + "<p>These formulas were designed for drug dosing, not health targets. A weight inside the healthy BMI range matters more than hitting any single number.</p>\n"
    SPECS.append(C("health", f"ideal-weight-for-{ft}-ft-{i}-in", f"Ideal Weight for {ft} ft {i} in",
                   f"Ideal body weight at {ft} ft {i} in using the Devine, Robinson, Miller and Hamwi formulas.",
                   [("sex", "Sex", 1, [(1, "Male"), (0, "Female")]), ("h", "Height (inches)", hin)], IDEAL_BODY,
                   f"Four common formulas estimate ideal body weight from height above 5 feet. At {ft} ft {i} in they average {avg_m * 2.2046:.0f} lb for men and {avg_w * 2.2046:.0f} lb for women.",
                   [(f"What is the ideal weight for a man {ft} ft {i} in?", f"About {avg_m * 2.2046:.0f} lb ({avg_m:.0f} kg) on average across four formulas."),
                    (f"What is the ideal weight for a woman {ft} ft {i} in?", f"About {avg_w * 2.2046:.0f} lb ({avg_w:.0f} kg) on average across four formulas.")],
                   extra, None, IDEAL_GROUP))


for hin in range(58, 83):
    ideal(hin)

# ---------------------------------------------------------------- cooking
COOK_GROUP = ("cooking-ingredient-conversions", "Cooking Ingredient Conversions", "Convert cups, tablespoons, teaspoons, ounces and grams for common ingredients.")
ING = [("All-Purpose Flour", "all-purpose-flour", 120), ("Bread Flour", "bread-flour", 120), ("Whole Wheat Flour", "whole-wheat-flour", 120), ("Cake Flour", "cake-flour", 114),
       ("Rye Flour", "rye-flour", 102), ("Almond Flour", "almond-flour", 96), ("Cornmeal", "cornmeal", 138), ("Cornstarch", "cornstarch", 112),
       ("Granulated Sugar", "granulated-sugar", 198), ("Brown Sugar (packed)", "brown-sugar", 213), ("Powdered Sugar", "powdered-sugar", 113),
       ("Honey", "honey", 336), ("Maple Syrup", "maple-syrup", 322), ("Molasses", "molasses", 336), ("Butter", "butter", 227), ("Vegetable Oil", "vegetable-oil", 218),
       ("Milk", "milk", 240), ("Heavy Cream", "heavy-cream", 238), ("Water", "water", 237), ("Yogurt", "yogurt", 245), ("Sour Cream", "sour-cream", 230),
       ("Cream Cheese", "cream-cheese", 227), ("Mayonnaise", "mayonnaise", 220), ("Ketchup", "ketchup", 240), ("Peanut Butter", "peanut-butter", 258),
       ("Rolled Oats", "rolled-oats", 90), ("White Rice (uncooked)", "white-rice", 185), ("Quinoa (uncooked)", "quinoa", 170), ("Lentils (dry)", "lentils", 192),
       ("Cocoa Powder", "cocoa-powder", 84), ("Chocolate Chips", "chocolate-chips", 170), ("Table Salt", "table-salt", 288), ("Baking Powder", "baking-powder", 192),
       ("Shredded Cheddar Cheese", "shredded-cheddar", 113), ("Grated Parmesan", "grated-parmesan", 100), ("Breadcrumbs (dry)", "breadcrumbs", 108),
       ("Whole Almonds", "almonds", 142), ("Chopped Walnuts", "walnuts", 113), ("Pecan Halves", "pecans", 99), ("Raisins", "raisins", 149),
       ("Shredded Coconut", "shredded-coconut", 85), ("Semolina", "semolina", 163)]
OZ = 28.3495
COOK_TYPES = [
    ("cups", "g", "Cups", "Grams", "cups", "grams", lambda g: g, 1),
    ("grams", "c", "Grams", "Cups", "grams", "cups", lambda g: 1 / g, 100),
    ("tablespoons", "g", "Tablespoons", "Grams", "tablespoons", "grams", lambda g: g / 16, 1),
    ("teaspoons", "g", "Teaspoons", "Grams", "teaspoons", "grams", lambda g: g / 48, 1),
    ("ounces", "c", "Ounces", "Cups", "ounces", "cups", lambda g: OZ / g, 1),
]


def cook(name, stub, g):
    fr = [.25, 1 / 3, .5, 2 / 3, .75, 1, 1.5, 2, 3, 4]
    lab = {.25: "1/4", 1 / 3: "1/3", .5: "1/2", 2 / 3: "2/3", .75: "3/4"}
    rows = [(f"{lab.get(c, f'{c:g}')} cup", f"{c * g:.0f} g", f"{c * g / OZ:.1f} oz") for c in fr]
    ref = ("<h2>" + name + " cup measurements</h2>\n" + table(["Volume", "Weight (grams)", "Weight (ounces)"], rows) +
           f"<p>1 US cup of {name.lower()} weighs about {g} g ({g / OZ:.1f} oz), 1 tablespoon about {g / 16:.1f} g and 1 teaspoon about {g / 48:.1f} g. "
           "Weights vary with brand, moisture and how the ingredient is scooped or packed, so use a kitchen scale for baking. Values use the US cup of 236.6 mL.</p>\n")
    n = name.lower()
    for kind, unit, fu, tu, fw, tw, ratio, default in COOK_TYPES:
        slug = f"{fw}-of-{stub}-to-{tw}"
        k = ratio(g)
        if unit == "g":
            body = f"const r=v*{k!r};return [[N(v,4)+' {fw} of {n} =',N(r,2)+' g'],['In ounces',N(r/{OZ},2)+' oz'],['Per 1 {fw[:-1]}',N({k!r},2)+' g']];"
            faq = [(f"How many grams is 1 {fw[:-1]} of {n}?", f"{k:.1f} g."),
                   (f"How many grams are in 2 {fw} of {n}?", f"{2 * k:.1f} g.")]
        else:
            body = f"const r=v*{k!r};return [[N(v,4)+' {fw} of {n} =',N(r,3)+' cups'],['In tablespoons',N(r*16,2)+' tbsp'],['In teaspoons',N(r*48,1)+' tsp']];"
            faq = [(f"How many cups is {default} {fw[:-1] if default == 1 else fw} of {n}?", f"{default * k:.3f} cups."),
                   (f"How many cups is 500 {fw} of {n}?", f"{500 * k:.2f} cups.")]
        SPECS.append(C("conversion", slug, f"{fu} of {name} to {tu}",
                       f"Convert {fw} of {n} to {tw}. 1 cup of {n} weighs about {g} g.", [("v", f"Amount in {fw}", default)], body,
                       f"{name} is measured by weight or by volume depending on the recipe. Using about {g} g per US cup, convert {fw} to {tw} by multiplying by {k:.4g}.",
                       faq, ref, None, COOK_GROUP))


for ing in ING:
    cook(*ing)

# ---------------------------------------------------------------- fractions
FRAC_GROUP = ("fraction-to-decimal-conversions", "Fraction to Decimal Conversions", "Convert common fractions to decimals, percents and millimeters.")
FRAC_BODY = r"""if(d===0)return 'The denominator cannot be zero.';const g=GCD(n,d);return [[n+'/'+d+' as a decimal',N(n/d,8)],['As a percent',PCT(n/d*100,4)],['Simplified',(n/g)+'/'+(d/g)],['As inches in millimeters',N(n/d*25.4,3)+' mm'],['As inches in centimeters',N(n/d*2.54,4)+' cm']];"""


def fraction(n, d):
    val = n / d
    eq = ", ".join(f"{n * k}/{d * k}" for k in (2, 3, 4, 5, 6))
    dec = f"{val:.10f}".rstrip("0").rstrip(".")
    rep = f"{val:.6f}" if len(dec) >= 10 else dec
    extra = ("<h2>" + f"{n}/{d} conversions" + "</h2>\n" + table(["Form", "Value"], [("Decimal", dec if len(dec) < 10 else f"{rep}…"), ("Percent", f"{val * 100:.4f}".rstrip("0").rstrip(".") + "%"),
             ("Inches to millimeters", f"{val * 25.4:.3f} mm"), ("Inches to centimeters", f"{val * 2.54:.4f} cm"), ("Equivalent fractions", eq)]) +
             f"<p>To convert {n}/{d} to a decimal, divide the numerator {n} by the denominator {d}. Multiply by 100 for a percent.</p>\n")
    SPECS.append(C("math", f"{n}-{d}-as-a-decimal", f"{n}/{d} as a Decimal, Percent and Millimeters",
                   f"{n}/{d} as a decimal is {dec if len(dec) < 10 else rep + '…'}. See it as a percent and as inches in mm.",
                   [("n", "Numerator", n), ("d", "Denominator", d)], FRAC_BODY,
                   f"Divide the numerator by the denominator: {n} / {d} = {dec if len(dec) < 10 else rep + '…'}. As a percent that is {val * 100:.2f}%. If the fraction is a length in inches, it equals {val * 25.4:.2f} mm.",
                   [(f"What is {n}/{d} as a decimal?", f"{dec if len(dec) < 10 else rep + '…'}"), (f"What is {n}/{d} as a percent?", f"{val * 100:.2f}%")],
                   extra, None, FRAC_GROUP))


for d in list(range(2, 33)) + [64]:
    for n in range(1, d):
        if math.gcd(n, d) == 1:
            fraction(n, d)

# ---------------------------------------------------------------- sales tax by state
TAX_GROUP = ("sales-tax-by-state", "Sales Tax Calculators by State", "State sales tax calculators using each state's base rate.")
STATES = [("Alabama", 4), ("Alaska", 0), ("Arizona", 5.6), ("Arkansas", 6.5), ("California", 7.25), ("Colorado", 2.9), ("Connecticut", 6.35), ("Delaware", 0),
          ("Florida", 6), ("Georgia", 4), ("Hawaii", 4), ("Idaho", 6), ("Illinois", 6.25), ("Indiana", 7), ("Iowa", 6), ("Kansas", 6.5), ("Kentucky", 6),
          ("Louisiana", 5), ("Maine", 5.5), ("Maryland", 6), ("Massachusetts", 6.25), ("Michigan", 6), ("Minnesota", 6.875), ("Mississippi", 7), ("Missouri", 4.225),
          ("Montana", 0), ("Nebraska", 5.5), ("Nevada", 6.85), ("New Hampshire", 0), ("New Jersey", 6.625), ("New Mexico", 4.875), ("New York", 4),
          ("North Carolina", 4.75), ("North Dakota", 5), ("Ohio", 5.75), ("Oklahoma", 4.5), ("Oregon", 0), ("Pennsylvania", 6), ("Rhode Island", 7),
          ("South Carolina", 6), ("South Dakota", 4.2), ("Tennessee", 7), ("Texas", 6.25), ("Utah", 6.1), ("Vermont", 6), ("Virginia", 4.3), ("Washington", 6.5),
          ("West Virginia", 6), ("Wisconsin", 5), ("Wyoming", 4), ("District of Columbia", 6)]
TAX_BODY = r"""return [['Sales tax',M(p*rate/100)],['Total price',M(p*(1+rate/100))],['Tax rate',PCT(rate,3)]];"""


def state_tax(name, rate):
    rows = [(money(p), money(p * rate / 100, 2), money(p * (1 + rate / 100), 2)) for p in (10, 25, 50, 100, 250, 500, 1000)]
    note = ("has no statewide sales tax, though some localities may charge their own" if rate == 0 else f"charges a statewide base sales tax of {rate:g}%")
    extra = (f"<h2>{name} sales tax on common purchases</h2>\n" + table(["Price", "Sales tax", "Total"], rows) +
             f"<p>{name} {note}. Cities and counties often add local taxes on top, and some items such as groceries, clothing or medicine may be taxed differently. "
             "Enter your combined local rate above for an exact figure, and check the state revenue department for current rules.</p>\n")
    stub = name.lower().replace(" ", "-")
    SPECS.append(C("finance", f"{stub}-sales-tax-calculator", f"{name} Sales Tax Calculator",
                   f"Calculate sales tax and total price in {name} using the {rate:g}% state base rate (add your local rate for an exact total).",
                   [("p", "Price before tax ($)", 100), ("rate", "Sales tax rate (%)", rate)], TAX_BODY,
                   f"Sales tax = price x rate. {name} {note}. This calculator starts from the state base rate; change the rate to include county or city taxes.",
                   [(f"What is the sales tax rate in {name}?", f"The state base rate is {rate:g}%; local taxes may add more." if rate else f"{name} has no statewide sales tax."),
                    (f"How much is sales tax on $100 in {name}?", f"At the base rate, ${rate:.2f}.")], extra, None, TAX_GROUP))


for s in STATES:
    state_tax(*s)

if __name__ == "__main__":
    print(len(SPECS))
