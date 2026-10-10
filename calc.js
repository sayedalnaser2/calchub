// Shared runtime + helpers used by every calculator page.
const $=id=>document.getElementById(id);
const M=x=>Number.isFinite(x)?x.toLocaleString('en-US',{style:'currency',currency:'USD'}):'—';
const N=(x,d=2)=>Number.isFinite(x)?x.toLocaleString('en-US',{maximumFractionDigits:d}):'—';
const PCT=(x,d=2)=>Number.isFinite(x)?N(x,d)+'%':'—';
const PMT=(P,apr,n)=>{const r=apr/1200;return r===0?P/n:P*r/(1-Math.pow(1+r,-n));};
const D=s=>{const [y,m,d]=s.split('-').map(Number);return new Date(y,m-1,d);};
const DS=d=>d.toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
const todayStr=()=>{const t=new Date();return t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');};
const NUMS=s=>s.split(/[\s,;]+/).filter(x=>x!==''&&!isNaN(x)).map(Number);

// 2025 US federal brackets (estimates): [upper limit, rate]
const BRK={1:[[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[626350,.35],[Infinity,.37]],
2:[[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]],
3:[[17000,.10],[64850,.12],[103350,.22],[197300,.24],[250500,.32],[626350,.35],[Infinity,.37]]};
const STD={1:15750,2:31500,3:23625};
const FEDTAX=(ti,st)=>{let t=0,prev=0;for(const [lim,r] of BRK[st]){if(ti>prev)t+=(Math.min(ti,lim)-prev)*r;prev=lim;}return t;};
const MARG=(ti,st)=>{for(const [lim,r] of BRK[st]){if(ti<=lim)return r;}return .37;};
const ERF=x=>{const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+.3275911*x);
  return s*(1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-.284496736)*t+.254829592)*t*Math.exp(-x*x));};
const NCDF=z=>.5*(1+ERF(z/Math.SQRT2));
const GCD=(a,b)=>b?GCD(b,a%b):Math.abs(a);

function CalcPage(fn){
  const form=document.querySelector('form[data-calc]'),out=$('out');
  form.querySelectorAll('input[data-today]').forEach(i=>{i.value=todayStr();});
  const read=()=>{
    const v={};let bad=false;
    form.querySelectorAll('input,select,textarea').forEach(el=>{
      if(el.tagName==='TEXTAREA'){v[el.id]=el.value;if(!el.value.trim())bad=true;}
      else if(el.tagName==='SELECT'){v[el.id]=isNaN(el.value)?el.value:Number(el.value);}
      else if(['date','time','text'].includes(el.type)){v[el.id]=el.value;if(!el.value)bad=true;}
      else{const n=parseFloat(el.value);v[el.id]=n;if(isNaN(n))bad=true;}
    });
    return bad?null:v;
  };
  const run=e=>{
    if(e)e.preventDefault();
    const v=read();
    if(!v){out.innerHTML='<p class="muted">Fill in every field to see the result.</p>';return;}
    let res;
    try{res=fn(v);}catch(err){res='Could not calculate. Please check your numbers.';}
    if(typeof res==='string'){out.innerHTML='<p><b>'+res+'</b></p>';return;}
    const [h,...rest]=res;
    out.innerHTML='<div class="muted">'+h[0]+'</div><div class="big">'+h[1]+'</div>'+
      rest.map(([k,x])=>'<div class="row"><span>'+k+'</span><b>'+x+'</b></div>').join('');
  };
  form.addEventListener('submit',run);
  form.addEventListener('input',run);
  run();
}
