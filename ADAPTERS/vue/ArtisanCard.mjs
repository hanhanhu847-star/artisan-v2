import {defineComponent,h,ref} from 'vue';
// Vue 3；素材根目录指向静态公开目录。样式表在应用入口导入。
export default defineComponent({name:'ArtisanCard',props:{asset:{type:Object,required:true},assetRoot:{type:String,default:'/artisan/'}},emits:['save'],setup(props,{emit}){
const saved=ref(false);return ()=>h('article',{'data-artisan':props.asset.style_id},[h('div',{class:'at-panel'},[
h('img',{src:props.assetRoot.replace(/\/?$/,'/')+props.asset.preview_path,alt:props.asset.asset_name,style:{maxWidth:'100%',height:'150px',objectFit:'contain'}}),
h('h2',props.asset.asset_name),h('p',props.asset.width+' × '+props.asset.height+' · '+props.asset.license),
h('button',{type:'button',class:'at-button','aria-pressed':saved.value,onClick:()=>{saved.value=!saved.value;emit('save',props.asset.asset_id,saved.value)}},saved.value?'已收藏':'收藏素材')])])}});
