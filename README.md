# UzbekLemmatizer
Uzbek Lemmatizer for Python. 
A Python package  to lemmatize Uzbek texts.

Use:
code1:

import UzbekLemmatizer as ltr
print(ltr.Lemma('keladiganlarning',full=True))

result1:
['keladiganlarning', 'kel', ['adigan', 'lar', 'ning'], [5, 5, 3]]

code2:

import UzbekLemmatizer as ltr

print(ltr.Lemma('keladiganlarning'))

result2:
kel
