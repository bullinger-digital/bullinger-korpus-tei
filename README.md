# BULLINGER CORPUS (TEI-XML)

PROVISIONAL VERSION (v3.2)

### Contents

- Letters: data/letters/\*.xml [13'154 files]

  * IDs $>=$ 10'013: HBBW, edited letters
  * IDs $<$ 10'013: unedited transcriptions
  * Source: UZH/IRG, unless otherwise noted
  *
- Listings:

  * Persons (correspondents): data/persons.xml
  * Institutions (organisations): data/orgs.xml
  * Titles (professions): data/roles.xml
  * Places: data/places.xml
  * Archives: data/archives.xml
  *
- Portraits: data/portraits/*.(jpg|png)
-

### Validation

- DTD: https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng
- Documentation: https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-TEI.html
- Script: scripts/validate.py
-

### Remarks

- the corpus still contains some non-TEI-Elements (qv/zfn)
- the IDs (resp. references) of entities in texts (persons/places) currently refer to a different indexfile. They will be mapped to their correct ID, soon.
- the TEI-standard doesn't allow blanks (' ') in attribut values, which is why they have been escaped by "__" (that is, two consecutive underscores). Consequently, this mapping has to be reversed to retrieve the proper attribute values (e.g. to query scan images from our server or to display values correctly).
- Design Guides: Feel free to give your creativity free rein. Otherwise, get inspired by:
  - the classical (printed) edition: http://teoirgsed.uzh.ch/
  - bullinger-digital: https://www.bullinger-digital.ch/

### Open Questions@K&R

Depending on previous feedback, there are no issues with the index files (anymore). However, the validation of these files outputs two errors:

```
TEI validation error: archives.xml Did not expect element org there, line 29
TEI validation error: persons.xml Did not expect element person there, line 29
```

How do we have to change the structure of «persons.xml» and «archives.xml» to avoid those issues?

---

**Volk et al., Mars 2, 2023**

**Contact: bernard.schroffenegger@uzh.ch**
