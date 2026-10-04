/* RTT-001 colour search (IQ-13, DEC-173). One colour per browser for the whole film, near each browser's familiar brand
 * colour (palette_targets.json; first-pass hex values chosen by Claude from the browsers' logos, not official brand
 * specifications), under the house rules: every colour keeps white names readable (contrast >= 3.0 : 1) and stands out
 * from the background (>= 3.0 : 1), and no two browsers that can be on screen together (top 10 in the same month or
 * the three months before, as RTT-002's colour rule) are closer than CIEDE2000 18 (DEC-023). The eight main browsers
 * plus UC Browser and Samsung Internet were fixed by hand (FIX argument, as recorded in DEC-173); the others were found
 * by a seeded annealing search over a 5-step sRGB grid (deterministic). Colour-blind separation is reported, not
 * enforced (argument 1 = 0). Output: palette_out.json in the working directory.
 *
 *   node kits/rtt-001/palette_search.js 0 '<FIX json>'
 */
const TL=require('../rtt-002/rtt_timeline.js');
const d=require('./race_rtt001.json');
const MAT={protan:[[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]],
 deutan:[[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]]};
const lin=c=>{c/=255;return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4)}, delin=c=>{c=Math.min(1,Math.max(0,c));return Math.round(255*(c<=0.0031308?12.92*c:1.055*Math.pow(c,1/2.4)-0.055))};
const rgb=h=>{const n=parseInt(h.slice(1),16);return[(n>>16)&255,(n>>8)&255,n&255]}, hex=a=>'#'+a.map(v=>v.toString(16).padStart(2,'0')).join('').toUpperCase();
const sim=(h,m)=>{const v=rgb(h).map(lin);return hex(m.map(r=>delin(r[0]*v[0]+r[1]*v[1]+r[2]*v[2])))};
const lum=h=>{const[r,g,b]=rgb(h).map(lin);return 0.2126*r+0.7152*g+0.0722*b}, con=(a,b)=>{const x=lum(a),y=lum(b);return(Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)};
const names={};d.entrants.forEach(e=>names[e.id]=e.label);
let prev=[];const tops=[];
for(const e of d.events){const pos={};prev.forEach((b,i)=>pos[b]=i);
 const ids=Object.keys(e.values).sort((a,b)=>(e.values[b]-e.values[a])||((pos[a]??1e9)-(pos[b]??1e9))||(names[a]<names[b]?-1:1));tops.push(ids.slice(0,10));prev=ids;}
const adj={},months={};for(let k=0;k<tops.length;k++){tops[k].forEach(x=>months[x]=(months[x]||0)+1);const V=new Set();for(let j=Math.max(0,k-3);j<=k;j++)tops[j].forEach(x=>V.add(x));for(const a of V){adj[a]=adj[a]||new Set();for(const b of V)if(a!==b)adj[a].add(b)}}
const T=require('./palette_targets.json'); const MAJOR=new Set(T._major); delete T._major;
const CBT=+process.argv[2]||0; const FIX=JSON.parse(process.argv[3]||'{}');
const grid=[];for(let r=0;r<256;r+=5)for(let g=0;g<256;g+=5)for(let b=0;b<256;b+=5){const h=hex([r,g,b]);if(TL.drawnColour(h)!==h.toLowerCase())continue;if(con(h,'#F4F6FA')>=3.0&&con(h,'#0B1424')>=3.0)grid.push(h);}
for(const h of Object.values(FIX)) if(!grid.includes(h.toUpperCase())) grid.push(h.toUpperCase());
const ids=Object.keys(adj).sort(), N=grid.length;
// brand distance on the colours as given (no darkening of the target): how far the drawn bar is from the brand colour
const lab=h=>{const[r,g,b]=rgb(h).map(lin);const X=(0.4124*r+0.3576*g+0.1805*b)/0.95047,Y=0.2126*r+0.7152*g+0.0722*b,Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883;const f=t=>t>0.008856?Math.cbrt(t):7.787*t+16/116;return[116*f(Y)-16,500*(f(X)-f(Y)),200*(f(Y)-f(Z))]};
const de76=(a,b)=>{const A=lab(a),B=lab(b);return Math.hypot(A[0]-B[0],A[1]-B[1],A[2]-B[2])};
const brand={};for(const id of ids)brand[id]=grid.map(h=>Math.min(...T[id].map(x=>TL.deltaE(h,x))));
const w={};for(const id of ids)w[id]=(MAJOR.has(id)?6:1)*Math.sqrt(months[id]||1);
const cacheDE=new Map();const DE=(i,j)=>{if(i===j)return 0;const k=i<j?i*N+j:j*N+i;let v=cacheDE.get(k);if(v==null){v=TL.deltaE(grid[i],grid[j]);cacheDE.set(k,v)}return v};
const simG={protan:grid.map(h=>sim(h,MAT.protan)),deutan:grid.map(h=>sim(h,MAT.deutan))};
const cacheCB=new Map();const CB=(i,j)=>{const k=i<j?i*N+j:j*N+i;let v=cacheCB.get(k);if(v==null){v=Math.min(TL.deltaE(simG.protan[i],simG.protan[j]),TL.deltaE(simG.deutan[i],simG.deutan[j]));cacheCB.set(k,v)}return v};
const pairs=[];for(const a of ids)for(const b of adj[a])if(a<b)pairs.push([a,b]);
const nb={};for(const id of ids)nb[id]=[...adj[id]];
function cost(c){let s=0;for(const id of ids)s+=w[id]*brand[id][c[id]];for(const [a,b] of pairs){const x=DE(c[a],c[b]);if(x<18)s+=1000*(18-x);if(CBT&&MAJOR.has(a)&&MAJOR.has(b)){const y=CB(c[a],c[b]);if(y<CBT)s+=300*(CBT-y)}}return s}
function local(c,id,ci){let s=w[id]*brand[id][ci];for(const m of nb[id]){const x=DE(ci,c[m]);if(x<18)s+=1000*(18-x);if(CBT&&MAJOR.has(id)&&MAJOR.has(m)){const y=CB(ci,c[m]);if(y<CBT)s+=300*(CBT-y)}}return s}
let rnd=1234567;const R=()=>{rnd=(rnd*1103515245+12345)%2147483648;return rnd/2147483648};
const chroma=h=>{const L=lab(h);return Math.hypot(L[1],L[2])};const tame=grid.map(h=>chroma(h)<=70);
const near={};for(const id of ids){near[id]=[...grid.keys()].filter(i=>tame[i]).sort((a,b)=>brand[id][a]-brand[id][b]);}
let best=null,bestC=Infinity;
for(let run=0;run<14;run++){
 const c={};for(const id of ids)c[id]=FIX[id]?grid.indexOf(FIX[id].toUpperCase()):near[id][Math.floor(R()*5)];
 const free=ids.filter(i=>!FIX[i]);
 let cur=cost(c),Tm=200;
 for(let it=0;it<400000;it++){const id=free[Math.floor(R()*free.length)];
  const ci=R()<0.7?near[id][Math.floor(R()*Math.min(near[id].length,400))]:near[id][Math.floor(R()*near[id].length)];
  const d0=local(c,id,c[id]),d1=local(c,id,ci),dd=d1-d0;
  if(dd<0||R()<Math.exp(-dd/Tm)){c[id]=ci;cur+=dd}
  Tm*=0.99997;}
 cur=cost(c); if(cur<bestC){bestC=cur;best=Object.assign({},c)} console.error('run',run,cur.toFixed(1));}
const col={};for(const id of ids)col[id]=grid[best[id]];
let mn=1e9,mp='',cbm=1e9,cbp='';
for(const [a,b] of pairs){const x=TL.deltaE(col[a],col[b]);if(x<mn){mn=x;mp=a+'/'+b}if(MAJOR.has(a)&&MAJOR.has(b)){const y=CB(best[a],best[b]);if(y<cbm){cbm=y;cbp=a+'/'+b}}}
const order=ids.slice().sort((a,b)=>(months[b]||0)-(months[a]||0));
for(const id of order)console.log(id.padEnd(18),col[id],'brand',T[id].join('/'),'dE',brand[id][best[id]].toFixed(1),'white',con(col[id],'#F4F6FA').toFixed(2),'bg',con(col[id],'#0B1424').toFixed(2),'months',months[id]);
for(const [a,b] of pairs){const x=TL.deltaE(col[a],col[b]);if(x<18)console.log('CLASH',a,b,x.toFixed(1));}
console.log('closest co-visible pair',mn.toFixed(1),mp,'| colour-blind closest (major pairs, protan/deutan)',cbm.toFixed(1),cbp,'| cost',bestC.toFixed(1));
require('fs').writeFileSync('palette_out.json',JSON.stringify({col,mn,mp,cbm,cbp,adj:Object.fromEntries(ids.map(i=>[i,[...adj[i]]]))},null,1));
