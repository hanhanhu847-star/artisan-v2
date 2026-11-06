/* Node 18+, sharp 0.33+。以目标像素直接光栅化 SVG，禁止小图放大。 */
const fs=require('node:fs'), path=require('node:path'), sharp=require('sharp');
const root=path.resolve(__dirname,'..'), styles=JSON.parse(fs.readFileSync(path.join(__dirname,'style-definitions.json'),'utf8'));
async function main(){
  for(const s of styles){
    const dir=path.join(root,'STYLES',s.id);
    const jobs=JSON.parse(fs.readFileSync(path.join(dir,'raster-jobs.json'),'utf8'));
    for(const j of jobs){
      // Avoid string-replacement group/digit ambiguity; use function values.
      const raw=fs.readFileSync(path.join(root,j.src),'utf8').replace(/(<svg[^>]*?\bwidth=")[^"]*(" height=")[^"]*"/,(_m,p,q)=>p+j.w+q+j.h+'"');
      const dest=path.join(root,j.dst);const image=sharp(Buffer.from(raw));
      if(dest.endsWith('.png'))await image.png().toFile(dest);else await image.jpeg({quality:93,mozjpeg:true}).toFile(dest);
    }
    const pdir=path.join(root,'PREVIEWS','plates');fs.mkdirSync(pdir,{recursive:true});
    await sharp(path.join(dir,'backgrounds','field-study-1920.jpg')).resize(640,360).webp({quality:84}).toFile(path.join(pdir,s.id+'.webp'));
    const photo=fs.readdirSync(path.join(dir,'backgrounds')).find(x=>x.startsWith('photo-')&&x!=='photo-window.jpg');
    if(photo)await sharp(path.join(dir,'backgrounds',photo),{limitInputPixels:false}).resize({width:900}).webp({quality:83}).toFile(path.join(pdir,s.id+'-photo.webp'));
    console.log('rendered',s.id);
  }
}
main().catch(e=>{console.error(e);process.exit(1)});
