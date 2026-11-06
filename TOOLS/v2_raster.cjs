const fs=require('node:fs'),path=require('node:path'),sharp=require('sharp');const root=path.resolve(__dirname,'..');
(async()=>{for(const f of fs.readdirSync(path.join(root,'AUDIT/raster-queue'))){
const z=f.slice(0,-5),rows=JSON.parse(fs.readFileSync(path.join(root,'AUDIT/raster-queue',f)));
const base=path.join(root,'STYLES',z);for(let k=0;k<rows.length;k+=2){const src=path.join(base,rows[k].file),dst=path.join(base,rows[k+1].file);
const meta=await sharp(src).metadata();if(fs.existsSync(dst)&&fs.statSync(dst).mtimeMs>=fs.statSync(src).mtimeMs){const current=await sharp(dst).metadata();if(current.width===meta.width&&current.height===meta.height)continue}
const r=await sharp(src).flatten({background:'#fff'}).jpeg({quality:92,mozjpeg:true}).toFile(dst);if(r.width!==meta.width||r.height!==meta.height)throw Error(src)}
fs.writeFileSync(path.join(base,'v2-records/backgrounds.json'),JSON.stringify(rows,null,2));console.log(z,'9 compositions + 9 native size JPGs')}})().catch(e=>{console.error(e);process.exit(1)})
