/* 实际解码与渲染缓存，用于离线浏览、pHash和全量联系表。不会把缩略图计入素材。 */
const fs=require('node:fs'),path=require('node:path'),sharp=require('sharp'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),P=path.join(root,'PREVIEWS','v2'),audit=path.join(root,'AUDIT');
const read=f=>JSON.parse(fs.readFileSync(f,'utf8'));const gethash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
async function check(style){const base=path.join(root,'STYLES',style);const dir=path.join(base,'v2-records');
const add=fs.existsSync(dir)?fs.readdirSync(dir).filter(x=>x.endsWith('.json')).flatMap(x=>read(path.join(dir,x))):[];
const legacy=read(path.join(base,'asset-meta.json')).filter(x=>!x.file.split('/')[1].startsWith('v2-'));const rows=legacy.concat(add),out=[];
const oldFile=path.join(audit,'render-'+style+'.json'),cache=new Map((fs.existsSync(oldFile)?read(oldFile):[]).map(x=>[x.file,x]));
for(let i=0;i<rows.length;i+=4){await Promise.all(rows.slice(i,i+4).map(async r=>{
 const file=path.join(base,r.file),rel='PREVIEWS/v2/'+style+'/'+r.file+'.webp',dest=path.join(root,rel),sum=gethash(file),o=cache.get(r.file);
 if(o&&o.sha256===sum&&fs.existsSync(dest)){out.push(o);return}
 fs.mkdirSync(path.dirname(dest),{recursive:true});const img=sharp(file,{limitInputPixels:false});const m=await img.metadata();
 const buffer=await img.resize({width:240,height:170,fit:'inside',withoutEnlargement:false}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
 const d=buffer.data;let mn=255,mx=0;for(let j=3;j<d.length;j+=4){mn=Math.min(mn,d[j]);mx=Math.max(mx,d[j])}
 if(mx===0 || (r.transparency&&mn===255))throw Error(style+'/'+r.file+' alpha mismatch '+mn+','+mx);
 await sharp(d,{raw:{width:buffer.info.width,height:buffer.info.height,channels:4}}).webp({quality:90,alphaQuality:100}).toFile(dest);
 out.push({file:r.file,sha256:sum,width:m.width,height:m.height,format:m.format,alphaMin:mn,alphaMax:mx,preview:rel})
}))}
out.sort((a,b)=>a.file.localeCompare(b.file));fs.writeFileSync(oldFile,JSON.stringify(out,null,1));
console.log(style,out.length)}
(async()=>{const styles=process.argv.slice(2);for(const s of styles.length?styles:fs.readdirSync(path.join(root,'STYLES')))await check(s)})().catch(e=>{console.error(e);process.exit(1)});
