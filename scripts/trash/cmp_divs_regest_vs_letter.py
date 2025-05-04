import os, re


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        divs_regest = re.findall(r'<p xml:id="regest\d+">', s, flags=re.S)
        divs_letter = re.findall(r'div xml:id="div\d+"', s, flags=re.S)
        if len(divs_letter) != len(divs_letter): print("*Warning", f)
        #if len(divs_letter) != 0 or len(divs_letter) != 0: print(f, len(divs_letter), len(divs_letter))
