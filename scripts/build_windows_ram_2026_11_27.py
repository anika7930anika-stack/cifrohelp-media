from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math,random,os
D='instagram/2026-11-27_windows_ram_10_cards'
os.makedirs(D,exist_ok=True)
W,H=1080,1350
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
CY=(60,228,251); AM=(255,184,76); WH=(247,252,255); MUT=(177,205,224)
def font(n,b=0): return ImageFont.truetype(bold if b else reg,n)
def text(d,x,y,s,n=35,col=WH,b=0):
 for z in s.split('\n'):
  d.text((x,y),z,font=font(n,b),fill=col)
  y+=round(n*1.23)
def box(d,q,r,fill,outline=None):
 d.rounded_rectangle(q,radius=r,fill=fill,outline=outline,width=3)
def ok(d,y,s):
 d.ellipse((112,y,156,y+44),fill=(16,106,111),outline=CY,width=3)
 d.line((123,y+22,132,y+30,144,y+13),fill=WH,width=5)
 text(d,175,y+2,s,30)
def backdrop(i):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 for y in range(H):
  t=y/H;d.line((0,y,W,y),fill=(int(5+4*t),int(16+13*t),int(33+15*t)))
 random.seed(i)
 for j in range(150):
  x=random.randrange(W);y=random.randrange(H);r=random.choice([1,1,2])
  d.ellipse((x-r,y-r,x+r,y+r),fill=(14,64,88))
 box(d,(24,24,1056,1325),36,None,(40,102,138))
 return im
def jelly(im,cx,cy,sc):
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 for j in range(17):
  k=(j-8)/8
  pts=[(int(cx+k*141*sc+math.sin(v*.33+j*.57)*13*sc),int(cy+70*sc+v*13*sc)) for v in range(33)]
  color=(66,227,249,170) if j%4 else (255,170,69,195)
  d.line(pts,fill=color,width=max(2,int(3*sc)),joint='curve')
  for z in [7,17,27]:
   x,y=pts[z];d.rectangle((x-4,y-4,x+4,y+4),fill=color)
 d.pieslice((cx-178*sc,cy-135*sc,cx+178*sc,cy+90*sc),180,360,fill=(20,145,228,144),outline=(97,240,255,230),width=max(3,int(6*sc)))
 d.arc((cx-171*sc,cy-46*sc,cx+171*sc,cy+117*sc),6,176,fill=(255,187,82,215),width=max(2,int(5*sc)))
 glow=layer.filter(ImageFilter.GaussianBlur(24));glow.putalpha(glow.getchannel('A').point(lambda a:a//2))
 im.alpha_composite(glow);im.alpha_composite(layer)
CARD=[
 ('ОЗУ ПОЧТИ\nНА ПРЕДЕЛЕ?','Не спеши покупать новую память.','hero'),
 ('ОТКРОЙ\nДИСПЕТЧЕР\nЗАДАЧ','Первая проверка займёт минуту.','keys'),
 ('НАЙДИ,\nКТО ТРАТИТ ОЗУ','Посмотри программы с наибольшим расходом.','sort'),
 ('БРАУЗЕР\nСЪЕДАЕТ ОЗУ?','Много вкладок и расширений — частая причина.','browser'),
 ('ЗАКРОЙ\nТОЛЬКО ЛИШНЕЕ','Не теряй данные ради скорости.','close'),
 ('ПРОВЕРЬ\nАВТОЗАГРУЗКУ','Некоторые приложения стартуют сами.','startup'),
 ('85% ОЗУ —\nНЕ ДИАГНОЗ','Ориентируйся на работу системы.','cache'),
 ('НЕ ОТКЛЮЧАЙ\nФАЙЛ ПОДКАЧКИ','Он помогает Windows при нехватке памяти.','pagefile'),
 ('ПЕРЕЗАГРУЗИ\nИ СРАВНИ','Измеряй при одинаковой нагрузке.','repeat'),
 ('WINDOWS\nБЕЗ ТОРМОЗОВ','Проверяй, а не угадывай.','cta')]
heads=['ПОЧЕМУ ТОРМОЗИТ WINDOWS?','БЫСТРАЯ ПРОВЕРКА','ДИСПЕТЧЕР ЗАДАЧ','ЧТО МОЖЕТ ПОМОЧЬ','ЗАКРЫВАЙ БЕЗОПАСНО','ЗАПУСК ВМЕСТЕ С WINDOWS','ВАЖНЫ СИМПТОМЫ','НЕ МЕНЯЙ НАУГАД','СРАВНИ ДВА ЗАМЕРА','СОХРАНИ КАРУСЕЛЬ']
for i,(title,sub,kind) in enumerate(CARD,1):
 im=backdrop(i)
 jelly(im,870,410,.92 if i in [1,10] else .65)
 d=ImageDraw.Draw(im)
 box(d,(72,78,480,132),22,(7,63,83,235),(54,193,219))
 text(d,95,92,'ЦИФРОHELP   /   WINDOWS',20,CY,1)
 text(d,71,177,title,67,WH,1)
 text(d,76,442,sub,30,MUT)
 box(d,(73,593,1005,1175),34,(8,37,60,242),(51,172,208))
 text(d,110,638,heads[i-1],30,CY,1)
 if kind=='hero':
  text(d,112,736,'Когда памяти не хватает,',34,WH,1)
  text(d,112,792,'программы могут зависать.',33)
  ok(d,903,'Сначала проверим нагрузку.')
  ok(d,1001,'Ничего опасного не удаляем.')
 elif kind=='keys':
  for x,s in [(111,'Ctrl'),(337,'+'),(414,'Shift'),(680,'+'),(776,'Esc')]:
   if s=='+':text(d,x,762,s,37,AM,1)
   else:
    box(d,(x,748,x+(180 if s!='Shift' else 219),841),18,(12,71,96),(54,213,238))
    text(d,x+20,766,s,38,WH,1)
  text(d,111,915,'Открой вкладку «Процессы».',34)
  text(d,111,988,'Найди столбец «Память».',34)
 elif kind=='sort':
  for k,(lab,val,p) in enumerate([('Браузер','1 240 МБ',.85),('Редактор','730 МБ',.58),('Мессенджер','280 МБ',.3)]):
   y=736+k*126
   text(d,112,y,lab,35,WH,1);text(d,750,y+3,val,26,AM)
   box(d,(114,y+61,948,y+83),8,(13,67,82))
   box(d,(114,y+61,114+834*p,y+83),8,CY)
 elif kind=='browser':
  ok(d,747,'Закрой ненужные вкладки.')
  ok(d,862,'Проверь расширения браузера.')
  ok(d,978,'Перезапусти зависший браузер.')
 elif kind=='close':
  ok(d,747,'Сохрани открытые документы.')
  ok(d,859,'Закрой ненужную программу.')
  ok(d,971,'Снова проверь показатель.')
 elif kind=='startup':
  text(d,113,754,'Ctrl + Shift + Esc',40,AM,1)
  text(d,113,838,'→ «Автозагрузка приложений»',30)
  ok(d,962,'Отключай лишь знакомое,')
  text(d,179,1015,'необязательное.',31)
 elif kind=='cache':
  text(d,114,746,'Высокий процент сам по себе',30,WH,1)
  text(d,114,804,'не означает неисправность.',30)
  ok(d,924,'Проверь, есть ли зависания.')
  ok(d,1022,'Повтори измерение позже.')
 elif kind=='pagefile':
  box(d,(105,739,963,954),26,(12,67,87,245),(66,188,219))
  text(d,140,784,'Виртуальная память',40,WH,1)
  text(d,140,872,'Автоматическое управление',29,CY)
  text(d,111,1016,'Отключение может вызвать сбои.',31)
 elif kind=='repeat':
  for j,(lab,p) in enumerate([('До проверки',.86),('После проверки',.52)]):
   y=754+j*170;text(d,114,y,lab,34,WH,1)
   box(d,(114,y+62,943,y+101),9,(11,61,78))
   box(d,(114,y+62,114+829*p,y+101),9,AM if j==0 else CY)
  text(d,114,1114,'Схема условная. Сравни свои цифры.',24,MUT)
 elif kind=='cta':
  text(d,114,750,'Теперь ты знаешь,',38)
  text(d,114,817,'где искать причину.',38,WH,1)
  box(d,(105,901,964,1095),26,(125,71,16,240),AM)
  text(d,145,932,'ГАЙД «WINDOWS',39,WH,1)
  text(d,145,997,'БЕЗ ТОРМОЗОВ»',39,WH,1)
  text(d,145,1055,'Ссылка в профиле «ЦифроHelp»',25)
 d.line((76,1252,1000,1252),fill=(47,117,149),width=2)
 text(d,78,1279,'ЦИФРОHELP',25,CY,1)
 text(d,795,1289,f'WINDOWS   •   {i:02d}/10',18,MUT)
 im.convert('RGB').save(f'{D}/{i:02d}_carousel.jpg','JPEG',quality=92,optimize=True)
print('Created 10 individual JPEG slides')