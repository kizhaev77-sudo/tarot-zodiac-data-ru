# -*- coding: utf-8 -*-
import os
os.chdir(os.path.expanduser('~/nebogovorit.ru/public_html'))
p = 'astrokalendar.html'
s = open(p, encoding='utf-8').read()
if 'Что это значит в гороскопе знаков' not in s:
    k = '<h2>Общий календарь и Ваша карта</h2>'
    assert s.count(k) == 1
    t = 'Астрокалендарь показывает события неба по датам, а гороскоп знака — то, как они ложатся на Ваш знак. Откройте <a href="/goroskop/">гороскоп на месяц для 12 знаков</a>, а для обзора всего года — <a href="/goroskop-na-2027-god.html">гороскоп на 2027 год</a>.'
    s = s.replace(k, '<h2>Что это значит в гороскопе знаков</h2><p>%s</p>' % t + k)
    open(p, 'w', encoding='utf-8').write(s)
print('done')
