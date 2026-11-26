# -*- coding: utf-8 -*-
import os,re
os.chdir(os.path.expanduser('~/nebogovorit.ru/public_html'))
p='taro/index.html'
s=open(p,encoding='utf-8').read()
if '"taro27"' not in s:
    k='["dengi",'
    assert s.count(k)==1
    i=s.find(k); j=s.find(']',i)+1
    add=',["goroskop27","Гороскоп на 2027 год"],["lyubov27","Что ждёт меня в любви в 2027 году?"],["taro27","Таро на 2027 год"]'
    s=s[:j]+add+s[j:]
    open(p,'w',encoding='utf-8').write(s)
print(len(re.findall(r'\["[a-z0-9]+","',s.split('var QUESTIONS=')[1].split('];')[0])))
