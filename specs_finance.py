from spec import C

SPECS = [
C("finance", "mortgage-calculator", "Mortgage Calculator",
  "Estimate your monthly mortgage payment including property tax and home insurance.",
  [("price", "Home price ($)", 350000), ("down", "Down payment ($)", 70000), ("rate", "Interest rate (% APR)", 6.5),
   ("years", "Loan term", 30, [(30, "30 years"), (20, "20 years"), (15, "15 years"), (10, "10 years")]),
   ("tax", "Property tax ($ per year)", 3500), ("ins", "Home insurance ($ per year)", 1200)],
  r"""const P=Math.max(price-down,0),n=years*12,pi=PMT(P,rate,n);
return [['Monthly payment',M(pi+tax/12+ins/12)],['Principal and interest',M(pi)],['Property tax',M(tax/12)],['Home insurance',M(ins/12)],['Loan amount',M(P)],['Total interest over the loan',M(pi*n-P)]];""",
  "Monthly principal and interest comes from the loan amount (price minus down payment), the interest rate and the term. Property tax and homeowners insurance are added as one-twelfth of the yearly cost, which is how most lenders collect them in escrow. Private mortgage insurance (PMI) is not included.",
  [("How much house can I afford?", "A common guideline is to keep housing costs under about 28% of gross monthly income and total debts under 36%."),
   ("Is a 15-year or 30-year mortgage better?", "A 15-year loan has higher payments but far less total interest. A 30-year loan has lower payments and more flexibility. Compare both above."),
   ("Does a bigger down payment help?", "Yes. It lowers the loan amount, the payment and total interest, and 20% or more usually avoids PMI.")]),

C("finance", "loan-calculator", "Loan Calculator",
  "Calculate the monthly payment and total interest on any fixed-rate loan.",
  [("amount", "Loan amount ($)", 20000), ("rate", "Interest rate (% APR)", 8), ("months", "Term (months)", 60)],
  r"""const m=PMT(amount,rate,months);
return [['Monthly payment',M(m)],['Total interest',M(m*months-amount)],['Total repaid',M(m*months)]];""",
  "Each payment covers interest on the remaining balance plus part of the principal. Early payments are mostly interest and later ones mostly principal. A shorter term or lower rate reduces the total interest.",
  [("How can I lower my loan cost?", "Improve your credit score before applying, compare lenders, choose a shorter term if you can afford it, and make extra principal payments."),
   ("What is APR?", "The annual percentage rate is the yearly cost of borrowing, including interest and some fees.")]),

C("finance", "compound-interest-calculator", "Compound Interest Calculator",
  "See how savings or investments grow with compound interest and monthly deposits.",
  [("principal", "Starting amount ($)", 5000), ("contrib", "Monthly contribution ($)", 300), ("rate", "Annual interest rate (%)", 7),
   ("years", "Years to grow", 20), ("freq", "Compounding", 12, [(12, "Monthly"), (365, "Daily"), (4, "Quarterly"), (1, "Yearly")])],
  r"""let bal=principal,paid=principal;const mr=Math.pow(1+rate/100/freq,freq/12)-1;
for(let i=0;i<Math.round(years*12);i++){bal=bal*(1+mr)+contrib;paid+=contrib;}
return [['Future balance',M(bal)],['Total contributed',M(paid)],['Interest earned',M(bal-paid)]];""",
  "Compound interest means you earn interest on your interest. Each month the balance grows by the effective monthly rate and your deposit is added. The longer the money stays invested, the faster it grows.",
  [("What return rate should I use?", "Savings accounts have recently paid roughly 3-5%. Long-run stock market averages are often quoted near 7% after inflation, but returns are never guaranteed."),
   ("Does compounding frequency matter?", "Slightly. Daily compounding earns a little more than yearly, but rate and time matter far more.")]),

C("finance", "credit-card-payoff-calculator", "Credit Card Payoff Calculator",
  "Find out how long it takes to pay off a credit card and how much interest you will pay.",
  [("balance", "Card balance ($)", 6000), ("apr", "Interest rate (% APR)", 22), ("pay", "Monthly payment ($)", 250)],
  r"""const r=apr/1200;let b=balance,months=0,interest=0;
if(pay<=b*r)return 'Your payment is too low to ever pay this off. It must be above the monthly interest of '+M(b*r)+'.';
while(b>0&&months<1200){const i=b*r;interest+=i;b=b+i-pay;months++;}
return [['Time to pay off',Math.floor(months/12)+' years '+months%12+' months'],['Total interest',M(interest)],['Number of payments',months]];""",
  "Credit card interest is charged monthly on the remaining balance. This calculator applies your fixed payment each month until the balance reaches zero. Two popular strategies are avalanche (highest rate first, saves the most money) and snowball (smallest balance first, builds momentum).",
  [("Why does the minimum payment take so long?", "Minimums are often only slightly above the monthly interest, so very little reduces the balance."),
   ("Should I use a balance transfer?", "A 0% intro APR transfer can save interest if you pay it off before the promotion ends and the fee is reasonable.")]),

C("finance", "simple-interest-calculator", "Simple Interest Calculator",
  "Calculate simple interest and the total amount owed or earned.",
  [("principal", "Principal ($)", 10000), ("rate", "Annual rate (%)", 5), ("years", "Time (years)", 3)],
  r"""const i=principal*rate/100*years;
return [['Interest',M(i)],['Total amount',M(principal+i)]];""",
  "Simple interest uses the formula I = P x r x t, where interest is calculated only on the original principal and never on accumulated interest.",
  [("What is the difference between simple and compound interest?", "Simple interest is earned on the principal only. Compound interest is also earned on previously added interest, so it grows faster.")]),

C("finance", "savings-goal-calculator", "Savings Goal Calculator",
  "Find the monthly amount you need to save to reach a target by a deadline.",
  [("goal", "Savings goal ($)", 50000), ("current", "Current savings ($)", 5000), ("rate", "Annual interest rate (%)", 5), ("years", "Years to reach goal", 10)],
  r"""const n=years*12,r=rate/1200,g=Math.pow(1+r,n),fvCur=current*g;
const need=Math.max(goal-fvCur,0),pmt=r===0?need/n:need*r/(g-1);
const total=fvCur+pmt*(r===0?n:(g-1)/r);
return [['Monthly savings needed',M(pmt)],['Total you deposit',M(pmt*n+current)],['Interest earned',M(total-pmt*n-current)],['Final balance',M(total)]];""",
  "Your existing savings grow at the interest rate, and the calculator finds the level monthly deposit that closes the remaining gap by the deadline.",
  [("What if I can't afford the monthly amount?", "Extend the time, lower the goal, or look for an account with a higher interest rate.")]),

C("finance", "retirement-calculator", "Retirement Savings Calculator",
  "Project your retirement savings and the income they could support.",
  [("age", "Current age", 30), ("retireAge", "Retirement age", 65), ("savings", "Current savings ($)", 20000),
   ("monthly", "Monthly contribution ($)", 500), ("rate", "Expected annual return (%)", 7)],
  r"""const n=Math.max(retireAge-age,0)*12,r=rate/1200,g=Math.pow(1+r,n);
const bal=savings*g+(r?monthly*(g-1)/r:monthly*n),paid=savings+monthly*n;
return [['Savings at retirement',M(bal)],['Total contributed',M(paid)],['Investment growth',M(bal-paid)],['Income, 4% rule (yearly)',M(bal*0.04)],['Income, 4% rule (monthly)',M(bal*0.04/12)]];""",
  "Your current savings and each monthly contribution compound until retirement. The 4% rule suggests withdrawing 4% of the balance in the first year of retirement as a sustainable starting income.",
  [("Is the 4% rule reliable?", "It is a rule of thumb based on historical US data for a 30-year retirement. Your own timeline, taxes and market conditions may differ."),
   ("Is the result adjusted for inflation?", "No. Use a return rate after inflation (for example 4-5% instead of 7%) to see results in today's dollars.")]),

C("finance", "auto-loan-calculator", "Auto Loan Calculator",
  "Estimate your monthly car payment including sales tax, down payment and trade-in.",
  [("price", "Vehicle price ($)", 30000), ("down", "Down payment ($)", 3000), ("trade", "Trade-in value ($)", 0),
   ("rate", "Interest rate (% APR)", 7), ("months", "Loan term (months)", 60), ("tax", "Sales tax (%)", 7)],
  r"""const taxAmt=Math.max(price-trade,0)*tax/100,P=Math.max(price-trade-down+taxAmt,0),m=PMT(P,rate,months);
return [['Monthly payment',M(m)],['Amount financed',M(P)],['Sales tax',M(taxAmt)],['Total interest',M(m*months-P)],['Total cost of loan',M(m*months+down+trade)]];""",
  "The amount financed is the vehicle price minus your trade-in and down payment, plus sales tax (calculated here on the price after trade-in). The payment is then calculated like any fixed-rate loan.",
  [("What loan term is best for a car?", "Shorter terms cost less in interest. Terms over 60-72 months often leave you owing more than the car is worth early on.")]),

C("finance", "sales-tax-calculator", "Sales Tax Calculator",
  "Add sales tax to a price or find the tax portion of a total.",
  [("amount", "Price before tax ($)", 100), ("rate", "Sales tax rate (%)", 8.25)],
  r"""const t=amount*rate/100;
return [['Total with tax',M(amount+t)],['Sales tax',M(t)],['Price before tax',M(amount)]];""",
  "Sales tax equals the pre-tax price multiplied by the tax rate. Add it to the price to get the total you pay.",
  [("What is my sales tax rate?", "It depends on your state, county and city. Check your local revenue department's website for the combined rate.")]),

C("finance", "tip-calculator", "Tip Calculator",
  "Work out the tip and split the bill between any number of people.",
  [("bill", "Bill amount ($)", 80), ("tip", "Tip (%)", 18), ("people", "Number of people", 2)],
  r"""const t=bill*tip/100,tot=bill+t;
return [['Each person pays',M(tot/people)],['Tip total',M(t)],['Total with tip',M(tot)],['Tip per person',M(t/people)]];""",
  "The tip is the bill multiplied by your tip percentage. The total is divided evenly by the number of people.",
  [("How much should I tip?", "In the US, 15-20% is typical at restaurants. Check local customs when traveling.")]),

C("finance", "discount-calculator", "Discount Calculator",
  "Calculate the sale price after a percentage discount, with an optional extra discount.",
  [("price", "Original price ($)", 100), ("disc", "Discount (%)", 25), ("extra", "Extra discount (%)", 0)],
  r"""const f=price*(1-disc/100)*(1-extra/100);
return [['Final price',M(f)],['You save',M(price-f)],['Total discount',PCT((1-f/price)*100)]];""",
  "Each discount is applied one after another to the remaining price. Two discounts of 25% and 10% equal 32.5% off, not 35%.",
  [("Why isn't a 25% plus 10% discount equal to 35%?", "The second discount applies to the already reduced price, so the total saving is slightly less than the sum.")]),

C("finance", "roi-calculator", "ROI Calculator",
  "Calculate return on investment and annualized return.",
  [("invested", "Amount invested ($)", 10000), ("final", "Final value ($)", 15000), ("years", "Years held", 3)],
  r"""const roi=(final-invested)/invested*100,ann=(Math.pow(final/invested,1/years)-1)*100;
return [['Return on investment',PCT(roi)],['Profit',M(final-invested)],['Annualized return',PCT(ann)]];""",
  "ROI is (final value - amount invested) / amount invested. Annualized return shows the equivalent steady yearly growth rate over the holding period.",
  [("What is a good ROI?", "It depends on the asset and risk. The stock market has historically averaged around 7-10% per year before inflation.")]),

C("finance", "inflation-calculator", "Inflation Calculator",
  "See how inflation changes what your money can buy in the future.",
  [("amount", "Amount today ($)", 1000), ("rate", "Average inflation rate (%)", 3), ("years", "Years", 10)],
  r"""const g=Math.pow(1+rate/100,years);
return [['Cost of the same goods later',M(amount*g)],['Purchasing power of today\'s money later',M(amount/g)],['Total price increase',PCT((g-1)*100)]];""",
  "At a steady inflation rate, prices grow by that percentage each year, so the same money buys less over time.",
  [("What inflation rate should I use?", "US inflation has averaged roughly 3% over the long term. Use a higher or lower figure to test scenarios.")]),

C("finance", "salary-calculator", "Salary Calculator (Hourly, Weekly, Monthly, Annual)",
  "Convert an hourly wage to weekly, monthly and yearly pay.",
  [("hourly", "Hourly rate ($)", 25), ("hours", "Hours per week", 40), ("weeks", "Weeks per year", 52)],
  r"""const y=hourly*hours*weeks;
return [['Yearly pay',M(y)],['Monthly pay',M(y/12)],['Weekly pay',M(hourly*hours)],['Daily pay (5 days)',M(hourly*hours/5)]];""",
  "Yearly pay is hourly rate times hours per week times weeks worked. Figures are before taxes and deductions.",
  [("Is this before or after tax?", "Before tax. Your take-home pay will be lower depending on income tax, Social Security and other deductions.")]),

C("finance", "break-even-calculator", "Break-Even Calculator",
  "Find how many units you must sell to cover your costs.",
  [("fixed", "Fixed costs ($)", 10000), ("price", "Selling price per unit ($)", 50), ("varc", "Variable cost per unit ($)", 30)],
  r"""if(price<=varc)return 'Selling price must be higher than variable cost.';
const u=fixed/(price-varc);
return [['Break-even units',N(Math.ceil(u),0)],['Break-even revenue',M(Math.ceil(u)*price)],['Contribution per unit',M(price-varc)]];""",
  "Break-even units equal fixed costs divided by the contribution margin (price minus variable cost per unit). Past that point each sale adds profit.",
  [("What are fixed and variable costs?", "Fixed costs (rent, salaries) stay the same regardless of sales. Variable costs (materials, shipping) grow with each unit sold.")]),

C("finance", "margin-calculator", "Profit Margin & Markup Calculator",
  "Calculate profit, gross margin and markup from cost and selling price.",
  [("cost", "Cost ($)", 60), ("price", "Selling price ($)", 100)],
  r"""const p=price-cost;
return [['Gross margin',PCT(p/price*100)],['Markup',PCT(p/cost*100)],['Profit',M(p)]];""",
  "Margin is profit as a share of the selling price. Markup is profit as a share of cost. A 50% markup equals a 33.3% margin.",
  [("What is the difference between margin and markup?", "Margin divides profit by price; markup divides profit by cost. Markup is always the larger number.")]),

C("finance", "cagr-calculator", "CAGR Calculator",
  "Calculate compound annual growth rate between two values.",
  [("start", "Beginning value ($)", 10000), ("end", "Ending value ($)", 25000), ("years", "Years", 5)],
  r"""return [['CAGR',PCT((Math.pow(end/start,1/years)-1)*100)],['Total growth',PCT((end/start-1)*100)]];""",
  "CAGR = (ending value / beginning value)^(1 / years) - 1. It is the steady annual rate that would turn the start value into the end value.",
  [("Is CAGR the same as average return?", "No. CAGR accounts for compounding and is usually lower than a simple arithmetic average of yearly returns.")]),

C("finance", "rule-of-72-calculator", "Rule of 72 Calculator",
  "Estimate how long it takes to double your money at a given rate.",
  [("rate", "Annual return (%)", 6)],
  r"""return [['Years to double (rule of 72)',N(72/rate,1)],['Exact years to double',N(Math.log(2)/Math.log(1+rate/100),1)],['Years to triple',N(Math.log(3)/Math.log(1+rate/100),1)]];""",
  "Divide 72 by the annual rate for a quick estimate of the years needed to double. The exact figure uses logarithms.",
  [("How accurate is the rule of 72?", "It is very close for rates between 4% and 12% and gets less precise outside that range.")]),

C("finance", "debt-to-income-calculator", "Debt-to-Income Ratio Calculator",
  "Calculate your DTI ratio, which lenders use to approve loans.",
  [("debts", "Monthly debt payments ($)", 1800), ("income", "Gross monthly income ($)", 6000)],
  r"""const d=debts/income*100;
const l=d<=20?'Excellent':d<=36?'Good':d<=43?'Acceptable':'High - may limit borrowing';
return [['Debt-to-income ratio',PCT(d,1)],['Rating',l]];""",
  "DTI is your total monthly debt payments divided by gross monthly income. Many mortgage lenders prefer 36% or lower and rarely approve above about 43-50%.",
  [("What counts as monthly debt?", "Mortgage or rent, car loans, student loans, credit card minimums and other loan payments. Utilities and groceries are not included.")]),

C("finance", "refinance-calculator", "Refinance Break-Even Calculator",
  "Find out how many months it takes for refinancing to pay for itself.",
  [("cur", "Current monthly payment ($)", 1800), ("newp", "New monthly payment ($)", 1650), ("closing", "Closing costs ($)", 4500)],
  r"""const s=cur-newp;
if(s<=0)return 'The new payment must be lower than the current one to break even.';
const m=closing/s;
return [['Break-even point',Math.ceil(m)+' months ('+N(m/12,1)+' years)'],['Monthly savings',M(s)],['Savings after 5 years',M(s*60-closing)]];""",
  "Divide the closing costs by your monthly savings to find the months needed to recoup them. If you will move before then, refinancing may not pay off.",
  [("Does this include the longer loan term?", "No. If you restart a 30-year term, you may pay more interest overall even with a lower payment.")]),

C("finance", "house-affordability-calculator", "House Affordability Calculator",
  "Estimate the maximum home price you can afford based on income and debts.",
  [("income", "Annual gross income ($)", 90000), ("debts", "Monthly debt payments ($)", 400), ("rate", "Interest rate (% APR)", 6.5),
   ("down", "Down payment ($)", 40000), ("term", "Loan term (years)", 30), ("ti", "Monthly tax and insurance ($)", 500)],
  r"""const m=income/12,maxHousing=Math.min(0.28*m,0.36*m-debts),maxPI=Math.max(maxHousing-ti,0);
const loan=maxPI/PMT(1,rate,term*12);
return [['Estimated home price',M(loan+down)],['Maximum loan',M(loan)],['Maximum monthly housing cost',M(maxHousing)],['Principal and interest budget',M(maxPI)]];""",
  "This uses the 28/36 rule: housing costs up to 28% of gross monthly income, and all debts including housing up to 36%. The lower limit sets your budget.",
  [("Can I afford more than this?", "Some lenders allow higher ratios, but a bigger payment leaves less room for savings and emergencies.")]),
]
