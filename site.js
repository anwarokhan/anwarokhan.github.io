// Mobile menu
const btn=document.querySelector('.menu-btn'),nav=document.querySelector('#nav');
if(btn){btn.addEventListener('click',()=>{const o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o)})}
// Lightbox for any figure with data-full
const lb=document.querySelector('.lightbox');
if(lb){const img=lb.querySelector('img'),cap=lb.querySelector('figcaption');let last=null;
 const close=()=>{lb.classList.remove('open');img.src='';if(last)last.focus()};
 document.querySelectorAll('figure[data-full]').forEach(f=>{f.tabIndex=0;f.setAttribute('role','button');
  const open=()=>{last=f;img.src=f.dataset.full;img.alt=f.querySelector('img')?.alt||'';cap.textContent=(f.dataset.caption||'').replace(/^([^:]+):\s*/,'$1. ');lb.classList.add('open');lb.querySelector('button').focus()};
  f.addEventListener('click',open);f.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}})});
 lb.addEventListener('click',e=>{if(e.target===lb||e.target.tagName==='BUTTON')close()});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&lb.classList.contains('open'))close()})}
// Photo filters
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{
 document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',x===b));
 const k=b.dataset.filter;document.querySelectorAll('.wall figure[data-tags]').forEach(f=>f.hidden=k!=='all'&&!f.dataset.tags.split(' ').includes(k))}));
