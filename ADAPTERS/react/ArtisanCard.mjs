import React, {useState} from 'react';
const h=React.createElement;
// 在宿主引入 web/components.css 与 web/themes.css。asset 取自 ASSET_INDEX。
export function ArtisanCard({asset,assetRoot='/artisan/',onSave}){
  const [saved,setSaved]=useState(false);
  const src=assetRoot.replace(/\/?$/,'/')+asset.preview_path;
  return h('article',{'data-artisan':asset.style_id},h('div',{className:'at-panel'},
    h('img',{src,alt:asset.asset_name,style:{maxWidth:'100%',height:150,objectFit:'contain'}}),
    h('h2',null,asset.asset_name),h('p',null,asset.width+' × '+asset.height+' · '+asset.license),
    h('button',{type:'button',className:'at-button','aria-pressed':saved,onClick:()=>{setSaved(!saved);onSave?.(asset.asset_id,!saved)}},saved?'已收藏':'收藏素材')));
}
