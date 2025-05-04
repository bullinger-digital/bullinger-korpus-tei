# TeX2TEI-Conversion

## Procedure

1. Change to directory "tex2tei" (under scripts): `cd scripts/tex2tei/`
2. Create (if not exists) a new directory "input": `mkdir input` (besides "output")
3. Copy the tex-files you wish to convert into the newly created directory "input/"
4. Execute the script: `python main.py` (within the directory "tex2tei")
5. Check the output. If it meets the expectations, copy/paste the newly created xml-files manually from `output/` into `data/letters/`

Note: The execution of `main.py` clears/overwrites the directory `output/`.
That is, do not change anything within the output directory - otherwise, changes might get lost...

## Preconditions

Make sure, that the filenames meet the following convention:

`<EditionID>-<TustepID>-<Senders>_an_<Addressees>,_<Place>,_<Date>.tex`

Example: `3102-18000-Bullinger_an_Joachim_Vadian,_Zürich,_3._Januar_1548.tex`

- separators 2x'-', 1x'\_an\_' & 2x',_'
- all blanks should be replaced by '_'
- concat multiple senders/addressees by '\_&\_'

Example: `034-18031-Matthias_Erb_an_Bullinger_&_Rudolf_Gwalther,_Reichenweier,_10._Februar_1548.tex`

Date-Examples:

- "when": 23._Mai_1985
- "notBefore": 23._Mai_1985- (ending '-')
- "notAfter": -23._Mai_1985 (starting '-')
- range: 23._Mai_1985-4._April_1988

Examples:
- `020-18336-Bullinger_an_Rudolf_Gwalther,_Zürich,_[28.]_Januar_1548-[31.]_Januar_1548.tex`
- `092-18348-Johann_Valentin_Furtmüller_an_[Bullinger],_St._Gallen,_-26._April_1548.tex`

Fields containing angular brakets ([...]) will be associated with the [TEI-]attribute «cert="low"».

## Errorhandling

1. In case of warnings durings the execution, try to fix them by adjusting the `config.py`-file accordingly.
2. In case of validation errors, adjust the script or fix the issues manually...
