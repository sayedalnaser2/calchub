const $=id=>document.getElementById(id);
const money=n=>n.toLocaleString(undefined,{style:'currency',currency:'USD',maximumFractionDigits:2});
const num=id=>parseFloat($(id).value)||0;
const rows=l=>l.map(([k,v])=>`<div class="row"><span>${k}</span><b>${v}</b></div>`).join('');

function payment(P,annualRate,months){
  const r=annualRate/100/12;
  return r===0?P/months:P*r/(1-Math.pow(1+r,-months));
}

const calcs={
  mortgage(){
    const price=num('price'),down=num('down'),rate=num('rate'),yrs=num('years');
    const tax=num('tax')/12,ins=num('ins')/12;
    const P=Math.max(price-down,0),n=yrs*12;
    const pi=payment(P,rate,n),total=pi+tax+ins;
    return `<div class="big">${money(total)}<small style="font-size:1rem"> /month</small></div>`+rows([
      ['Principal &amp; interest',money(pi)],['Property tax',money(tax)],['Home insurance',money(ins)],
      ['Loan amount',money(P)],['Total interest over loan',money(pi*n-P)],['Total paid (P&amp;I)',money(pi*n)]]);
  },
  loan(){
    const P=num('amount'),rate=num('rate'),n=num('months');
    const m=payment(P,rate,n);
    return `<div class="big">${money(m)}<small style="font-size:1rem"> /month</small></div>`+rows([
      ['Total interest',money(m*n-P)],['Total repaid',money(m*n)]]);
  },
  compound(){
    const P=num('principal'),c=num('contrib'),rate=num('rate')/100,yrs=num('years'),f=num('freq');
    let bal=P,contributed=P;
    const steps=Math.round(yrs*12);
    const mr=Math.pow(1+rate/f,f/12)-1;
    for(let i=0;i<steps;i++){bal=bal*(1+mr)+c;contributed+=c;}
    return `<div class="big">${money(bal)}</div>`+rows([
      ['Total contributed',money(contributed)],['Interest earned',money(bal-contributed)]]);
  },
  payoff(){
    let bal=num('balance');const apr=num('apr')/100/12,pay=num('pay');
    if(pay<=bal*apr) return '<b>Payment is too low to ever pay this off. Increase it above the monthly interest ('+money(bal*apr)+').</b>';
    let months=0,interest=0;
    while(bal>0&&months<1200){const i=bal*apr;interest+=i;bal=bal+i-pay;months++;}
    return `<div class="big">${Math.floor(months/12)} yrs ${months%12} mo</div>`+rows([
      ['Total interest paid',money(interest)],['Number of payments',months]]);
  }
};

document.querySelectorAll('form[data-calc]').forEach(f=>{
  const run=e=>{e&&e.preventDefault();$('out').innerHTML=calcs[f.dataset.calc]();$('out').hidden=false;};
  f.addEventListener('submit',run);
  f.addEventListener('input',run);
  run();
});
