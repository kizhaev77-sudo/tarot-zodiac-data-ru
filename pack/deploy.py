# -*- coding: utf-8 -*-
import os, re, glob, shutil, sys
PK = os.path.expanduser('~/pk')
os.chdir(os.path.expanduser('~/nebogovorit.ru/public_html'))
log = []
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
def sub1(s, a, b, name, must=True):
    n = s.count(a)
    if n == 0:
        if must: raise SystemExit('NOT FOUND: ' + name)
        log.append('skip ' + name); return s
    log.append('%s x%d' % (name, n))
    return s.replace(a, b)

NEW = ['goroskop-na-2027-god.html', 'lyubov-v-2027-godu.html', 'kogda-budut-dengi.html', 'taro-na-2027-god.html']
for f in NEW:
    shutil.copy(os.path.join(PK, f), f); os.chmod(f, 0o644)
log.append('pages copied')

# ---- главная ----
s = rd('index.html')
s = sub1(s, '"t": "Что он(а) на самом деле ко мне чувствует?"', '"t": "Что он чувствует ко мне?"', 'home chuvstva')
s = sub1(s, '"t": "Почему у меня нет денег?"', '"t": "Когда у меня будут деньги и что им мешает?"', 'home dengi')
s = sub1(s, '"t": "Почему я не могу отпустить бывшего?"', '"t": "Как отпустить бывшего?"', 'home byvshiy')
s = sub1(s, '"t": "Почему у меня не складываются отношения?"', '"t": "Почему не складываются отношения?"', 'home otnosh')
oldord = 'var ORDER=["otnosh", "dengi", "byvshiy", "chuvstva", "lyubit", "zamuzh", "dengizod", "vernetsya", "vezet", "vmeste", "dumaet", "prednaz", "sovm"];'
newq = ('Q.goroskop27={"t":"Гороскоп на 2027 год","form":"one","wait":["Считаем карту…","Смотрим, где в 2027 году медленные планеты встают на Ваши точки…"],"note":"Дальше — про отрезки 2027 года, которые важны именно Вам.","h2":"Ваша формула"};\n'
        '  Q.lyubov27={"t":"Что ждёт меня в любви в 2027 году?","form":"one","wait":["Считаем карту…","Смотрим на Венеру и Луну в 2027 году…"],"note":"Дальше — про то, как у Вас складывается любовь в 2027 году.","h2":"Ваша формула"};\n'
        '  var ORDER=["vernetsya", "lyubit", "vmeste", "dumaet", "zamuzh", "prednaz", "chuvstva", "byvshiy", "otnosh", "dengi", "goroskop27", "lyubov27", "sovm", "dengizod", "vezet"];\n'
        '  var HIDE=["sovm", "dengizod", "vezet"];')
s = sub1(s, '  ' + oldord, '  ' + newq, 'home ORDER') if ('  ' + oldord) in s else sub1(s, oldord, newq, 'home ORDER')
s = sub1(s, "if(i>=5) b.classList.add('more');", "if(i>=5) b.classList.add('more');\n    if(HIDE.indexOf(id)>=0) b.style.display='none';", 'home hide')
s = sub1(s, "(ORDER.length-5)", "(ORDER.length-HIDE.length-5)", 'home morebtn')
wr('index.html', s)

# ---- /taro/ ----
s = rd('taro/index.html')
newqs = ('var QUESTIONS=[["vernetsya","Вернётся ли он(а)?"],["lyubit","Любит ли он меня?"],["vmeste","Будем ли мы вместе?"],["dumaet","Думает ли он обо мне?"],'
         '["zamuzh","Когда я выйду замуж?"],["prednaz","В чём моё предназначение?"],["chuvstva","Что он чувствует ко мне?"],["byvshiy","Как отпустить бывшего?"],'
         '["otnosh","Почему не складываются отношения?"],["dengi","Когда у меня будут деньги и что им мешает?"]];')
m = re.search(r'var QUESTIONS=\[\[.*?\]\];', s, re.S)
if not m: raise SystemExit('taro QUESTIONS not found')
s = s[:m.start()] + newqs + s[m.end():]; log.append('taro QUESTIONS')
blk = ('<p class="small" style="text-align:center;margin:22px 16px">Ещё по теме: <a href="/taro-na-2027-god.html">Таро на 2027 год</a> · '
       '<a href="/goroskop-na-2027-god.html">Гороскоп на 2027 год</a> · <a href="/lyubov-v-2027-godu.html">Любовь в 2027 году</a> · '
       '<a href="/kogda-budut-dengi.html">Когда у меня будут деньги</a></p>\n')
if 'taro-na-2027-god.html' not in s:
    i = s.find('<footer')
    if i < 0: raise SystemExit('taro footer not found')
    s = s[:i] + blk + s[i:]; log.append('taro links')
wr('taro/index.html', s)

# ---- гороскоп: H2 ----
n = 0
for p in sorted(glob.glob('goroskop/*/index.html')):
    s = rd(p)
    s2, k = re.subn(r'<h2>([А-Яа-яЁё]+): ноябрь 2026 по сферам жизни</h2>', r'<h2>Гороскоп на ноябрь 2026: \1 по сферам жизни</h2>', s)
    if k == 1: wr(p, s2); n += 1
log.append('goroskop h2: %d pages' % n)

# ---- совместимость ----
NAMES = {'oven':'Овен','telec':'Телец','bliznecy':'Близнецы','rak':'Рак','lev':'Лев','deva':'Дева','vesy':'Весы','skorpion':'Скорпион','strelec':'Стрелец','kozerog':'Козерог','vodoley':'Водолей','ryby':'Рыбы'}
n = 0
for p in sorted(glob.glob('sovmestimost/*/index.html')):
    slug = p.split('/')[1]
    if '-i-' not in slug: continue
    a, b = slug.split('-i-')
    if a not in NAMES or b not in NAMES: continue
    s = rd(p)
    if 'Это гороскоп совместимости' in s: continue
    h1 = re.search(r'<h1>Совместимость (.+?) в любви и браке</h1>', s)
    i = s.find('<h2>Общая картина</h2>')
    if not h1 or i < 0: continue
    j = s.find('</p>', i)
    add = ('<p>Это гороскоп совместимости %s: общий ориентир по знакам Солнца. Гороскоп на месяц для каждого знака — <a href="/goroskop/%s/">%s</a> и <a href="/goroskop/%s/">%s</a>.</p>'
           % (h1.group(1), a, NAMES[a], b, NAMES[b]))
    s = s[:j+4] + add + s[j+4:]
    wr(p, s); n += 1
log.append('sovm pages: %d' % n)

# ---- деньги ----
p = 'dengi-po-znaku-zodiaka.html'
s = rd(p)
s = sub1(s, '<h2>Деньги по 12 знакам зодиака</h2>', '<h2>Денежный гороскоп: деньги по 12 знакам зодиака</h2>', 'dengi h2')
s = s.replace('Почему у меня нет денег', 'Когда у меня будут деньги и что им мешает')
s = sub1(s, 'Выберите на главной вопрос «Я и деньги по знакам зодиака» или «', 'Выберите на главной вопрос «', 'dengi howto', False)
s = sub1(s, 'в разборе на главной есть два вопроса:', 'в разборе есть два вопроса:', 'dengi two', False)
if 'kogda-budut-dengi' not in s:
    s, k = re.subn(r'(<a href="/retrogradnyy-merkuriy\.html">ретроградный Меркурий</a>\.)', r'\1 Отдельная страница про сроки — <a href="/kogda-budut-dengi.html">когда у меня будут деньги</a>.', s, count=1)
    log.append('dengi link %d' % k)
wr(p, s)

# ---- прочие страницы с названиями плиток ----
for p, pairs in [
  ('kak-otpustit-byvshego.html', [('Почему я не могу отпустить бывшего', 'Как отпустить бывшего')]),
  ('vernetsya-li-byvshiy.html', [('Почему я не могу отпустить бывшего', 'Как отпустить бывшего')]),
  ('chto-on-chuvstvuet-ko-mne.html', [('Что он(а) на самом деле ко мне чувствует?', 'Что он чувствует ко мне?')]),
  ('pochemu-mne-ne-vezet.html', [('Выберите на главной вопрос «Почему мне не везёт?».', 'Нажмите кнопку выше — откроется вопрос «Почему мне не везёт?».')]),
]:
    s = rd(p)
    for a, b in pairs: s = sub1(s, a, b, p, False)
    wr(p, s)

# ---- sitemap ----
s = rd('sitemap.xml')
add = ''
for f in NEW:
    u = 'https://nebogovorit.ru/' + f
    if u not in s:
        add += '<url>\n    <loc>%s</loc>\n  </url>\n' % u
s = s.replace('</urlset>', add + '</urlset>')
wr('sitemap.xml', s); log.append('sitemap +%d' % add.count('<url>'))
print('\n'.join(log))
