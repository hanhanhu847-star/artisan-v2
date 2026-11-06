/* 独立于 XML 解析，使用 librsvg 实际渲染每个 SVG。对平铺项做邻接检查。 */
const fs=require('node:fs'),path=require('node:path'),sharp=require('sharp'),root=path.resolve(__dirname,'..');
const rows=JSON.parse(fs.readFileSync(path.join(root,'ASSET_INDEX.json'),'utf8')).assets.filter(r=>r.file_format==='svg');
async function main(){
const previews=path.join(root,'PREVIEWS','details');fs.mkdirSync(previews,{recursive:true});let tile=0,alpha=0;const failures=[];
for(let i=0;i<rows.length;i+=8){await Promise.all(rows.slice(i,i+8).map(async a=>{
 try{const f=path.join(root,a.file_path),side=230;
 const {data,info}=await sharp(f).resize({width:side,height:side,fit:'inside'}).ensureAlpha().raw().toBuffer({resolveWithObject:true});let min=255,max=0;for(let k=3;k<data.length;k+=4){min=Math.min(min,data[k]);max=Math.max(max,data[k])}
 if(!max)throw Error('Rendered invisible');if(a.transparency&&min===255)throw Error('Declared transparency missing');if(a.transparency)alpha++;
 if(a.tiling){let maxDiff=0;for(let x=0;x<info.width;x++)for(let k=0;k<4;k++)maxDiff=Math.max(maxDiff,Math.abs(data[x*4+k]-data[((info.height-1)*info.width+x)*4+k]));for(let y=0;y<info.height;y++)for(let k=0;k<4;k++)maxDiff=Math.max(maxDiff,Math.abs(data[y*info.width*4+k]-data[(y*info.width+info.width-1)*4+k]));if(maxDiff>4 && a.asset_id!=='shared.patterns.alpha-grid.svg')throw Error('Boundary mismatch '+maxDiff);
 // 棋盘边界本应翻色；用数学周期的两周期参考验证灰格跨边界仍然交替。
 if(a.asset_id==='shared.patterns.alpha-grid.svg'){const d=await sharp(f).ensureAlpha().raw().toBuffer();for(let y=0;y<64;y++)for(let x=0;x<64;x++){const expected=((x>>4)+(y>>4))%2?244:211;if(d[((y%32)*32+x%32)*4]!==expected)throw Error('Checker periodicity')}}tile++}
 if(a.style_id!=='shared' && (a.file_path.endsWith('/icons/search.svg')||a.file_path.endsWith('/illustrations/study-02.svg')||a.file_path.endsWith('/ornaments/rule.svg')||a.file_path.endsWith('/ui/button-selected.svg'))){
 await sharp(f).resize({width:450,height:190,fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toFile(path.join(previews,a.style_id+'-'+a.category+'.png'))}
 }catch(e){failures.push({id:a.asset_id,error:String(e)})}
}))}
const report={rendered:rows.length-failures.length,alphaChecked:alpha,svgTiles:tile,failures};
fs.writeFileSync(path.join(root,'PREVIEWS','svg-check.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(failures.length)process.exitCode=1
}main().catch(e=>{console.error(e);process.exit(1)})
