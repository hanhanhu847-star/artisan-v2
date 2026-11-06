/* 全部标注可平铺SVG原生渲染，核对RGBA接缝并导出2×2实物证明。 */
const fs=require('fs'),path=require('path'),sharp=require('sharp');
const root=path.resolve(__dirname,'..'),idx=JSON.parse(fs.readFileSync(path.join(root,'ASSET_INDEX.json'),'utf8'));
const out=[],dest=path.join(root,'PREVIEWS','svg-tile-proofs');fs.mkdirSync(dest,{recursive:true});
function edges(d,w,h,axis){
 const samples=[],at=(x,y,c)=>d[(y*w+x)*4+c];
 let seam=0;
 const max=axis==='x'?w:h,inner=axis==='x'?h:w;
 for(let k=1;k<max;k++){let sum=0;for(let j=0;j<inner;j++)for(let c=0;c<4;c++)sum+=Math.abs(axis==='x'?at(k,j,c)-at(k-1,j,c):at(j,k,c)-at(j,k-1,c));samples.push(sum/(inner*4))}
 for(let j=0;j<inner;j++)for(let c=0;c<4;c++)seam+=Math.abs(axis==='x'?at(0,j,c)-at(w-1,j,c):at(j,0,c)-at(j,h-1,c));
 seam/=inner*4;samples.sort((a,b)=>a-b);const threshold=Math.max(2.5,samples[Math.floor(samples.length*.995)]*1.6+1);
 return {seam,threshold,ok:seam<=threshold};
}
(async()=>{
 for(const a of idx.assets.filter(a=>a.tiling&&a.file_format==='svg')){
  const im=await sharp(path.join(root,a.file_path)).ensureAlpha().raw().toBuffer({resolveWithObject:true}),w=im.info.width,h=im.info.height;
  // 比较预乘颜色，避免透明像素中的无意义RGB干扰。
  const d=Buffer.from(im.data);for(let k=0;k<d.length;k+=4)for(let c=0;c<3;c++)d[k+c]=Math.round(d[k+c]*d[k+3]/255);
  const X=edges(d,w,h,'x'),Y=edges(d,w,h,'y');out.push({asset_id:a.asset_id,file:a.file_path,width:w,height:h,x:X,y:Y,ok:X.ok&&Y.ok});
  const input=await sharp(im.data,{raw:{width:w,height:h,channels:4}}).resize(192,192,{fit:'fill'}).png().toBuffer();
  await sharp({create:{width:384,height:384,channels:4,background:'#b8bec0'}}).composite([{input,left:0,top:0},{input,left:192,top:0},{input,left:0,top:192},{input,left:192,top:192}]).webp({quality:92}).toFile(path.join(dest,a.asset_id+'.webp'));
 }
 fs.writeFileSync(path.join(root,'AUDIT','svg-tiling.json'),JSON.stringify(out,null,2));
 const fail=out.filter(x=>!x.ok);console.log(out.length,'SVG tile files;',fail.length,'seam candidates');console.log(JSON.stringify(fail));
})().catch(e=>{console.error(e);process.exit(1)});
