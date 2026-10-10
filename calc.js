// Shared runtime + helpers used by every calculator page.
const $=id=>document.getElementById(id);
const M=x=>Number.isFinite(x)?x.toLocaleString('en-US',{style:'currency',currency:'USD'}):'—';
const N=(x,d=2)=>Number.isFinite(x)?x.toLocaleString('en-US',{maximumFractionDigits:d}):'—';
const SF=x=>{if(!Number.isFinite(x))return '—';if(x===0)return '0';const a=Math.abs(x);
  if(a>=1e-4&&a<1e12)return Number(x.toPrecision(10)).toLocaleString('en-US',{maximumFractionDigits:12});
  return x.toExponential(6).replace(/\.?0+e/,'e');};
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

// Two-way equation engine: fill any (N-1) fields and the remaining one is solved.
// cfg.vars: [{id, units:[[label,factor,offset?]], init}], cfg.solve: {id: fn | [[requiredIds, fn],...]}
// cfg.need: how many fields must be entered (default N-1). The most recently edited fields are the inputs.
function EqPage(cfg){
  const V=cfg.vars,by={};V.forEach(v=>by[v.id]=v);
  const need=cfg.need||V.length-1;
  const form=document.querySelector('form[data-calc]'),out=$('out'),note=$('eqnote');
  const el={},sel={};V.forEach(v=>{el[v.id]=$(v.id);sel[v.id]=$(v.id+'_u');});
  const U=v=>(sel[v.id]&&v.units)?v.units[sel[v.id].selectedIndex]:['',1,0];
  const toB=(v,x)=>(x+(U(v)[2]||0))*U(v)[1];
  const fromB=(v,b)=>b/U(v)[1]-(U(v)[2]||0);
  const fmt=x=>Number.isFinite(x)?String(Number(x.toPrecision(10))):'';
  const alts=id=>{const s=cfg.solve[id];return !s?[]:(typeof s==='function'?[[null,s]]:s);};
  let order=[];
  const hint='Type in any '+need+' field'+(need>1?'s':'')+' and the rest are calculated (the '+(need>1?need+' you edited last are':'one you edited last is')+' used). Press Clear to start over.';
  function compute(){
    const ins=order.filter(id=>el[id].value!==''&&!isNaN(parseFloat(el[id].value))).slice(-need);
    const known={};ins.forEach(id=>known[id]=toB(by[id],parseFloat(el[id].value)));
    V.forEach(v=>{el[v.id].classList.remove('computed');if(!ins.includes(v.id))el[v.id].value='';});
    out.innerHTML='';
    if(ins.length<need){note.textContent=hint;return;}
    const sol=Object.assign({},known);let changed=true,guard=0;
    while(changed&&guard++<6){changed=false;
      V.forEach(v=>{if(v.id in sol)return;
        for(const a of alts(v.id)){
          const ok=a[0]?a[0].every(r=>r in sol):V.every(w=>w.id===v.id||w.id in sol);
          if(!ok)continue;let r;try{r=a[1](sol);}catch(e){r=NaN;}
          if(Number.isFinite(r)){sol[v.id]=r;changed=true;break;}
        }});}
    let bad=false;
    V.forEach(v=>{if(ins.includes(v.id))return;
      if(v.id in sol){el[v.id].value=fmt(fromB(v,sol[v.id]));el[v.id].classList.add('computed');}else bad=true;});
    note.textContent=bad?'No valid result for these values. Check for zero, negative or impossible numbers.':hint;
    if(!bad&&cfg.extra){try{out.innerHTML=cfg.extra(sol).map(([k,x])=>'<div class="row"><span>'+k+'</span><b>'+x+'</b></div>').join('');}catch(e){}}
  }
  V.forEach(v=>{
    el[v.id].addEventListener('input',()=>{order=order.filter(x=>x!==v.id);if(el[v.id].value!=='')order.push(v.id);compute();});
    if(sel[v.id])sel[v.id].addEventListener('change',compute);
  });
  const init=()=>{order=[];V.forEach(v=>{if(v.init!==undefined&&v.init!==null){el[v.id].value=v.init;order.push(v.id);}});compute();};
  form.addEventListener('submit',e=>e.preventDefault());
  form.addEventListener('reset',()=>setTimeout(()=>{order=[];V.forEach(v=>{el[v.id].value='';});compute();},0));
  init();
}
