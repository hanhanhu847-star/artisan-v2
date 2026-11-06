/* 实际SVG中心区域应保持透明，让边框能叠放在已有图片上。 */
const fs=require('fs'),path=require('path'),sharp=require('sharp'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),out=path.join(root,'PREVIEWS/frame-review');fs.mkdirSync(out,{recursive:true});
(async()=>{const result=[];
for(const z of fs.readdirSync(path.join(root,'STYLES'))){
 for(let n=1;n<=3;n++){
  const rel='STYLES/'+z+'/ornaments/v2-frame-'+n+'.svg',p=path.join(root,rel);
  const raw=await sharp(p).ensureAlpha().extract({left:400,top:250,width:100,height:100}).raw().toBuffer();
  let maxAlpha=0;for(let j=3;j<raw.length;j+=4)maxAlpha=Math.max(maxAlpha,raw[j]);
  if(maxAlpha!==0)throw Error(rel+' content aperture covered '+maxAlpha);
  await sharp(p).resize(400,267,{fit:'inside'}).png().toFile(path.join(out,z+'-'+n+'.png'));
  result.push({file:rel,sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),apertureMaxAlpha:maxAlpha});
 }}
fs.writeFileSync(path.join(root,'AUDIT/frame-apertures.json'),JSON.stringify(result,null,2));console.log(result.length+' transparent frame apertures checked');
})().catch(e=>{console.error(e);process.exit(1)});
