from spec import C

SEX = [(1, "Male"), (2, "Female")]

HEALTH = [
C("health", "bmi-calculator", "BMI Calculator",
  "Calculate your body mass index and see which weight category you fall in.",
  [("units", "Units", 1, [(1, "Metric (kg, cm)"), (2, "Imperial (lb, in)")]), ("weight", "Weight (kg or lb)", 70), ("height", "Height (cm or in)", 175)],
  r"""const bmi=units==1?weight/Math.pow(height/100,2):703*weight/(height*height);
const cat=bmi<18.5?'Underweight':bmi<25?'Healthy weight':bmi<30?'Overweight':'Obesity';
return [['Your BMI',N(bmi,1)],['Category',cat]];""",
  "BMI is weight in kilograms divided by height in metres squared. A BMI of 18.5-24.9 is classed as healthy, 25-29.9 as overweight and 30 or more as obesity.",
  [("Is BMI accurate?", "BMI is a quick screening tool. It does not distinguish muscle from fat, so athletes can score high without excess body fat."),
   ("Does BMI differ for children?", "Yes. Children and teens use age and sex percentiles rather than the adult cutoffs shown here.")]),

C("health", "bmr-calculator", "BMR Calculator",
  "Estimate the calories your body burns at rest using the Mifflin-St Jeor equation.",
  [("sex", "Sex", 1, SEX), ("age", "Age (years)", 30), ("weight", "Weight (kg)", 70), ("height", "Height (cm)", 175)],
  r"""const b=10*weight+6.25*height-5*age+(sex==1?5:-161);
return [['Basal metabolic rate',N(b,0)+' kcal/day'],['Per hour',N(b/24,0)+' kcal']];""",
  "The Mifflin-St Jeor equation estimates resting energy use from weight, height, age and sex. It is among the most accurate predictive formulas for most adults.",
  [("What is BMR?", "Basal metabolic rate is the energy your body needs at complete rest to keep organs working, breathing and circulating blood.")]),

C("health", "calorie-calculator", "Calorie Calculator (TDEE)",
  "Find your daily calorie needs to maintain, lose or gain weight.",
  [("sex", "Sex", 1, SEX), ("age", "Age (years)", 30), ("weight", "Weight (kg)", 70), ("height", "Height (cm)", 175),
   ("act", "Activity level", 1.375, [(1.2, "Sedentary (little exercise)"), (1.375, "Light (1-3 days/week)"), (1.55, "Moderate (3-5 days/week)"), (1.725, "Very active (6-7 days/week)"), (1.9, "Extra active (physical job)")])],
  r"""const bmr=10*weight+6.25*height-5*age+(sex==1?5:-161),t=bmr*act;
return [['Maintain weight',N(t,0)+' kcal/day'],['Lose about 0.5 kg/week',N(t-500,0)+' kcal/day'],['Lose about 1 kg/week',N(t-1000,0)+' kcal/day'],['Gain about 0.5 kg/week',N(t+500,0)+' kcal/day'],['BMR',N(bmr,0)+' kcal/day']];""",
  "Total daily energy expenditure (TDEE) is your BMR multiplied by an activity factor. Eating about 500 calories below it leads to roughly 0.5 kg (1 lb) of weight loss per week.",
  [("How low should I go on calories?", "Avoid dropping below about 1,200 kcal (women) or 1,500 kcal (men) per day without medical supervision.")]),

C("health", "body-fat-calculator", "Body Fat Calculator",
  "Estimate body fat percentage with the US Navy tape-measure method.",
  [("sex", "Sex", 1, SEX), ("height", "Height (cm)", 175), ("neck", "Neck (cm)", 38), ("waist", "Waist at navel (cm)", 85), ("hip", "Hip (cm, women only)", 95)],
  r"""let bf;
if(sex==1){if(waist<=neck)return 'Waist must be larger than neck.';bf=495/(1.0324-0.19077*Math.log10(waist-neck)+0.15456*Math.log10(height))-450;}
else{if(waist+hip<=neck)return 'Check your measurements.';bf=495/(1.29579-0.35004*Math.log10(waist+hip-neck)+0.22100*Math.log10(height))-450;}
const c=sex==1?(bf<6?'Essential':bf<14?'Athletic':bf<18?'Fit':bf<25?'Average':'Above average'):(bf<14?'Essential':bf<21?'Athletic':bf<25?'Fit':bf<32?'Average':'Above average');
return [['Body fat',PCT(bf,1)],['Category',c]];""",
  "The US Navy method estimates body fat from height and circumference measurements of the neck, waist and (for women) hips. It is convenient but less accurate than DEXA scans.",
  [("How do I measure correctly?", "Use a flexible tape, measure on bare skin, keep it level and snug but not tight, and measure the waist at the navel.")]),

C("health", "ideal-weight-calculator", "Ideal Weight Calculator",
  "Estimate a healthy weight range for your height using standard formulas.",
  [("sex", "Sex", 1, SEX), ("height", "Height (cm)", 175)],
  r"""const over=Math.max(height/2.54-60,0);
const dev=(sex==1?50:45.5)+2.3*over,rob=(sex==1?52:49)+(sex==1?1.9:1.7)*over,mil=(sex==1?56.2:53.1)+(sex==1?1.41:1.36)*over;
const f=k=>N(k,1)+' kg ('+N(k*2.20462,0)+' lb)';
return [['Devine formula',f(dev)],['Robinson formula',f(rob)],['Miller formula',f(mil)],['Healthy BMI range (18.5-24.9)',f(18.5*Math.pow(height/100,2))+' to '+f(24.9*Math.pow(height/100,2))]];""",
  "Several formulas estimate ideal weight from height and sex. The healthy BMI range gives a wider and often more useful target.",
  [("Which formula is best?", "None is perfect. Treat them as rough guides and use the BMI range for a broader healthy window.")]),

C("health", "water-intake-calculator", "Water Intake Calculator",
  "Estimate how much water you should drink each day.",
  [("weight", "Weight (kg)", 70), ("mins", "Exercise per day (minutes)", 30)],
  r"""const l=weight*0.033+mins/30*0.35;
return [['Daily water',N(l,1)+' litres'],['In ounces',N(l*33.814,0)+' fl oz'],['In 250 ml glasses',N(l/0.25,0)]];""",
  "A common estimate is about 33 ml per kilogram of body weight, plus roughly 350 ml for every 30 minutes of exercise.",
  [("Does food count toward water intake?", "Yes. Food provides roughly 20% of daily fluid. Needs also rise in heat and at altitude.")]),

C("health", "due-date-calculator", "Pregnancy Due Date Calculator",
  "Estimate your due date from the first day of your last period.",
  [("lmp", "First day of last period", "today", "date")],
  r"""const l=D(lmp),add=d=>{const x=new Date(l);x.setDate(x.getDate()+d);return DS(x);};
const days=Math.floor((new Date()-l)/864e5);
return [['Estimated due date',add(280)],['Conception (approx.)',add(14)],['End of first trimester',add(91)],['Start of third trimester',add(189)],['Today you are',days>=0?Math.floor(days/7)+' weeks '+days%7+' days':'in the future']];""",
  "Naegele's rule adds 280 days (40 weeks) to the first day of your last menstrual period. Only about 5% of babies arrive on the exact due date.",
  [("How accurate is the due date?", "It is an estimate. An early ultrasound gives a more precise date, and your doctor or midwife will confirm it.")]),

C("health", "macro-calculator", "Macro Calculator",
  "Split your daily calories into protein, carbs and fat grams.",
  [("cal", "Daily calories", 2000), ("split", "Diet type", 1, [(1, "Balanced (40% carbs, 30% protein, 30% fat)"), (2, "Low carb (20% carbs, 40% protein, 40% fat)"), (3, "High protein (35% carbs, 40% protein, 25% fat)")])],
  r"""const s={1:[40,30,30],2:[20,40,40],3:[35,40,25]}[split];
return [['Carbohydrates',N(cal*s[0]/100/4,0)+' g'],['Protein',N(cal*s[1]/100/4,0)+' g'],['Fat',N(cal*s[2]/100/9,0)+' g']];""",
  "Protein and carbohydrates provide 4 calories per gram and fat provides 9. Each share of your calories is divided by those values to get grams.",
  [("How much protein do I need?", "Many adults aim for 1.2-2.0 g per kilogram of body weight depending on activity and goals.")]),

C("health", "pace-calculator", "Running Pace Calculator",
  "Find your running pace and speed from distance and time.",
  [("dist", "Distance (km)", 10), ("h", "Hours", 0), ("m", "Minutes", 50), ("s", "Seconds", 0)],
  r"""const t=h*3600+m*60+s;if(t<=0||dist<=0)return 'Enter a distance and time.';
const pk=t/dist,mm=x=>Math.floor(x/60)+':'+String(Math.round(x%60)).padStart(2,'0');
return [['Pace per km',mm(pk)],['Pace per mile',mm(pk*1.609344)],['Speed',N(dist/(t/3600),2)+' km/h'],['Speed',N(dist/1.609344/(t/3600),2)+' mph']];""",
  "Pace is total time divided by distance. This tool reports it per kilometre and per mile, plus average speed.",
  [("What is a good 10K pace?", "Recreational runners often finish 10K in 50-70 minutes, a pace of about 5:00-7:00 per km.")]),

C("health", "heart-rate-calculator", "Target Heart Rate Calculator",
  "Find your heart rate training zones with the Karvonen method.",
  [("age", "Age (years)", 30), ("rest", "Resting heart rate (bpm)", 60)],
  r"""const mx=220-age,z=p=>N(rest+(mx-rest)*p,0);
return [['Estimated max heart rate',mx+' bpm'],['Zone 1 - recovery (50-60%)',z(.5)+' - '+z(.6)+' bpm'],['Zone 2 - fat burn (60-70%)',z(.6)+' - '+z(.7)+' bpm'],['Zone 3 - aerobic (70-80%)',z(.7)+' - '+z(.8)+' bpm'],['Zone 4 - threshold (80-90%)',z(.8)+' - '+z(.9)+' bpm'],['Zone 5 - maximum (90-100%)',z(.9)+' - '+z(1)+' bpm']];""",
  "Maximum heart rate is estimated as 220 minus your age. The Karvonen method uses heart rate reserve (max minus resting) to set each training zone.",
  [("How do I measure resting heart rate?", "Count your pulse for 60 seconds first thing in the morning before getting out of bed.")]),

C("health", "one-rep-max-calculator", "One Rep Max Calculator",
  "Estimate your one-rep max (1RM) from a lighter set of repetitions.",
  [("w", "Weight lifted", 100), ("reps", "Repetitions", 5)],
  r"""if(reps<1||reps>36)return 'Use between 1 and 36 reps.';
const ep=w*(1+reps/30),br=w*36/(37-reps);
return [['Estimated 1RM (average)',N((ep+br)/2,1)],['Epley formula',N(ep,1)],['Brzycki formula',N(br,1)],['85% of 1RM',N((ep+br)/2*.85,1)],['70% of 1RM',N((ep+br)/2*.7,1)]];""",
  "The Epley and Brzycki formulas estimate the maximum weight you could lift once from a set of several reps. Estimates are most reliable under 10 reps.",
  [("Is it safe to test a true 1RM?", "Testing a true max carries injury risk. Estimating from a submaximal set with a spotter is safer.")]),
]

MATH = [
C("math", "percentage-calculator", "Percentage Calculator",
  "Find a percentage of a number, what percent one number is of another, and more.",
  [("x", "Percentage / first number (X)", 15), ("y", "Second number (Y)", 200)],
  r"""return [[N(x)+'% of '+N(y),N(x/100*y,4)],[N(x)+' is what % of '+N(y),PCT(x/y*100,4)],[N(y)+' increased by '+N(x)+'%',N(y*(1+x/100),4)],[N(y)+' decreased by '+N(x)+'%',N(y*(1-x/100),4)]];""",
  "To find X% of Y multiply Y by X/100. To find what percent X is of Y divide X by Y and multiply by 100.",
  [("How do I calculate a percentage of a number?", "Divide the percentage by 100 and multiply by the number. For example 15% of 200 is 0.15 x 200 = 30.")]),

C("math", "percent-change-calculator", "Percent Change Calculator",
  "Calculate the percentage increase or decrease between two numbers.",
  [("a", "Old value", 80), ("b", "New value", 100)],
  r"""const c=(b-a)/Math.abs(a)*100;
return [[c>=0?'Percent increase':'Percent decrease',PCT(Math.abs(c),4)],['Absolute change',N(b-a,4)]];""",
  "Percent change = (new value - old value) / |old value| x 100. A positive result is an increase and a negative result is a decrease.",
  [("Why isn't a 50% rise followed by a 50% fall back to the start?", "The fall applies to the larger number. 100 up 50% is 150, and 150 down 50% is 75.")]),

C("math", "percentage-difference-calculator", "Percentage Difference Calculator",
  "Compare two values by percentage difference, independent of which is larger.",
  [("a", "First value", 80), ("b", "Second value", 100)],
  r"""return [['Percentage difference',PCT(Math.abs(a-b)/((a+b)/2)*100,4)],['Absolute difference',N(Math.abs(a-b),4)],['Average of the two',N((a+b)/2,4)]];""",
  "Percentage difference divides the absolute difference by the average of the two values. Use it when neither value is the clear starting point.",
  [("Percentage difference vs percent change?", "Percent change has a baseline (old to new). Percentage difference treats both values symmetrically.")]),

C("math", "average-calculator", "Average Calculator (Mean, Median, Mode)",
  "Find the mean, median, mode, range and sum of a list of numbers.",
  [("list", "Numbers (separated by commas or spaces)", "4, 8, 15, 16, 23, 42", "text")],
  r"""const a=NUMS(list);if(!a.length)return 'Enter at least one number.';
const s=[...a].sort((x,y)=>x-y),n=a.length,sum=a.reduce((x,y)=>x+y,0);
const med=n%2?s[(n-1)/2]:(s[n/2-1]+s[n/2])/2;
const cnt={};a.forEach(v=>cnt[v]=(cnt[v]||0)+1);const mx=Math.max(...Object.values(cnt));
const mode=mx===1?'No mode':Object.keys(cnt).filter(k=>cnt[k]===mx).join(', ');
return [['Mean (average)',N(sum/n,6)],['Median',N(med,6)],['Mode',mode],['Range',N(s[n-1]-s[0],6)],['Sum',N(sum,6)],['Count',n],['Smallest',N(s[0],6)],['Largest',N(s[n-1],6)]];""",
  "The mean is the sum divided by the count. The median is the middle value when sorted. The mode is the most frequent value. The range is the largest minus the smallest.",
  [("When should I use median instead of mean?", "The median is better when data has extreme outliers, such as income or house prices.")]),

C("math", "standard-deviation-calculator", "Standard Deviation Calculator",
  "Calculate sample and population standard deviation and variance.",
  [("list", "Numbers (separated by commas or spaces)", "10, 12, 23, 23, 16, 23, 21, 16", "text")],
  r"""const a=NUMS(list),n=a.length;if(n<2)return 'Enter at least two numbers.';
const mean=a.reduce((x,y)=>x+y,0)/n,ss=a.reduce((x,y)=>x+(y-mean)*(y-mean),0);
return [['Sample standard deviation',N(Math.sqrt(ss/(n-1)),6)],['Population standard deviation',N(Math.sqrt(ss/n),6)],['Sample variance',N(ss/(n-1),6)],['Population variance',N(ss/n,6)],['Mean',N(mean,6)],['Count',n]];""",
  "Standard deviation measures how spread out numbers are around the mean. Use the sample version when your data is a sample of a larger group and the population version when it is the whole group.",
  [("Sample or population?", "If your numbers are every member of the group, use population. If they are a sample, use sample (divides by n-1).")]),

C("math", "quadratic-formula-calculator", "Quadratic Formula Calculator",
  "Solve ax² + bx + c = 0 and find the roots, including complex ones.",
  [("a", "a", 1), ("b", "b", -3), ("c", "c", 2)],
  r"""if(a===0)return 'a cannot be 0 in a quadratic equation.';
const d=b*b-4*a*c;
if(d>=0){const r=Math.sqrt(d);return [['Roots',N((-b+r)/(2*a),6)+' and '+N((-b-r)/(2*a),6)],['Discriminant',N(d,6)],['Vertex x',N(-b/(2*a),6)]];}
const re=-b/(2*a),im=Math.sqrt(-d)/(2*a);
return [['Complex roots',N(re,6)+' ± '+N(Math.abs(im),6)+'i'],['Discriminant',N(d,6)],['Vertex x',N(re,6)]];""",
  "The quadratic formula x = (-b ± √(b² - 4ac)) / 2a gives the solutions. A positive discriminant means two real roots, zero means one repeated root and negative means two complex roots.",
  [("What does the discriminant tell me?", "It is b² - 4ac. Its sign tells you how many real solutions the equation has.")]),

C("math", "pythagorean-theorem-calculator", "Pythagorean Theorem Calculator",
  "Find the hypotenuse of a right triangle from its two legs.",
  [("a", "Leg a", 3), ("b", "Leg b", 4)],
  r"""const c=Math.sqrt(a*a+b*b);
return [['Hypotenuse c',N(c,6)],['Area',N(a*b/2,6)],['Perimeter',N(a+b+c,6)],['Angle A',N(Math.atan(a/b)*180/Math.PI,4)+'°'],['Angle B',N(Math.atan(b/a)*180/Math.PI,4)+'°']];""",
  "For a right triangle a² + b² = c², where c is the hypotenuse opposite the right angle.",
  [("What is a Pythagorean triple?", "A set of three whole numbers satisfying a² + b² = c², such as 3-4-5 or 5-12-13.")]),

C("math", "circle-calculator", "Circle Calculator",
  "Calculate area, circumference and diameter of a circle from its radius.",
  [("r", "Radius", 5)],
  r"""return [['Area',N(Math.PI*r*r,6)],['Circumference',N(2*Math.PI*r,6)],['Diameter',N(2*r,6)]];""",
  "Area = πr², circumference = 2πr and diameter = 2r.",
  [("What is pi?", "Pi (π ≈ 3.14159) is the ratio of a circle's circumference to its diameter.")]),

C("math", "triangle-area-calculator", "Triangle Area Calculator",
  "Find the area of a triangle from its three sides using Heron's formula.",
  [("a", "Side a", 5), ("b", "Side b", 6), ("c", "Side c", 7)],
  r"""if(a+b<=c||a+c<=b||b+c<=a)return 'These sides cannot form a triangle.';
const s=(a+b+c)/2,ar=Math.sqrt(s*(s-a)*(s-b)*(s-c));
return [['Area',N(ar,6)],['Perimeter',N(a+b+c,6)],['Height from side a',N(2*ar/a,6)]];""",
  "Heron's formula: area = √(s(s-a)(s-b)(s-c)) where s is half the perimeter. It works for any triangle when you know all three sides.",
  [("Can any three lengths make a triangle?", "No. The sum of any two sides must be greater than the third.")]),

C("math", "gcd-lcm-calculator", "GCD and LCM Calculator",
  "Find the greatest common divisor and least common multiple of two numbers.",
  [("a", "First integer", 12), ("b", "Second integer", 18)],
  r"""a=Math.abs(Math.round(a));b=Math.abs(Math.round(b));if(!a||!b)return 'Enter non-zero integers.';
const g=(x,y)=>y?g(y,x%y):x,d=g(a,b);
return [['Greatest common divisor',N(d,0)],['Least common multiple',N(a/d*b,0)]];""",
  "The GCD is the largest number dividing both inputs. The LCM is the smallest number both divide into. They are linked by GCD x LCM = a x b.",
  [("What are GCD and LCM used for?", "Simplifying fractions uses the GCD. Adding fractions with different denominators uses the LCM.")]),

C("math", "prime-factorization-calculator", "Prime Factorization Calculator",
  "Break a number into its prime factors.",
  [("n", "Whole number (up to 1,000,000,000,000)", 360)],
  r"""n=Math.round(n);if(n<2||n>1e12)return 'Enter an integer from 2 to 1,000,000,000,000.';
let m=n;const f={};for(let p=2;p*p<=m;p++){while(m%p===0){f[p]=(f[p]||0)+1;m/=p;}}if(m>1)f[m]=(f[m]||0)+1;
const keys=Object.keys(f),str=keys.map(k=>f[k]>1?k+'^'+f[k]:k).join(' × ');
return [['Prime factors',str],['Is prime?',keys.length===1&&f[keys[0]]===1?'Yes':'No']];""",
  "Prime factorization writes a number as a product of primes. This tool divides out each prime from smallest to largest.",
  [("What is a prime number?", "A prime has exactly two factors: 1 and itself. The first primes are 2, 3, 5, 7, 11 and 13.")]),

C("math", "permutation-combination-calculator", "Permutation and Combination Calculator",
  "Calculate nPr and nCr for choosing r items from n.",
  [("n", "Total items (n)", 10), ("r", "Items chosen (r)", 3)],
  r"""n=Math.round(n);r=Math.round(r);if(r<0||r>n||n>170)return 'Use 0 ≤ r ≤ n ≤ 170.';
let p=1;for(let i=0;i<r;i++)p*=(n-i);let f=1;for(let i=2;i<=r;i++)f*=i;
return [['Combinations nCr',N(p/f,0)],['Permutations nPr',N(p,0)]];""",
  "A permutation counts ordered arrangements, nPr = n!/(n-r)!. A combination counts unordered selections, nCr = n!/(r!(n-r)!).",
  [("When do I use combinations vs permutations?", "Use permutations when order matters (race places) and combinations when it does not (lottery numbers).")]),

C("math", "slope-calculator", "Slope Calculator",
  "Find the slope, distance and midpoint between two points.",
  [("x1", "x₁", 1), ("y1", "y₁", 2), ("x2", "x₂", 4), ("y2", "y₂", 8)],
  r"""const dx=x2-x1,dy=y2-y1;
return [['Slope',dx===0?'Undefined (vertical line)':N(dy/dx,6)],['Distance',N(Math.hypot(dx,dy),6)],['Midpoint','('+N((x1+x2)/2,4)+', '+N((y1+y2)/2,4)+')'],['Angle',N(Math.atan2(dy,dx)*180/Math.PI,4)+'°']];""",
  "Slope is rise over run: (y₂ - y₁) / (x₂ - x₁). Distance uses the Pythagorean theorem and the midpoint averages the coordinates.",
  [("What does a negative slope mean?", "The line goes downward from left to right.")]),

C("math", "number-base-converter", "Binary, Hex and Octal Converter",
  "Convert a decimal number to binary, hexadecimal and octal.",
  [("n", "Decimal integer", 255)],
  r"""n=Math.trunc(n);if(!Number.isSafeInteger(n)||n<0)return 'Enter a non-negative integer.';
return [['Binary',n.toString(2)],['Hexadecimal',n.toString(16).toUpperCase()],['Octal',n.toString(8)]];""",
  "Number bases represent the same value with different digits: binary uses 0-1, octal 0-7 and hexadecimal 0-9 plus A-F.",
  [("Why do programmers use hexadecimal?", "One hex digit equals exactly four binary digits, making long binary values compact and readable.")]),

C("math", "volume-calculator", "Volume Calculator",
  "Calculate the volume of a sphere, cylinder, cone or cube.",
  [("shape", "Shape", 1, [(1, "Sphere (radius a)"), (2, "Cylinder (radius a, height h)"), (3, "Cone (radius a, height h)"), (4, "Cube (side a)")]),
   ("a", "Radius or side (a)", 5), ("h", "Height (h)", 10)],
  r"""const P=Math.PI,v={1:4/3*P*a*a*a,2:P*a*a*h,3:P*a*a*h/3,4:a*a*a}[shape];
return [['Volume',N(v,6)+' cubic units'],['In litres (if units are cm)',N(v/1000,6)]];""",
  "Sphere: 4/3 πr³. Cylinder: πr²h. Cone: ⅓πr²h. Cube: a³. Height is ignored for the sphere and cube.",
  [("What units does the volume use?", "Cubic units matching your input. If you enter centimetres the result is in cm³, and 1,000 cm³ equals one litre.")]),
]

SPECS = HEALTH + MATH
