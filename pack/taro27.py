# -*- coding: utf-8 -*-
import os
os.chdir(os.path.expanduser('~/nebogovorit.ru/public_html'))
# 1. engine: ключ taro27
p = 'engine.php'
s = open(p, encoding='utf-8').read()
if "'taro27'" not in s:
    k = "  'lyubov27' =>"
    assert s.count(k) == 1
    i = s.find(k); j = s.find('\n', i) + 1
    new = "  'taro27' => ['t' => 'Таро на 2027 год', 'type' => 'year', 'f' => 'карта года и расклад на 2027 год: что показывают карты по отрезкам года, на что опираться и чего не форсировать'],\n"
    s = s[:j] + new + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('engine ok')
# 2. taro.php: транзиты 2027 для вопросов type=year
p = 'taro.php'
s = open(p, encoding='utf-8').read()
if "транзиты_2027" not in s:
    k = "  return ['data' => $data, 'spread' => $spread];\n}"
    assert s.count(k) == 1
    add = ("  if ((QUESTIONS[$q]['type'] ?? '') === 'year') {\n"
           "    $Np = array_intersect_key($N, array_flip(PERSONAL_POINTS));\n"
           "    $data['транзиты_2027'] = transits_period($Np, jd_local('2027-01-01', '00:00', 'UTC'), jd_local('2027-12-31', '00:00', 'UTC'));\n"
           "    unset($data['транзиты_сегодня']);\n"
           "  }\n")
    s = s.replace(k, add + k, 1)
    k2 = '. "\\n\\nРасчёт и расклад:\\n"'
    assert s.count(k2) == 1, s.count(k2)
    note = ('. ((QUESTIONS[$q][\'type\'] ?? \'\') === \'year\' ? "\\nЭто вопрос на 2027 год: привязывай карты расклада к отрезкам из «транзиты_2027» — даты и месяцы бери только оттуда, не пиши про «сегодня»." : \'\') ')
    s = s.replace(k2, note + k2, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('taro ok')
