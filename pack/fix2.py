# -*- coding: utf-8 -*-
import os, re, glob
os.chdir(os.path.expanduser('~/nebogovorit.ru/public_html'))
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
NOM = {'oven':'Овен','telec':'Телец','bliznecy':'Близнецы','rak':'Рак','lev':'Лев','deva':'Дева','vesy':'Весы','skorpion':'Скорпион','strelec':'Стрелец','kozerog':'Козерог','vodoley':'Водолей','ryby':'Рыбы'}
GEN = {'oven':'Овна','telec':'Тельца','bliznecy':'Близнецов','rak':'Рака','lev':'Льва','deva':'Девы','vesy':'Весов','skorpion':'Скорпиона','strelec':'Стрельца','kozerog':'Козерога','vodoley':'Водолея','ryby':'Рыб'}
G2S = dict((NOM[k], k) for k in NOM)
# 1. знаки: H2 с родительным падежом
n = 0
for p in sorted(glob.glob('goroskop/*/index.html')):
    s = rd(p)
    m = re.search(r'<h2>Гороскоп на ноябрь 2026: ([А-Яа-яЁё]+) по сферам жизни</h2>', s)
    if not m or m.group(1) not in G2S: continue
    g = GEN[G2S[m.group(1)]]
    s = s.replace(m.group(0), '<h2>Гороскоп %s на ноябрь 2026: по сферам жизни</h2>' % g)
    wr(p, s); n += 1
print('goroskop h2', n)
# 2. пары
n = 0
for p in sorted(glob.glob('sovmestimost/*/index.html')):
    slug = p.split('/')[1]
    if '-i-' not in slug: continue
    a, b = slug.split('-i-')
    if a not in NOM or b not in NOM: continue
    s = rd(p)
    h1 = re.search(r'<h1>Совместимость (.+?) в любви и браке</h1>', s)
    if not h1: print('skip h1', slug); continue
    pair = h1.group(1)
    para = ('<p>Это гороскоп совместимости %s: общий ориентир по знакам Солнца. Что происходит на небе в этом месяце для каждого знака — '
            '<a href="/goroskop/%s/">гороскоп %s на ноябрь</a> и <a href="/goroskop/%s/">гороскоп %s на ноябрь</a>.</p>' % (pair, a, GEN[a], b, GEN[b]))
    old = re.search(r'<p>Это гороскоп совместимости .*?</p>', s)
    if old:
        s = s.replace(old.group(0), para)
    else:
        m = re.search(r'<h2>(Общая картина|[^<]*: общая картина)</h2>', s)
        if not m: print('skip h2', slug); continue
        j = s.find('</p>', m.end())
        s = s[:j+4] + para + s[j+4:]
    s = s.replace('<h2>Общая картина</h2>', '<h2>Общая картина: гороскоп совместимости %s</h2>' % pair, 1)
    s = re.sub(r'<h2>([^<]*): общая картина</h2>', r'<h2>\1: гороскоп совместимости и общая картина</h2>', s, count=1)
    wr(p, s); n += 1
print('pairs', n)
# 3. страницы про небо: блок про гороскоп знаков
TXT = {
 'retrogradnyy-merkuriy.html': 'Ретроградный Меркурий проходит по знакам по-разному: в том знаке, где он стоит, на первый план выходят слова, договоры и дорога. Как это выглядит для каждого знака в этом месяце — в <a href="/goroskop/">гороскопе на месяц для 12 знаков</a>, а на весь 2027 год — в <a href="/goroskop-na-2027-god.html">гороскопе на 2027 год</a>.',
 'zatmeniya.html': 'Затмения принято читать по знаку, в котором они происходят: этот знак и связанные с ним сферы жизни затрагиваются сильнее. Что происходит на небе в этом месяце для каждого знака — в <a href="/goroskop/">гороскопе на месяц</a>, а на 2027 год — в <a href="/goroskop-na-2027-god.html">гороскопе на 2027 год</a>.',
 'novoluniya-i-polnoluniya.html': 'Новолуния и полнолуния проходят по знакам зодиака, и у каждого знака они попадают на свою сферу жизни. Как это выглядит для Вашего знака в этом месяце — в <a href="/goroskop/">гороскопе на месяц для 12 знаков</a>, а на 2027 год — в <a href="/goroskop-na-2027-god.html">гороскопе на 2027 год</a>.',
 'astrokalendar.html': 'Астрокалендарь показывает события неба по датам, а гороскоп знака — то, как они ложатся на Ваш знак. Откройте <a href="/goroskop/">гороскоп на месяц для 12 знаков</a>, а для обзора всего года — <a href="/goroskop-na-2027-god.html">гороскоп на 2027 год</a>.',
}
for p, t in TXT.items():
    s = rd(p)
    if 'Что это значит в гороскопе знаков' in s: continue
    k = '<h2>Частые вопросы</h2>'
    i = s.find(k)
    if i < 0: print('no faq', p); continue
    s = s[:i] + '<h2>Что это значит в гороскопе знаков</h2><p>%s</p>' % t + s[i:]
    wr(p, s); print('astro block', p)
