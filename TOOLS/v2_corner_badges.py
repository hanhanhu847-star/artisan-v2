"""替换视觉复核中主形重复、标记对比不足的V1实色三角角标。原件不删改。"""
from v2_plates import *
from v2_registry import *
def badge(P):
 z=P.S['id'];a=P.a;b=P.b;i=P.i;c=P.c;bg=P.bg;o=''
 if z=='bauhaus':
  o=P.r(8,8,96,25,a,'none')+P.r(8,33,25,104,i,'none')+P.p('M40 41H113A73 73 0 0 1 40 114Z',b,'none')+P.o(116,22,11,c,'none')
 elif z=='art-deco':
  o=P.p('M8 8H152V25H115V40H87V57H63V80H43V110H25V152H8Z',a,i,1.5)
  for k in range(8):o+=P.l(21,22,24+k*16,127-k*15,b,1)
  o+=P.p('M17 132V18H134',None,i,1)
 elif z=='swiss':
  o=P.r(9,9,130,12,i,'none')+P.r(9,21,12,130,a,'none')+P.r(30,31,30,68,i,'none')+P.r(69,31,60,22,a,'none')+P.r(69,63,39,12,i,'none')
 elif z=='neo-brutalism':
  o=P.p('M12 17H145L128 35L137 48L107 53L111 74L82 79L82 101L55 108L49 133L18 151Z',i,i,3)+P.p('M6 8H139L121 27L130 40L100 45L104 66L75 71L75 93L48 100L42 125L8 143Z',a,i,4)+P.p('M23 36H83V20L112 49L82 78V62H23Z',c,i,3)
 elif z=='memphis':
  o=P.p('M8 10H143Q124 24 128 37Q111 38 111 57Q91 56 90 75Q72 72 68 91Q48 90 47 111Q27 109 8 144Z',a,i,2)
  o+=P.p('M24 23Q28 47 41 32T65 33T90 25',None,b,6)+P.o(28,79,9,c,i,2)+P.p('M62 54L85 42L80 68Z',bg,i,2)
 elif z=='editorial':
  o=P.p('M10 9H143L10 143Z',c,i,1)+P.p('M10 9H110V36H83V63H57V89H30V116H10Z',bg,i,1.3)+P.t(26,55,'§',40,a,'Georgia')+P.l(24,69,61,69,i,.8)+P.p('M111 9L136 34H111Z',a,'none')
 elif z=='wabi-sabi':
  o=P.p('M8 11L45 9L68 13L96 8L139 12L124 32L107 42L100 66L79 72L61 98L44 103L26 133L9 143L12 104L7 76L11 41Z',c,'none')+P.p('M23 116Q36 66 103 29',None,i,2)+leaf(42,83,.82,-15,b,i)+leaf(65,61,.74,55,a,i)
 elif z=='dark-academia':
  o=P.p('M8 8H144V23H68L23 68V144H8Z',a,i,2)+P.p('M23 23H108L23 108Z',bg,a,1)+P.p('M34 69Q38 29 69 34Q67 60 34 69ZM40 62L61 41',None,a,2)+P.o(15,15,3,bg,i)+P.o(126,16,3,bg,i)+P.o(16,126,3,bg,i)
 elif z=='celestial-atlas':
  o=P.p('M12 12H148A136 136 0 0 1 12 148Z',bg,a,2)+P.p('M12 31H128A116 116 0 0 1 31 128V12',None,b,1)
  for k in range(12):
   ang=k*pi/22;o+=P.l(12+120*cos(ang),12+120*sin(ang),12+130*cos(ang),12+130*sin(ang),a,1)
  o+=star(51,49,25,5,6,a)+P.o(51,49,4,bg,'none')
 elif z=='dunhuang':
  o=P.p('M8 8H146L130 28H112L112 47H93L93 68H71L71 91H49L49 113H28L8 146Z',a,i,1.5)+P.p('M19 19H115L19 115Z',c,'none')
  o+=P.p('M50 77Q24 74 27 46Q44 47 51 62Q37 40 52 25Q65 42 53 62Q62 44 81 46Q79 74 50 77Z',b,i,1.8)+P.p('M23 93Q40 87 43 81M89 35Q92 23 108 24',None,i,1.5)
 elif z=='cartography':
  o=P.p('M9 9H147V29H115L29 115V147H9Z',c,i,1.2)+P.p('M22 22H119L22 119Z',bg,i,1)+star(54,54,31,8,4,i)+g(star(54,54,21,6,4,a),'rotate(45 54 54)')+P.l(15,37,15,115,i,1)
 elif z=='natural-history':
  o=P.p('M8 9H148L123 32L121 49L100 51L96 73L74 78L64 99L42 112L29 139H8Z',c,'none')+P.p('M20 122Q42 67 110 21',None,i,2.4)
  for x,y,ang in [(33,99,-24),(47,77,47),(67,57,-23),(88,39,47)]:o+=leaf(x,y,.72,ang,a,i)
 elif z=='retrofuturism':
  o=P.p('M10 10H140Q150 10 144 23L24 144Q10 155 10 140Z',a,i,2)+P.p('M24 23H112Q128 23 112 40L40 112Q24 128 24 112Z',bg,b,2)+g(P.e(60,56,29,10,None,b,3),'rotate(-35 60 56)')+P.o(60,56,13,c,i,1)+P.r(32,16,33,3,c,'none')
 elif z=='cyberpunk':
  o=P.p('M9 22L22 9H151L132 28H112L99 43H84L43 85V101L28 116V133L9 152Z',a,i,2)+P.p('M24 32H83L71 44H48V63H33V89M32 22H106L93 34',None,bg,3)+P.r(30,110,14,5,b,'none')
 elif z=='blueprint':
  o=P.p('M9 9H150V30H31V150H9ZM18 39H143L39 143V39Z',None,i,2)+P.p('M43 46H121L46 121V46M4 36V143M1 36H7M1 143H7',None,b,1)+P.p('M59 54V89H94M54 80H65M80 84V95',None,a,2)+P.o(16,16,3,None,a,1)
 else:
  def triangle(x,y,r,depth):
   if depth==0:return P.p(f'M{x} {y}h{r}l{-r} {r}Z',None,a,1.5)
   return triangle(x,y,r/2,depth-1)+triangle(x+r/2,y,r/2,depth-1)+triangle(x,y+r/2,r/2,depth-1)
  o=triangle(9,9,137,3)
 return svg(160,160,o)
def make():
 for S in STYLES:
  r=item(S['id'],'ornaments','corner-badge','页角标识 · V2','独立透明页角饰件；各套重绘主轮廓，替代V1低对比三角角标。',0,'corner',family='ribbon',credit='upgrade')
  write(outfile(S['id'],r),badge(Pen(S)));save_batch(S['id'],'corner-revision',[r])
 report()
if __name__=='__main__':make()
