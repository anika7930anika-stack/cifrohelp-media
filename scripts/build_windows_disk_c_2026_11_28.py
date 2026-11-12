from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math,random,os
D='instagram/2026-11-28_windows_disk_c_10_cards'
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
 ('МАЛО МЕСТА\nНА ДИСКЕ C?','Не спеши удалять системные файлы.','hero'),
 ('ПРОВЕРЬ\nХРАНИЛИЩЕ','Узнай, что на самом деле занимает место.','storage'),
 ('СМОТРИ\nКАТЕГОРИИ','Большую часть места занимает не всегда мусор.','categories'),
 ('ВРЕМЕННЫЕ\nФАЙЛЫ','Сначала изучи список. Затем решай.','temp'),
 ('ПАПКА\n«ЗАГРУЗКИ»','Здесь могут быть нужные документы.','downloads'),
 ('ПРОВЕРЬ\nКОРЗИНУ','Удалённые файлы ещё занимают место.','bin'),
 ('НАЙДИ\nКРУПНЫЕ ФАЙЛЫ','Ищи видео, архивы и старые копии.','large'),
 ('УДАЛИ ЛИШНИЕ\nПРИЛОЖЕНИЯ','Используй только штатное удаление.','apps'),
 ('НЕ ЧИСТИ\nВСЛЕПУЮ','Системные папки нельзя удалять как мусор.','warn'),
 ('ПРОВЕРЬ\nРЕЗУЛЬТАТ','И сохрани план безопасной очистки.','cta')]
heads=['НАЧНИ С ДИАГНОСТИКИ','ВСТРОЕННЫЙ ИНСТРУМЕНТ','ГДЕ ИСКАТЬ ПРИЧИНУ','ОЧИЩАЙ ОСОЗНАННО','ПЕРЕД УДАЛЕНИЕМ — ПРОВЕРЬ','НЕ ПОТЕРЯЙ ВАЖНОЕ','КУДА УШЛИ ГИГАБАЙТЫ?','УДАЛЯЙ ЧЕРЕЗ WINDOWS','ЧТО ДЕЛАТЬ НЕЛЬЗЯ','ЗАКРЕПИ РЕЗУЛЬТАТ']
for i,(title,sub,kind) in enumerate(CARD,1):
 im=backdrop(i+30)
 jelly(im,870,410,.90 if i in [1,10] else .70)
 d=ImageDraw.Draw(im)
 box(d,(72,78,480,132),22,(7,63,83,235),(54,193,219))
 text(d,95,92,'ЦИФРОHELP   /   WINDOWS',20,CY,1)
 text(d,71,177,title,64,WH,1)
 text(d,76,444,sub,28,MUT)
 box(d,(73,593,1005,1175),34,(8,37,60,242),(51,172,208))
 text(d,110,638,heads[i-1],28,CY,1)
 if kind=='hero':
  text(d,112,748,'Мало свободного места?',38,WH,1)
  ok(d,866,'Проверим, что его заняло.')
  ok(d,973,'Освободим без риска для Windows.')
 elif kind=='storage':
  text(d,112,750,'Параметры',42,WH,1)
  text(d,112,817,'→ Система → Память',39,AM,1)
  ok(d,930,'Выбери диск C.')
  text(d,112,1018,'Посмотри общий объём и свободное место.',27,MUT)
 elif kind=='categories':
  for k,(lab,p) in enumerate([('Приложения',.80),('Временные файлы',.46),('Документы',.25)]):
   y=747+k*123
   text(d,112,y,lab,33,WH,1)
   box(d,(114,y+57,943,y+78),8,(13,67,82))
   box(d,(114,y+57,114+829*p,y+78),8,CY if k!=1 else AM)
  text(d,114,1122,'Пример категорий. Проверь свои данные.',23,MUT)
 elif kind=='temp':
  text(d,112,750,'Память → Временные файлы',32,AM,1)
  ok(d,838,'Открой категории очистки.')
  ok(d,934,'Проверь каждую галочку.')
  text(d,111,1034,'Не выбирай нужные файлы',29,WH,1)
  text(d,111,1090,'ради быстрой очистки.',29)
 elif kind=='downloads':
  text(d,112,749,'Проводник → Загрузки',34,AM,1)
  ok(d,841,'Отсортируй файлы по размеру.')
  ok(d,940,'Открой незнакомые названия.')
  text(d,112,1043,'Удаляй только то, что не нужно.',28,WH,1)
 elif kind=='bin':
  text(d,112,749,'Открой «Корзину»',39,AM,1)
  ok(d,849,'Посмотри её содержимое.')
  ok(d,950,'Восстанови нужные файлы.')
  text(d,112,1059,'Только после этого очищай.',28,WH,1)
 elif kind=='large':
  ok(d,748,'Проверь папки с видео.')
  ok(d,852,'Найди старые ZIP и архивы.')
  ok(d,956,'Убедись, что есть копия.')
  text(d,112,1081,'Потом переноси или удаляй.',29,AM,1)
 elif kind=='apps':
  text(d,112,751,'Параметры → Приложения',33,AM,1)
  text(d,112,811,'→ Установленные приложения',30)
  ok(d,914,'Выбери ненужную программу.')
  ok(d,1020,'Нажми «Удалить».')
 elif kind=='warn':
  text(d,112,750,'Не удаляй вручную:',36,AM,1)
  ok(d,854,'Windows и Program Files.')
  ok(d,955,'Незнакомые системные папки.')
  text(d,112,1065,'Не ставь «чистильщики» из рекламы.',27,MUT)
 elif kind=='cta':
  text(d,113,741,'Вернись в «Память»',38,WH,1)
  text(d,113,804,'и сравни свободное место.',30)
  box(d,(105,907,963,1095),26,(115,65,18,240),AM)
  text(d,145,942,'ГАЙД «WINDOWS',39,WH,1)
  text(d,145,1007,'БЕЗ ТОРМОЗОВ»',39,WH,1)
  text(d,145,1062,'Подробные шаги — по ссылке в профиле',22,WH)
 d.line((76,1252,1000,1252),fill=(47,117,149),width=2)
 text(d,78,1279,'ЦИФРОHELP',25,CY,1)
 text(d,795,1289,f'WINDOWS   •   {i:02d}/10',18,MUT)
 im.convert('RGB').save(f'{D}/{i:02d}_carousel.jpg','JPEG',quality=92,optimize=True)
print('Created 10 individual JPEG slides')