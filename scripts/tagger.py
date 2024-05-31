
''' Zürich '''

import os
import re

e_ = ["Tigurin&#281;", "Tigurinenses", "Tigurinensis", "Tigurinorum", "Tigurinum", "Tigurinam", "Tigurinae",
      "Tigurinis", "Tigurinos", "Tigurinus", "Tigurini", "Tigurino", "Tigurinę", "Tigurina", "Tigurum", "Tiguri",
      "Tiguro", "Zürych", "Zurich", "Zurych", "Zurin&#281;", "Zurinę", "Zürich", "Zurik", "Turcicae"]

e = []
z = '\[?\(?\)?\]?'
for a in e_:
    new_ = z
    for letter in a: new_ += letter + z;
    e.append(new_)

regex = '([> ])(' + '|'.join(e) + ')([!?.,;:< ])'


root = "data/letters"
for f in os.listdir(root):
    p = os.path.join(root, f)
    if (os.path.isfile(p) and re.match(r'.*?\.xml', f)):
        with open(p) as fi: s = fi.read()
        m = re.match(r'.*(<text xml:lang.*?</text>).*', s, flags=re.S)
        if m:
            x0 = m.group(1)
            x1 = re.sub(regex, r'\1<placeName ref="l587" type="auto_name">\2</placeName>\3', x0, flags=re.S)
            s = re.sub(re.escape(x0), x1, s, flags=re.S)
            with open(root+'/'+f, 'w') as fo: fo.write(s)
