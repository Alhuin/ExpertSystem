import re

ruleRegex = re.compile(r'((?:!*\(*\s*!*[A-Z]+\)*)(?:\s*(?:[+|\-^])\s*(?:!*\(*\s*!?[A-Z]+\)*)\s*\)*)*)\s*(<?=>?)\s*((?:!*\(*\s*?!?[A-Z]+\)*)(?:\s*(?:[+|\-^])\s*(?:!*\(*\s*!*[A-Z]\)*)+\s*\)*)*)')
elementRegex = re.compile(r'(^|[+|\-^])\s*(!?[A-Z]+)')
factsRegex = re.compile(r'^=([A-Z]*)')
queriesRegex = re.compile(r'^\?([A-Z]*)')
composedRegex = re.compile(r'^((?:!?[A-Z]+|\(.*\)))([+|^])(!?[A-Z]+|\(.+?\))$')
andRegex = re.compile(r'((?:!*\([A-Z]+\)|!*[A-Z]+|\(.+?\))\s*\+\s*(?:!*\([A-Z]+\)|!*[A-Z]+|\(.+?\)))')
orRegex = re.compile(r'((?:!*\([A-Z]+\)|!*[A-Z]+|\(.+?\))\s*\|\s*(?:!*\([A-Z]+\)|!*[A-Z]+|\(.+?\)))')
xorRegex = re.compile(r'((?:!*\([A-Z]+\)|!*[A-Z]+|\(.+?\))\s*\^\s*(?:!*\([A-Z]+\)|!*[A-Z]+|\(.+?\)))')
operatorsRegex = re.compile(r'[()!+^|]')
doubleNotRegex = re.compile(r'!!')
