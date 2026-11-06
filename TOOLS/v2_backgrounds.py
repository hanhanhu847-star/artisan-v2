"""九个新背景/风格，按意图与长宽比单独构图。画板本身具有交付分辨率。"""
from v2_scenes import *
from v2_bg_more import more
DIMS=[(3840,2160)]*3+[(2160,3840)]*2+[(3000,3000)]*2+[(5120,1440)]*2
TITLES={
'bauhaus':'齿轨桥与支点|北向采光工场|三色印版套位|悬线舞台装置|楼梯塔剖影|四分圆构成|三角铺装实验|连续拱廊|舞台平衡横轴',
'art-deco':'宝石门廊|黄铜扇窗|都会投影|退台商厦|长廊吊灯|旭日马赛克|八角大厅地坪|群楼节拍|铸铜长栏板',
'swiss':'字级基线海报|通勤时间带|字母阶梯|单栏目录|斜向导视塔|比例分格|编码索引|站台信息带|尺度标本',
'neo-brutalism':'折箭路标墙|拼钉仓板|撕纸横幅|叠放便笺柱|硬影阶梯|封条交叉|粗网点标记|看台护板|油印滚带',
'memphis':'滚珠迷宫|弯管浮岛|彩屑墙|摇摆花架|波浪阶梯|弧砖游乐场|彩豆围盘|共舞饰带|断线跑道',
'editorial':'图像与旁注|目录双层导航|多栏通讯|纵向章首|摄影侧栏|封面字级标本|书页结构|跨卷目录|校样刻度纸带',
'wabi-sabi':'风过浅滩|砂纹庭院|泥坯排列|一枝过纸窗|石壁水痕|落叶浮水|茶席俯视|岸边远山|竹篱与雾带',
'dark-academia':'书脊档墙|拱窗夜色|索引抽屉|烛影阅览栏|攀架书梯|徽章压纹|装帧工位平面|书库通廊|窗沿藏品',
'celestial-atlas':'黄道十二分区|极轴方位盘|流星辐射点|观测筒剖影|经线象限仪|天球投影网|月海雕线|长曝光星迹|银河尘埃带',
'dunhuang':'莲池水纹|层叠洞龛|火焰云带|飞舞飘带|供养花架|团莲方井|八瓣套菱藻井|楼阁栏楯长卷|缠枝连珠边饰',
'cartography':'三角测网|群岛浅滩|航程剖面|河流纵域|山隘指北图|城市方格|罗盘海流|海岸纵剖|岛间航路',
'natural-history':'羽叶冠层|沉积地层|河床藻群|茎节纵图|地质钻芯|花粉形态|贝壳年轮|物候观察带|浅海化石层',
'retrofuturism':'太空通讯天际|月港着陆道|电台频带|发射塔架|调谐柱|舷窗观测|原子晶格|高架通道|行星信标',
'cyberpunk':'电路外墙|空中连廊|数据包栅格|通风井道|霓虹导柱|通讯界面|多层电路阵列|光纤流网络|雨幕商业街',
'blueprint':'梁柱示意|给排水支线|装配基准台|水准立面|阀门剖切|齿圈安装|桁格构件|桥梁纵剖|传动工位带',
'generative-art':'粒子干涉|加权胞形|分形树冠|规则30生长带|递归枝晶|迭代置换|回转采样织纹|双涡流迁移|动态采样脉冲'}
def board(P,j,W,H):
    z=P.S['id'];i,a,b,c,bg=P.i,P.a,P.b,P.c,P.bg;rnd=random.Random(P.S['no']*719+j*107)
    x=W/2;y=H/2;u=min(W,H);o=rect(0,0,W,H,bg)
    def m(k,X,Y,s):return place(motif(P.S,k),X-s/2,Y-s/2,s/300)
    def ob(k,X,Y,s):return place(obj(P,k),X-s/2,Y-s/2,s/240)
    def gd(nx,ny):return '<g opacity=".25">'+P.grid(18,18,W-36,H-36,nx,ny,b)+'</g>'
    def punit(q,X,Y,K=1,R=0):return place(q,X,Y,K,R)
    def ring(X,Y,R,nc,f):
        return ''.join(g(f(k),f'translate({X} {Y}) rotate({k*360/nc})')for k in range(nc))
    def rail():return P.l(14,H*.8,W-14,H*.8,i,3)
    def note():return P.l(W*.05,H*.89,W*.24,H*.89,a,1)
    q=(P.S['no']-1)%4
    if z=='bauhaus':
        if j==0:o+=rail()+''.join(P.o(80+147*k,220,45,[a,b,c][k%3],'none')+P.r(73+147*k,251,15,224,i,'none')+P.p(f'M{29+147*k} 472l65 -96l73 96Z',b,'none')for k in range(7))
        if j==1:o+=P.p('M0 324L166 151V271L362 115V239L559 81V210L785 48V183L1070 20V474H0Z',b,'none')+''.join(pane(P,30+k*144,326,106,82,3,2)for k in range(7))
        if j==2:o+=P.r(89,109,440,302,c,'none')+P.o(535,266,151,a,'none')+P.p('M541 492L697 91L899 492Z',b,'none')+P.cols(126,152,13,22,203,i,0,3)
        if j==3:o+=P.p('M169 19V98M36 126L303 92M79 120V273M262 96V374',None,i,2.5)+P.o(79,311,41,a,'none')+P.p('M202 469L261 370L319 469Z',b,'none')+P.r(40,506,181,12,c,'none')
        if j==4:o+=P.r(71,62,161,442,b,'none')+''.join(pane(P,86,87+k*62,126,36,2,1)for k in range(6))+P.p('M16 547L306 376V547Z',a,'none')
        if j==5:o+=P.p('M43 296A251 251 0 0 1 294 45V296Z',a,'none')+P.p('M306 306H555A249 249 0 0 1 306 555Z',b,'none')+P.r(44,308,250,246,c,'none')+P.o(425,170,92,i,'none')
        if j==6:o+=''.join(poly([(25+k*138,25+l*138),(158+k*138,25+l*138),(25+k*138,158+l*138)],[a,b,c,i][(k+2*l)%4])if (k+l)%2 else P.o(91+k*138,91+l*138,57,[b,c,i][k%3],'none')for k in range(4)for l in range(4))
        if j==7:o+=''.join(arch(P,22+k*180,139,155,276,[a,b,c][k%3])+arch(P,51+k*180,191,97,224,bg)for k in range(12))+P.r(0,412,W,17,i,'none')
        if j==8:o+=P.l(0,337,W,249,i,8)+''.join(P.l(102+k*259,333-k*10,102+k*259,175+k%3*20,i,2)+P.o(102+k*259,142+k%3*20,34,[a,b,c][k%3],'none')for k in range(8))
    elif z=='art-deco':
        if j==0:o+=P.p(f'M53 510V173L179 72H{W-178}L{W-53} 173V510Z',b,a,3)+''.join(P.p(f'M{124+k*258} 465V198L{187+k*258} 145H{279+k*258}L{343+k*258} 198V465Z',bg,a,2)+P.cols(169+k*258,224,5,28,208,a)for k in range(3))
        if j==1:o+=ring(x,H*.75,200,33,lambda k:poly([(0,0),(-12,-(185+(k%3)*52)),(12,-(185+(k%3)*52))],[a,b,c][k%3]))+P.r(0,H*.72,W,H*.3,bg,'none')+P.bars(W*.12,H*.74,3,12,W*.76,a)
        if j==2:o+=P.o(W*.63,177,88,c)+staircity(P,0,415,W,339,rnd)+''.join(poly([(k*86,415),(k*86+43,415),(k*86-82,570),(k*86-103,570)],b)for k in range(15))
        if j==3:o+=''.join(P.r(29+k*21,414-k*73,W-58-k*42,152+k*73,[b,bg][k%2],a,2)for k in range(6))+P.cols(x-23,85,4,15,442,a)+P.l(x,20,x,64,c,3)
        if j==4:o+=''.join(P.l(47+k*103,18,47+k*103,95+k*102,a,1.8)+place(obj(P,2),4+k*103,75+k*104,.40)for k in range(3))+P.p('M23 523H84V501H131V480H161V457H181V480H211V502H256V525H316',None,a,3)
        if j==5:o+=ring(x,y,200,32,lambda k:poly([(0,-49),(-15,-221),(14,-246),(22,-164)],[a,b,c,bg][k%4],i,1))+P.o(x,y,56,bg,a,3)+P.o(x,y,29,b)
        if j==6:o+= ''.join(poly([polar(x,y,r,k*pi/4+pi/8)for k in range(8)],f,a,1.4)for r,f in [(278,b),(251,bg),(206,c),(198,bg),(144,b),(108,bg),(68,a)])+ringticks(x,y,77,32,b)
        if j==7:o+=staircity(P,0,467,W,383,rnd)+P.bars(0,476,4,11,W,a)
        if j==8:o+=P.bars(0,135,2,12,W,a,0,2)+P.bars(0,430,2,13,W,a,0,2)+''.join(place(cell(P.S),28+k*188,194,2.14) +P.r(16+k*188,153,174,266,'none',b,1)for k in range(12))
    elif z in ['swiss','editorial']:
        ed=z=='editorial';font='Georgia' if ed else 'Arial'
        if j==0:o+=P.r(.06*W,70,.42*W,402,b if ed else bg,'none')+(P.e(.27*W,257,154,156,bg,'none')if ed else P.t(.06*W,395,'24',315,i,font))+P.t(.54*W,239,'Fig.' if ed else '07',119,a,font)+P.bars(.55*W,299,9,13,.34*W,i,0,1.4)
        if j==1:
            if ed:o+=P.t(52,151,'I   /   II',113,i)+P.l(47,207,W-47,207,a,2)+''.join(P.t(57+k*252,311,f'{k+1:02}',35,a)+P.bars(57+k*252,344,8,12,175,i)for k in range(4))
            else:o+=gd(12,6)+''.join(P.r(106,57+k*75,260+((k*131)%570),33,[a,i,b][k%3],'none')+P.t(39,83+k*75,f'{k+1:02}',17,i,'monospace')for k in range(7))
        if j==2:
            if ed:o+=P.r(49,46,420,510,None,i,2)+P.t(80,172,'I.',92,a)+P.bars(79,214,16,16,305,i)+P.r(528,49,478,173,b,'none')+P.bars(549,264,14,17,408,i)
            else:o+=P.t(40,452,'A',460,i,font)+P.t(438,394,'a',323,b,font)+P.t(748,340,'a',173,a,font)+P.l(31,457,W-31,457,i,2)
        if j==3:o+=(P.t(30,216,'III',157,i)+P.t(41,313,'Chapter',39,a)+P.bars(43,374,9,12,201,i) if ed else P.r(34,35,10,523,i,'none')+''.join(P.t(61,102+k*79,f'{k+1:02}',47,i if k else a,font)+P.bars(177,72+k*79,3,8,116,b) for k in range(6)))
        if j==4:o+=(P.r(26,35,W-52,535,None,i)+P.r(44,62,51,435,a,'none')+P.e(210,215,76,111,b,'none')+P.bars(126,369,8,14,144,i)if ed else place(P.r(0,0,520,46,a,'none')+P.r(48,61,222,14,i,'none')+P.t(319,108,'N',48,i,font),-20,418,1,-55)+P.t(32,540,'12 →',45,i,font))
        if j==5:o+=(P.t(40,374,'R',351,i)+P.t(313,455,'r',220,a)+P.bars(28,97,4,126,545,b,0,.7)+P.o(427,163,56,None,a) if ed else P.r(40,38,310,311,a,'none')+P.r(365,38,183,183,i,'none')+P.r(365,236,105,110,b,'none')+P.r(484,238,64,61,c,'none')+P.cols(44,391,15,33,132,i,0,2))
        if j==6:o+=(book(P,49,91,505,383,bg)+P.r(79,144,154,171,b,'none')+P.t(332,263,'IV',67,a)+P.bars(326,340,7,13,182,i) if ed else ''.join(P.r(42+k*57,51+l*57,48,48,[a,i,b][(k//2+l)%3],'none')for k in range(9)for l in range(8)if (k*k+5*l+k*l)%7<3)+P.l(41,532,557,532,i,3))
        if j==7:
            if ed:
                for k in range(5):
                    X=45+k*414;o+=P.r(X,82,366,433,None,b,1)+P.t(X+25,205,['I','II','III','IV','V'][k],87,a,font)+P.r(X+188,121,143,173,c,'none')+P.bars(X+25,341,7,15,301,i)+P.t(X+296,488,str(k*16+1),15,i,font)
            else:o+=''.join(P.t(46+k*283,278,f'{k+1:02}',120,i if k%3 else a,font)+P.l(45+k*283,316,282+k*283,316,i,4)+P.bars(45+k*283,349,4,13,187,b)for k in range(7))
        if j==8:o+=(P.bars(32,169,5,57,W-64,b)+''.join(P.t(37+k*342,374,s,151,i if k%2 else a,font)for k,s in enumerate(['Aa','Bb','Cc','Dd','Ee','Ff'])) if ed else P.l(28,303,W-28,303,i,4)+''.join(P.l(42+k*26,303,42+k*26,190 if k%5==0 else 249,a if k%5==0 else i,2.2)+(P.t(38+k*26,351,str(k),19,i,font)if k%5==0 else '')for k in range(79)))
    elif z in ['neo-brutalism','memphis']:
        ne=z=='neo-brutalism'
        if j==0:
            if ne:o+=place(P.r(0,0,420,195,c,i,6)+P.p('M23 68H242V27L353 95L242 165V120H23Z',i),48,211,1,-9)+place(P.r(0,0,381,187,b,i,6)+P.p('M21 102L157 28L159 66H335V125H159V154Z',a,i,4),W*.52,155,1,7)
            else:o+=P.p('M43 455H327Q436 451 436 321Q439 175 577 172H958',None,i,24)+P.p('M43 449H325Q430 445 430 315Q434 169 575 166H958',None,a,14)+''.join(P.o(168+k*267,166+k%2*145,29+k*6,[b,c,a][k])for k in range(3))
        if j==1:o+=''.join(place((P.r(0,0,199,193,[a,b,c][k%3],i,5)+P.o(18,18,6,i)+P.p('M36 151L98 42L171 152Z',None,i,7))if ne else (P.p('M0 57Q21 -61 63 3T112 59T163 -10',None,[a,b,i][k%3],14)+P.o(148,96,18,c)),36+k*204,153+(k%2)*115,1,(-1)**k*5)for k in range(5))
        if j==2:
            if ne:
                for k in range(5):o+=poly([(0,48+k*97)]+[(p*W/37,74+k*97+rnd.randrange(-16,20))for p in range(38)]+[(W,159+k*97),(0,159+k*97)],[a,b,c,i,bg][k],i,3)
            else:
                for k in range(93):
                    X=rnd.uniform(17,W-25);Y=rnd.uniform(31,H-30);f=[i,a,b,c][k%4];o+=P.o(X,Y,rnd.randrange(3,16),f,'none')if k%3==0 else place(P.p('M0 9L16 0L31 17L14 25Z',f,'none')if k%3==1 else P.p('M0 8l12 -7l12 11l12 -7',None,f,4),X,Y)
        if j==3:o+=''.join(place(P.r(7,8,226,106,i)+P.r(0,0,226,106,[a,c,b,bg][k],i,4)+P.bars(19,32,3,15,147,i,0,3),39+(k%2)*13,41+k*127,1,(-1)**k*4)for k in range(4)) if ne else ''.join(P.e(x+(-1)**k*13,510-k*89,W*(.35-k*.035),19,[a,b,c,i,b][k])+P.p(f'M{x-21} {490-k*89}l27 -46l29 48Z',[c,a][k%2])for k in range(5))
        if j==4:o+=P.p('M16 525H68V422H123V313H182V210H240V103H320V549H16Z',b,i,6)+P.p('M24 316L113 161L125 227L169 200L78 360L66 288Z',a,i,4)if ne else P.p('M33 536V431H96V337H154V238H212V143H279V52',None,b,18)+P.o(188,126,35,a)+P.p('M37 145l25 -35l24 31l25 -35',None,i,5)
        if j==5:o+=place(P.r(0,0,411,105,c,i,5)+P.cols(20,22,18,19,60,i,5,2),28,226,1,-21)+place(P.r(0,0,397,117,b,i,5)+P.p('M22 41H223V16L311 60L222 103V79H22Z',i),125,239,1,17)if ne else ''.join(place(arch(P,0,0,127,142,[a,b,c][(k+l)%3])+arch(P,28,34,75,107,bg),26+k*141,35+l*177)for l in range(3)for k in range(4))
        if j==6:o+=''.join(P.o(40+k*47,41+l*47,4+((k+2*l)%8)*2,[i,a,b][(k//3+l//4)%3],'none')for k in range(12)for l in range(12))+place(P.r(0,0,212,76,c,i,4)+P.t(17,54,'02',48,i,'Arial'),178,293,1,-9)if ne else P.o(x,y,202,b,'none')+ring(x,y,146,17,lambda k:P.e(142,0,29,13,[a,c,bg,i][k%4],'none'))+P.p('M209 324Q247 211 287 279T363 278T393 262',None,i,12)
        if j==7:o+=''.join(place((P.r(0,0,253,181,[a,b,c][k%3],i,5)+P.p('M24 132L101 32L202 141Z',None,i,12)+P.o(230,20,5,i))if ne else(P.p('M0 81Q24 -22 66 34T145 69T209 18',None,[a,b,i][k%3],12)+P.o(195,104,21,c)),19+k*269,179+40*sin(k))for k in range(8))
        if j==8:o+=P.r(16,164,W-32,269,c,i,5)+''.join(P.e(99+k*178,297,59,82,[a,b,bg][k%3],i,5)+P.e(99+k*178,297,16,25,i)for k in range(12))if ne else rope(P,[(22+k*43,320+sin(k*.7)*91+(k%2)*39)for k in range(49)],b,14)+''.join(P.o(62+k*193,153+k%2*27,19,[c,a,i][k%3],'none')for k in range(11))
    else:return more(P,j,W,H,o,rnd)
    return o

def make():
    for S in STYLES:
        z=S['id'];rows=[]
        for j,((w,h),title) in enumerate(zip(DIMS,TITLES[z].split('|'))):
            W=600*w/h;H=600
            body=board(Pen(S),j,W,H)
            assert len(body)>180,(z,j)
            role=['landscape']*3+['portrait']*2+['square']*2+['ultrawide']*2
            r=item(z,'backgrounds',f'plate-{j+1:02}',title,'按此画幅单独创作的可编辑背景；不是旧图裁切。', [0,1,2,0,1,2,0,1,2][j],role[j],alpha=False)
            write(outfile(z,r),svg(w,h,body,f'{n(W)} 600'));rows.append(r)
            jpg=dict(r,file=r['file'][:-3]+'jpg',credit='variant',asset_name=title+' · 栅格版',intended_usage='从同名SVG按目标像素直接光栅化；不另计独立作品。')
            rows.append(jpg)
        # 延后登记，直到所有 JPG 的实际写入均完成。
        dump(ROOT/'AUDIT'/'raster-queue'/(z+'.json'),rows)
if __name__=='__main__':make()
