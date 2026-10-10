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

function CalcPage(fn){
  const form=document.querySelector('form[data-calc]'),out=$('out');
  form.querySelectorAll('input[data-today]').forEach(i=>{i.value=todayStr();});
  const read=()=>{
    const v={};let bad=false;
    form.querySelectorAll('input,select').forEach(el=>{
      if(el.tagName==='SELECT'){v[el.id]=isNaN(el.value)?el.value:Number(el.value);}
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
