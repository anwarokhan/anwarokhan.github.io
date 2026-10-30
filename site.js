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
// Row-ordered masonry: each photo goes to the shortest column, so rank reads left to right
const wall=document.querySelector('.wall');
if(wall){const figs=[...wall.querySelectorAll(':scope > figure')];
 const lay=()=>{const n=innerWidth<640?1:innerWidth<1000?2:3;wall.classList.add('js');wall.innerHTML='';
  const cols=[...Array(n)].map(()=>{const c=document.createElement('div');c.className='col';wall.appendChild(c);return c}),h=Array(n).fill(0);
  figs.forEach(f=>{if(f.hidden){cols[0].appendChild(f);return}const img=f.querySelector('img');const r=(img.naturalHeight&&img.naturalWidth)?img.naturalHeight/img.naturalWidth:(+img.getAttribute('height')/+img.getAttribute('width')||0.75);const i=h.indexOf(Math.min(...h));cols[i].appendChild(f);h[i]+=r+0.12})};
 let w=0;const re=()=>{const n=innerWidth<640?1:innerWidth<1000?2:3;if(n!==w){w=n;lay()}};
 re();addEventListener('resize',re);
 document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{w=0;re()}));}
