#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re


class Parser:

    def __init__(self, matcher):
        self.root = matcher.config["PATHS"]["OUTPUT"]
        self.root_letters = matcher.config["PATHS"]["CORPUS"]["LETTERS"]
        self.matcher = matcher
        self.show_warnings = 0
        self.print_info = True
        self.footnotes = []

    def parse_files(self):
        if self.print_info: print("- transforming files ...")
        for f in sorted(os.listdir(self.root)):
            #print("\rProcessing "+f+3*'\t', end="", flush=True)
            if f.endswith('.xml'):
                self.footnotes = []
                with open(os.path.join(self.root, f)) as fi: s = fi.read()
                f_id = re.match(r'(.*)\.xml', f).group(1)
                s = self.rm_comments(s)
                s = self.rm_blanks(s)
                s = self.rm_appendage(s)
                s = self.rm_tex_layout(s)
                s = self.normalize(s)
                s = self.map_tables(s)
                s = self.map_tex2tei(s)
                s = self.map_lists(s)
                s = self.page_ref_warnings(s, f)
                s = self.map_attachments(s)
                s = self.map_qv_nr(s)
                s = self.map_recursively(s)
                s = self.map_letter(s, f)
                s = self.insert_notes(s)
                s = self.insert_lists(s)
                s = self.insert_tables(s)
                s = self.insert_seqs(s)
                s = self.insert_blanks(s)
                t = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'  # root
                t += '<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="file' + str(f_id) + '" type="Brief" source="HBBW-'+str(self.matcher.config["EDITION_NUMBER"])+'" n="' + self.matcher.data[f_id]["id_irg"] + '">\n'
                t += '\t<teiHeader xml:lang="de">\n'  # head
                t += '\t\t<fileDesc>\n'
                t += '\t\t\t<titleStmt>\n'
                t += '\t\t\t\t<title subtype="file">'+self.get_title(s, f)+'</title>\n'
                t += '\t\t\t</titleStmt>\n'
                t += '\t\t\t<publicationStmt>\n'
                t += '\t\t\t\t<publisher>Volk et al.</publisher>\n'
                t += '\t\t\t\t<pubPlace>Zürich</pubPlace>\n'
                t += '\t\t\t\t<address>\n'
                t += '\t\t\t\t\t<addrLine>Institut für Computerlinguistik</addrLine>\n'
                t += '\t\t\t\t\t<addrLine>Andreasstrasse 15</addrLine>\n'
                t += '\t\t\t\t\t<addrLine>8050 Zürich</addrLine>\n'
                t += '\t\t\t\t\t<addrLine>Schweiz</addrLine>\n'
                t += '\t\t\t\t</address>\n'
                t += '\t\t\t\t<authority>Universität Zürich</authority>\n'
                t += '\t\t\t\t<idno subtype="url">https://www.bullinger-digital.ch/</idno>\n'
                t += '\t\t\t\t<date when="'+str(self.matcher.config["YEAR"])+'"/>\n'
                t += '\t\t\t</publicationStmt>\n'
                t += '\t\t\t<sourceDesc>\n'
                t += '\t\t\t\t<bibl ref="'+str(self.matcher.config["ID_BIB"])+'" n="'+self.matcher.data[f_id]["id_irg"]+'" type="transcription"/>\n'#+self.matcher.config["BIBLIOGRAPHY"]+'</bibl>\n'
                t += '\t\t\t\t<bibl ref="'+str(self.matcher.config["ID_BIB"])+'" n="'+self.matcher.data[f_id]["id_irg"]+'" type="regest"/>\n'#+self.matcher.config["BIBLIOGRAPHY"]+'</bibl>\n'
                t += '\t\t\t\t<bibl ref="'+str(self.matcher.config["ID_BIB"])+'" n="'+self.matcher.data[f_id]["id_irg"]+'" type="footnotes"/>\n'#+self.matcher.config["BIBLIOGRAPHY"]+'</bibl>\n'
                documents, regest, printed = self.get_signature(s, f), self.get_regest(s), self.get_printed(s)
                if documents or regest or printed:
                    t += '\t\t\t\t<msDesc'\
                         +((' type="'+documents[0][0]+'"') if documents else '') \
                         +((' subtype="'+documents[0][1]+'"') if documents and documents[0][1] else '')+'>\n'
                    if documents and (documents[0][2] or documents[0][3]):
                        t += '\t\t\t\t\t<msIdentifier>\n'
                        if documents[0][2]: t += '\t\t\t\t\t\t<repository ref="'+documents[0][2]+'"/>\n'
                        if documents[0][3]: t += '\t\t\t\t\t\t<idno'+((' subtype="'+documents[0][1]+'"') if documents[0][1] else '')+'>'+documents[0][3]+'</idno>\n'
                        t += '\t\t\t\t\t</msIdentifier>\n'
                    if regest:
                        t += '\t\t\t\t\t<msContents>\n'
                        t += '\t\t\t\t\t\t<summary>\n'
                        t += regest
                        t += '\t\t\t\t\t\t</summary>\n'
                        t += '\t\t\t\t\t</msContents>\n'
                    if printed:
                        t += '\t\t\t\t\t<additional>\n'
                        t += '\t\t\t\t\t\t<listBibl>\n'
                        for p in printed:
                            t += '\t\t\t\t\t\t\t<bibl type="Gedruckt"'+((' subtype="'+p[0]+'"') if p[0] else '')+'>\n'
                            t += '\t\t\t\t\t\t\t\t<title>'+re.sub(r'<.*?>', '', p[1], flags=re.S)+'</title>\n'
                            t += '\t\t\t\t\t\t\t</bibl>\n'
                        t += '\t\t\t\t\t\t</listBibl>\n'
                        t += '\t\t\t\t\t</additional>\n'
                    t += '\t\t\t\t</msDesc>\n'
                if len(documents)>1:
                    for d in documents[1:]:
                        t += '\t\t\t\t<msDesc' \
                             + ((' type="' + d[0] + '"') if d[0] else '') \
                             + ((' subtype="' + d[1] + '"') if d[1] else '') + '>\n'
                        if d[2] or d[3]:
                            t += '\t\t\t\t\t<msIdentifier>\n'
                            if d[2]: t += '\t\t\t\t\t\t<repository ref="' + d[2] + '"/>\n'
                            elif documents[0][2]: t += '\t\t\t\t\t\t<repository ref="' + documents[0][2] + '"/>\n'
                            if d[3]: t += '\t\t\t\t\t\t<idno'+((' subtype="'+d[1]+'"') if d[1] else '')+'>'+d[3]+'</idno>\n'
                            t += '\t\t\t\t\t</msIdentifier>\n'
                        t += '\t\t\t\t</msDesc>\n'
                t += '\t\t\t</sourceDesc>\n'
                t += '\t\t</fileDesc>\n'
                t += '\t\t<profileDesc>\n'
                t += '\t\t\t<correspDesc ref="https://www.bullinger-digital.ch/letter/'+re.match(r'(\d+).*', f, flags=re.S).group(1)+'">\n'
                senders, addressees = self.matcher.data[f_id]["senders"], self.matcher.data[f_id]["addressees"]
                place, date = self.matcher.data[f_id]["place"], self.matcher.data[f_id]["date"]
                pd, context = self.get_placedate(s), self.get_element_from_corpus(f, "correspContext")
                lang_usage = self.get_element_from_corpus(f, "langUsage")
                if senders or place or date:
                    t += '\t\t\t\t<correspAction type="sent">\n'
                    for s_ in senders: t += '\t\t\t\t\t<persName ref="'+s_+'" cert="'+senders[s_][1]+'"/>\n'
                    if place: t += '\t\t\t\t\t<placeName ref="'+place["id"]+'" cert="'+place["cert"]+'"/>\n'
                    if date: t += '\t\t\t\t\t<date'\
                        +((' when="'+date["when"]+'"') if 'when' in date else (
                          ((' notBefore="'+date["notBefore"]+'"') if 'notBefore' in date and date['notBefore'] else '')
                          +((' notAfter="' + date["notAfter"] + '"') if 'notAfter' in date and date['notAfter'] else '')
                        ))+' cert="'+date["cert"]+'"'+(('>'+pd[1]+'</date>\n') if pd[1] else '/>\n')
                    t += '\t\t\t\t</correspAction>\n'
                if addressees:
                    t += '\t\t\t\t<correspAction type="received">\n'
                    for a_ in addressees: t += '\t\t\t\t\t<persName ref="'+a_+'" cert="'+addressees[a_][1]+'"/>\n'
                    t += '\t\t\t\t</correspAction>\n'
                if context: t += '\t\t\t\t'+self.filter_context(context).strip()+'\n'
                t += '\t\t\t</correspDesc>\n'
                if lang_usage: t += '\t\t\t'+lang_usage.strip()+'\n'
                t += '\t\t</profileDesc>\n'
                key_words = self.get_key_words_from_corpus(f)
                if key_words: t += '\t\t'+key_words+'\n'
                t += '\t\t<revisionDesc>\n'
                t += '\t\t\t<change status="untouched">init</change>\n'
                t += '\t\t</revisionDesc>\n'
                t += '\t</teiHeader>\n'
                facsimile = self.get_element_from_corpus(f, 'facsimile')
                if facsimile: t += '\t'+facsimile.strip()+'\n'
                t += s
                t += '</TEI>'
                t = self.insert_meta_fns(t)
                t = self.cleanup(t)
                t = self.set_numbers(t)
                t = self.fix_structral_issues(t)
                t = self.rename_notes(t)
                t = re.sub(r'(<bibl>)\s*(HBBW|hbbw)\s*\-?\s*(</bibl>)\s*\-?\s*([IVX\d+]+)', r'\1\2 \4\3', t, flags=re.S)
                with open(os.path.join(self.root, f), 'w') as fo: fo.write(t)

    def rm_comments(self, s): return re.sub(r'([^\\]|^)%[^\n]*', r'\1', s, flags=re.S)
    def rm_blanks(self, s): return re.sub(r'\n\s*\n', '\n', s, flags=re.S)
    def rm_appendage(self, s): return re.sub(r'(\n)\s*(\\end\{brieftext\}).*', r'\1\2', s, flags=re.S)
    def rm_tex_layout(self, s):
        s = re.sub(r'\\(newpage|n?o?pagebreak|relax|vskip)', '', s, flags=re.S)
        s = re.sub(r'\-?\d+\.?\d*\\baselineskip', '', s, flags=re.S)
        s = re.sub(r'\\vadjust(\{[^}]*\}|)', '', s, flags=re.S)
        s = re.sub(r'\\KORRlinespenalties\{[^\{\}]*\}', '', s, flags=re.S)
        s = re.sub(r'\\KORRnofirstline(\{[^\{\}]*\}|)', '', s, flags=re.S)
        s = re.sub(r'\\count\\footinsB=\-?\d+\.?\d*', '', s, flags=re.S)
        s = re.sub(r'\\looseness=\-?\d+\.?\d*', '', s, flags=re.S)
        s = re.sub(r'\\parfillskip=\d+\S*', '', s, flags=re.S)
        s = re.sub(r'\\(par|noindent)', '', s, flags=re.S)
        s = re.sub(r'\\KORR\{[^\{\}]*(\{\s*\}|)[^\{\}]*\}', '', s, flags=re.S)
        s = re.sub(r'\\small\{([^\{\}]*)\}', r'\1', s, flags=re.S)
        s = re.sub(r'\\mbox\{([^\{\}]*)\}', r'\1', s, flags=re.S)
        s = re.sub(r'\~', ' ', s, flags=re.S)
        s = re.sub(r'\\,', ' ', s, flags=re.S)
        s = re.sub(r'-\-', '-', s, flags=re.S)
        s = re.sub(r'\\\\\*', ' ', s, flags=re.S)
        s = re.sub(r'[ ]+', ' ', s, flags=re.S)
        s = re.sub(r'([\{\[])\s*\n([^\\])', r'\1\2', s, flags=re.S)
        s = re.sub(r'\s*\n', r'\n', s, flags=re.S)
        s = re.sub(r'\n[ ]+', r'\n', s, flags=re.S)
        s = re.sub(r'\s*\n([^\\])', r' \1', s, flags=re.S)
        return s
    def normalize(self, s):
        s = re.sub(r'\s*(\\zupar)', r'\n\1', s, flags=re.S)
        s = re.sub(r'\s*(\\end)', r'\n\1', s, flags=re.S)
        s = re.sub(r'[ ]+', ' ', s, flags=re.S)
        s = re.sub(r'\s*\n', '\n', s, flags=re.S)
        s = re.sub(r'(\!Tagsatzung)\d+', r'\1', s, flags=re.S)
        s = re.sub(r'([^\s\{])@\\[^\{\}\s@!\\]*\!([^\{\}\@\!\\]*),\s*(\})', r'\1, \2\3', s, flags=re.S)
        s = re.sub(r'@\\[^\{\}\@\!\\]*\s*(\})', r'\1', s, flags=re.S)
        s = re.sub(r'@\\[^\{\}\@\!\\]*!\s*(\})', r'\1', s, flags=re.S)
        s = re.sub(r'@\\[^\{\}\@\!\\]*!([^\{\}\@\!\\]*)\}', r', \1}', s, flags=re.S)
        s = re.sub(r'\!\\[^\{\}!]*\}', r'}', s, flags=re.S)
        s = re.sub(r'([^\\])\\ ', r'\1 ', s, flags=re.S)
        s = re.sub(r'\s+\}', '}', s, flags=re.S)
        s = re.sub(r'@\\[^\{\}\@\\!]*!([^\{\}\@\\!]*)!([^\{\}\@\\!]*),\}', r', \1\2}', s, flags=re.S)
        s = re.sub(r'@\\[^\{\}\@\\!]*!([^\{\}\@\\!]*)!([^\{\}\@\\!]*)\}', r', \1\2}', s, flags=re.S)
        s = re.sub(r'@\\[^\{\}]*\}', r'}', s, flags=re.S)
        s = re.sub(r'\\GrZ?\{([^\{\}]*)\}', r'<foreign xml:lang="el">\1</foreign>', s, flags=re.S)
        s = re.sub(r'@\\[^\{\}@\!\\]*!([^\{\}\@\!\\]*)!([^\{\}\@\!\\]*\})', r', \1 \2', s, flags=re.S)
        s = re.sub(r'\\Anfz\{([^\{\}]*)\}', r'«\1»', s, flags=re.S)
        s = re.sub(r'\{\s*\}', '', s, flags=re.S)
        s = re.sub(r'(\\HBreg\{[^\{\}\!\@]*)@[^\{\}!@]*!([^\{\}!@]*)!([^\{\}!@]*),(\})', r'\1; \2, \3\4', s, flags=re.S)
        s = re.sub(r'(\\HBreg\{[^\{\}\!\@]*)@[^\{\}!@]*!([^\{\}!@]*)!([^\{\}!@]*)(\})', r'\1; \2, \3\4', s, flags=re.S)
        s = re.sub(r'(\\HBreg\{[^\{\}\!\@]*)@[^\{\}!@]*!([^\{\}!@]*),(\})', r'\1, \2\3', s, flags=re.S)
        s = re.sub(r'(\\HBreg\{[^\{\}\!\@]*)@[^\{\}!@]*!([^\{\}!@]*)(\})', r'\1, \2\3', s, flags=re.S)
        s = re.sub(r'(\\HBreg\{)[^\{\}\!\@]*@([^\{\}!@]*),\s*(\})', r'\1\2\3', s, flags=re.S)
        s = re.sub(r'(\\HBreg\{)[^\{\}\!\@]*@([^\{\}!@]*)\s*(\})', r'\1\2\3', s, flags=re.S)
        s = re.sub(r'\\kzu', '', s, flags=re.S)
        s = re.sub(r'\s*(\\Anm)', r'\1', s, flags=re.S)
        s = re.sub(r'\n\s*(\\zzl)', r' \1', s, flags=re.S)
        s = re.sub(r'\\AnhangNr\{([^\{\}]*)\}\{([^\{\}]*)\}', r'\\HBBWNummer{\2}', s, flags=re.S)
        s = re.sub(r'\\EA', r'<bibl>EA</bibl>', s, flags=re.S)
        s = re.sub(r'\\TextkritAnm\{([^\{\}]*)\}', r'<hi rend="italic">\1</hi>', s, flags=re.S)
        return s
    def map_tables(self, s):
        s = re.sub(r'\s*\\(begin|end)\{center\}\s*', '\n', s, flags=re.S)
        s = re.sub(r'(m|p)\{\d+[.,]*\d*[ce]m\}', '', s, flags=re.S)
        s = re.sub(r'\s*\\begin\{tabular\}\{.*?\}\s*', r'\n\t<table>\n', s, flags=re.S)
        s = re.sub(r'\s*\\end\{tabular\}\s*', r'\n\t</table>\n', s, flags=re.S)
        for t in re.findall(r'<table>\s*(.*?)\n\t</table>', s, flags=re.S):
            content = ''
            for r in re.findall(r'.*?\\\\', t, flags=re.S):
                row = '\t\t<row>\n'
                for cell in r.strip('\\\\').split("&"):
                    m = re.match(r'\s*\\?multicolumn\{(\d+)\}\{[^\}]*\}\{([^\}]*)\}\s*', cell, flags=re.S)
                    if m:
                        x = m.group(2).strip()
                        if x: row += 3*'\t'+'<cell cols="'+m.group(1).strip()+'">'+m.group(2).strip()+'</cell>\n'
                        else: row += 3*'\t'+'<cell cols="'+m.group(1).strip()+'"/>\n'
                    else:
                        c = cell.strip()
                        if c: row += 3*'\t'+'<cell>'+cell.strip()+'</cell>\n'
                        else: row += 3*'\t'+'<cell/>\n'
                row += '\t\t</row>\n'
                content += row
            s = re.sub(re.escape(t), content.rstrip(), s, flags=re.S)
        return s
    def map_tex2tei(self, s):
        s = re.sub(r'\\HBZ\s*\{(zl\d+\s*\-+\s*[^\{\}]*)\}\s*\{(zl(\d+)\s*\-+\s*[^\{\}]*)\}', r'<ref source="\1" target="\2" type="zl">\3</ref>', s, flags=re.S)
        s = re.sub(r'\\Autorname\{([^\{\}]*?)(,?)\}', r'<bibl><author>\1</author></bibl>\2', s, flags=re.S)
        s = re.sub(r'\\HBreg\{([^\{\}]*)\}', r'<note type="entity">\1</note>', s, flags=re.S)
        s = re.sub(r'(<note type="entity">[^<]*\))([^\s][^<]*</note>)', r'\1 \2', s, flags=re.S)
        s = re.sub(r'(<note type="entity">[^<]*,)([^\s][^<]*</note>)', r'\1 \2', s, flags=re.S)
        s = re.sub(r'(<note type="entity">[^<,]*?)\s*,\s*([^\s][^<]*</note>)', r'\1, \2', s, flags=re.S)
        s = re.sub(r'(<note type="entity">[^<]*)\s*,\s*([^\s][^<]*</note>)', r'\1, \2', s, flags=re.S)
        s = re.sub(r'\s*\,[\|\(\)\,\.\s]*(</note>)', r'\1', s, flags=re.S)
        s = re.sub(r'\,\|?\(?(</note>)', r'\1', s, flags=re.S)
        s = re.sub(r'\\Autor[Nn]ame\{([^\{\}]*?)\}', r'<bibl><author>\1</author></bibl>', s, flags=re.S)
        s = re.sub(r'\\Anfze?\{([^\{\}]*?)\}', r'«\1»', s, flags=re.S)
        s = re.sub(r'\\Kirsch', r'<bibl>Kirsch</bibl>', s, flags=re.S)
        s = re.sub(r'\s*\\HBBWnextpage\{([^\{\}]*?)\}', r'<pb type="scan" next="\1"/>', s, flags=re.S)
        s = re.sub(r'\\(SI)', r'<bibl>\1</bibl>', s, flags=re.S)
        s = re.sub(r'\\(hbbw)', r'<bibl>\1</bibl>', s, flags=re.S)
        s = re.sub(r'\\url\{(.*?)\}', r'<ref target="\1">\1</ref>', s, flags=re.S)
        s = re.sub(r'\\VD\{([^\{\}]*)\}\{([^\{\}]*)\}', r'<ref target="\2">\1</ref>', s, flags=re.S)
        s = re.sub(r'\\VD16\s*\\href\{([^\{\}]*)\}\{([^\{\}]*)\}', r'<ref target="\1">\2</ref>', s, flags=re.S)
        s = re.sub(r'\\HBCite\{VD16\}\s*\\href\{([^\{\}]*)\}\{([^\{\}]*)\}', r'<ref target="\1">\2</ref>', s, flags=re.S)
        s = re.sub(r'\\hyperref\[[^\[\]]*\]\{([^\{\}]*)\}', r'\1', s, flags=re.S)
        s = re.sub(r'\\(FNHDW)', r'\1', s, flags=re.S)
        s = re.sub(r'\\textsuperscript\{([^\{\}]*)\}', r'<hi rend="superscript">\1</hi>', s, flags=re.S)
        s = re.sub(r'\\Nr', r'Nr.', s, flags=re.S)
        s = re.sub(r'\\qvAnm\{([^\{\}]*)\}', r'<ref target="\1" type="fn">\1</ref>', s, flags=re.S)
        s = re.sub(r'\\zzl\{([^\{\}]*)\}', r'<ptr target="\1" type="zzl"/>', s, flags=re.S)
        s = re.sub(r'\\zfn\{([^\{\}]*)\}', r'<ptr target="\1" type="zfn"/>', s, flags=re.S)
        s = re.sub(r'\\HBCite\{([^\{\}]*)\}', r'<bibl>\1</bibl>', s, flags=re.S)
        s = re.sub(r'\\href\{([^\{\}]*)\}\{([^\}]*)\}', r'<ref target="\2">\1</ref>', s, flags=re.S)
        s = re.sub(r'\\textit\{([^\{\}]*)\}', r'<hi rend="italic">\1</hi>', s, flags=re.S)
        s = re.sub(r'\\mbox\{([^\{\}]*)\}', r'\1', s, flags=re.S)
        s = re.sub(r'\\ohneAdresse\{([^\{\}]*)\}\{([^\{\}]*)\}', r'<note_address>\1</note_address>\2', s, flags=re.S)
        s = re.sub(r'\\ohneAdresse\{([^\{\}]*)\}', r'<note_address>\1</note_address>', s, flags=re.S)
        s = re.sub(r'\\Unterschrift\{(\[[^\{\}]*\])\}', r'<note_signature>\1</note_signature>', s, flags=re.S)
        s = re.sub(r'\\faAnm\{([^\{\}]*)\}', r'<note xml:id="fn" type="footnote" n="alpha">\1</note>', s, flags=re.S)
        s = re.sub(r'\\Anm\{([^\{\}]*)\}', r'<note xml:id="fn" type="footnote" n="num">\1</note>', s, flags=re.S)
        s = re.sub(r'\\fafn\{([^\{\}]*)\}', r'\1', s, flags=re.S)
        s = re.sub(
            r'\\VonBisAnm\{([^\{\}]*)\}\{([^\{\}]*)\}\{([^\{\}]*)\}\{([^\{\}]*)\}',
            r'<ptr target="\1" type="range_start"/><note xml:id="fn" type="footnote" target="\1" n="alpha">\2</note>\3\4<ptr target="\1-E" type="range_end"/>',
            s, flags=re.S)
        s = re.sub(
            r'\\VonBisAnm\{([^\{\}]*)\}\{([^\{\}]*)\}\{([^\{\}]*)\}([^\{])',
            r'<ptr target="\1" type="range_start"/><note xml:id="fn" type="footnote" target="\1" n="alpha">\2</note>\3<ptr target="\1-E" type="range_end"/>\4',
            s, flags=re.S)
        s = re.sub(r'\\Caput\{([^\{\}]*)\}', r'<span rend="caput">\1</span>', s, flags=re.S)
        s = re.sub(r'\{([aeiou]e)\}', r'\1', s, flags=re.S)
        s = re.sub(r'\\kk\{([^\{\}]*)\}', '', s, flags=re.S)
        s = re.sub(r'\\Unterschrift\{([^\{\}]*)\}', r'<note_signature>Unterschrift:</note_signature> \1', s, flags=re.S)
        s = re.sub(r'\\Adresse\{([^\{\}]*)\}\{([^\{\}]*)\}', r'<note_address>\1</note_address> \2', s, flags=re.S)
        return s
    def map_lists(self, s):
        s = re.sub(r'(\\begin\{(enumerate|itemize)\})\s*\[[^\]]*\]', r'\1', s, flags=re.S)
        s = re.sub(r'\s*(\\begin\{(enumerate|itemize)\})\s*', r'\n\t\t\t\t\t<list>\n', s, flags=re.S)
        s = re.sub(r'\s*(\\end\{(enumerate|itemize)\})\s*', r'\n\t\t\t\t\t</list>\n', s, flags=re.S)
        s = re.sub(r'\s*\\item(\[[^\]]*\]|)\s*', r'\n\t\t\t\t\t\t<item>', s, flags=re.S)
        s = re.sub(r'(\s*<item>)', r'</item>\1', s, flags=re.S)
        s = re.sub(r'(\s*</list>)', r'</item>\1', s, flags=re.S)
        s = re.sub(r'<list></item>', r'<list>', s, flags=re.S)
        return s
    def page_ref_warnings(self, s, f):
        for r in re.findall(r'\\pageref\{[^\}]*\}', s, flags=re.S):
            s = re.sub(re.escape(r), '?', s, flags=re.S)
            if self.show_warnings: print("*Warning, couldn't resolve page reference in", f+' ('+self.matcher.data[re.match(r'(.*)\.xml', f).group(1)]["id_tustep"]+'):', "\\pageref{"+r+"}")
        return s
    def map_attachments(self, s):
        s = re.sub(r'\\Beilage\{([^\{\}]*)\}', r'<note_attachment>\1</note_attachment>', s, flags=re.S)
        return s
    def map_qv_nr(self, s):
        for q in re.findall(r'(\\qvNr\{(\d+)\})', s, flags=re.S):
            s = re.sub(re.escape(q[0]), r'<ref target="' + q[1] + r'">' + q[1] + '</ref>', s, flags=re.S)
        return s
    def map_recursively(self, s):
        s_new = ''
        while s_new != s:
            s_new = s
            s = self.normalize(s)
            s = self.map_tex2tei(s)
        return s
    def map_letter(self, s, f):
        m_letter = re.match(r'.*?(\\begin\{brieftext\}(.*?)\\end\{brieftext\}).*', s, flags=re.S)
        if not m_letter:
            if self.show_warnings: print("*Warning, invalid letter (missing text):", f+' ('+self.matcher.data[re.match(r'(.*)\.xml', f).group(1)]["id_tustep"]+')')
        else:
            s = re.sub(r'\\begin\{brieftext\}\s*(.*?)\s*\\end\{brieftext\}', r'\t<text>\n\t\t<body>\n\1\n\t\t</body>\n\t</text>\n', s, flags=re.S)
            s = re.sub(
                r'\\div\w*\{\s*([^\{\}]*)\s*\}',
                r'\t\t\t<div xml:id="div" corresp="regest">\n\t\t\t\t<p>\n\t\t\t\t\t<s>\1</s>\n\t\t\t\t</p>\n\t\t\t</div>',
                s, flags=re.S)
        return s
    def insert_notes(self, s):
        s_new = ''
        while s_new != s:
            s_new = s
            for t in ["signature", "address", "attachment"]:
                s = re.sub(
                    r'(\s*</div>)\s*<note_'+t+'>(.*?)</note_'+t+'>\s*([^<]*)\s*',
                    r'\n\t\t\t\t<p>\n\t\t\t\t\t<note type="'+t+r'">\2</note>\n\t\t\t\t\t<s>\3</s>\n\t\t\t\t</p>\1', s, flags=re.S
                )
            s = re.sub(r'\s*(</s>)', r'\1', s, flags=re.S)
            s = re.sub(r'\s*<s>\s*</s>', '', s, flags=re.S)
            s = re.sub(r'(</div>)<note type="entity">[^<]*</note>(\s*</body>)', r'\1\2', s, flags=re.S)
            s = re.sub(r'<note type="entity">[^<]*</note>(\s*</body>)', r'\1', s, flags=re.S)
            s = re.sub(r'(</s>\s*</p>\s*</div>)([^\n]*)(\s*</body>)', r'\2\1\3', s, flags=re.S)
        return s
    def insert_lists(self, s):
        lists_, i = dict(), 0
        for l in re.findall(r'(\s*<list.*?</list>)', s, flags=re.S):
            s = re.sub(re.escape(l), '@@@'+str(i), s, flags=re.S)
            lists_['@@@'+str(i)] = l
            i += 1
        for j in range(0, i):
            s = re.sub(r'(@@@'+str(j)+')(</s>\s*\n)', r'\2\1', s, flags=re.S)
            s = re.sub(r'(</s>\n)(\s*</p>\s*</div>\s*)(@@@'+str(j)+')', r'\1\3\n\2', s, flags=re.S)
        for j in range(0, i): s = re.sub(r'@@@'+str(j), lists_['@@@'+str(j)], s, flags=re.S)
        s = re.sub(r'\s*\n\s*\n', r'\n', s, flags=re.S)
        s = re.sub(r'\s*</p>', r'\n\t\t\t\t</p>', s, flags=re.S)
        s = re.sub(r'<item>', r'<item><s>', s, flags=re.S)
        s = re.sub(r'</item>', r'</s></item>', s, flags=re.S)
        return s
    def insert_tables(self, s):
        lists_, i = dict(), 0
        for l in re.findall(r'(\s*<table.*?</table>\s*)', s, flags=re.S):
            s = re.sub(re.escape(l), ' @@@'+str(i)+' ', s, flags=re.S)
            lists_['@@@'+str(i)] = l
            i += 1
        for j in range(0, i):
            s = re.sub(r'(<s>[^\n]*)\s*(@@@'+str(j)+')\s*([^\n]*</s>)', r'\1 \3\n\2\n', s, flags=re.S)
        for j in range(0, i): s = re.sub(r'@@@'+str(j), lists_['@@@'+str(j)], s, flags=re.S)
        s = re.sub(r'\s*\n\s*\n', r'\n', s, flags=re.S)
        s = re.sub(r'\s*(</?table)', r'\n\t\t\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*(</?row)', r'\n\t\t\t\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*(<cell)', r'\n\t\t\t\t\t\t\t\1', s, flags=re.S)
        return s
    def insert_seqs(self, s):
        s = re.sub(r'(<s>[^\n]*)\n(<span)', r'\1 \2', s, flags=re.S)
        m = re.match(r'.*?(([^\n]*</s>)(\s*</p>\s*</div>\s*)(<span[^\n]*)\n)', s, flags=re.S)
        while m:
            s = re.sub(re.escape(m.group(1)), m.group(2)+'\n\t\t\t\t\t<s>'+m.group(4)+'</s>'+m.group(3), s, flags=re.S)
            m = re.match(r'.*?(([^\n]*</s>)(\s*</p>\s*</div>\s*)(<span[^\n]*)\n)', s, flags=re.S)
        return s
    def insert_blanks(self, s):
        s = re.sub(r'(<s><pb .*?/>)\s+', r'\1', s, flags=re.S)
        for n in re.findall(r'<note type="entity">.*?</note>', s, flags=re.S):
            s = re.sub(re.escape(n), re.sub(r'([a-z])([A-Z])', r'\1 \2', n, flags=re.S), s, flags=re.S)
        return s
    def extract_notes(self, t, type):
        t = re.sub(r'<note type="entity".*?</note>', '', t, flags=re.S)
        for fn in re.findall(r'<note.*?</note>', t, flags=re.S): self.footnotes.append([type, fn])
        t = re.sub(r'<note.*?</note>', '', t, flags=re.S)
        return t
    def get_title(self, s, f):
        t = ''
        m_title = re.match(r'.*\\Korrespondenten(\[[^\{]*?\}|)\{([^\n]*?)\}.*', s, flags=re.S)
        m_date = re.match(r'.*\\HBBWOrtDatum(\[[^\{]*?\]|)\{([^\n]*?)\}.*', s, flags=re.S)
        title = m_title.group(2) if m_title else ''
        date = m_date.group(2) if m_date else ''
        if title and date: t = ', '.join([title, date])
        elif title: t = title
        elif date: t = date
        t = self.extract_notes(t, "title")
        return t
    def get_signature(self, s, f):
        entries = []
        s = re.sub(r'\s*(\\HBBWSignatur)', r'\n\1', s, flags=re.S)
        for m in re.findall(r'\\HBBWSignatur\{([^\n]*)\}', s, flags=re.S):
            type, subtype, id_archive, signature = 'Brief', '', '', ''
            if m:
                t = self.extract_notes(m, "signature")
                t = re.sub(r'[\[\]]+', '', t, flags=re.S)
                # type
                m_attachment = re.match(r'((Beilage)[^:]*:\s*).*', t, flags=re.S)
                if m_attachment:
                    type = "Beilage"
                    t = re.sub(re.escape(m_attachment.group(1)), '', t, flags=re.S)
                # subtype
                m_subtype = re.match(r'((Autograph|Original|Kopie|Abschrift)\s*[^:]*:\s*)', t, flags=re.S)
                if m_subtype:
                    subtype = m_subtype.group(2)
                    t = re.sub(re.escape(m_subtype.group(1)), '', t, flags=re.S)
                # archive
                m_archive = re.match(r'([^,]*),.*', t, flags=re.S)
                if m_archive and m_archive.group(1) in self.matcher.archive2id:
                    id_archive = self.matcher.archive2id[m_archive.group(1)]
                    t = re.sub(r'^[^,]*,\s*', '', t, flags=re.S)
                signature = re.sub('<[^>]*>', '', t.strip(';'), flags=re.S)
                entries.append([type, subtype, id_archive, signature])
        return entries
    def get_placedate(self, s):
        mpd = re.match(r'.*\\HBBWOrtDatum\{(.*?)\}.*', s, flags=re.S)
        if mpd:
            t = self.extract_notes(mpd.group(1), "sender")
            t = re.sub(r'[\[\]]', '', t, flags=re.S).split(', ')
            return ', '.join(t[:1]), ', '.join(t[1:])
        else: return '', ''
    def get_key_words_from_corpus(self, f):
        path = os.path.join(self.root_letters, f)
        if os.path.exists(path):
            with open(path) as fi: s = fi.read()
            m = re.match(r'.*(<encodingDesc.*?</encodingDesc>).*', s, flags=re.S)
            if m: return m.group(1)
        return ''
    def get_element_from_corpus(self, f, name):
        path = os.path.join(self.root_letters, f)
        if os.path.exists(path):
            with open(path) as fi: s = fi.read()
            m = re.match(r'.*(<'+name+'>.*</'+name+'>).*', s, flags=re.S)
            if m: return m.group(1)
        return ''
    def filter_context(self, context):
        for c in re.findall(r'[ \t]*<ref type=.*?/>[ \t]*\n', context, flags=re.S):
            if not re.match(r'.*type="(child|parent)".*', c, flags=re.S):
                context = re.sub(re.escape(c), '', context, flags=re.S)
        if re.match(r'.*<correspContext>\s*</correspContext>.*', context, flags=re.S): return ''
        return context
    def get_regest(self, s):
        t = ''
        m_reg = re.match(r'.*?\\begin\{regest\}\s*(.*?)\s*\\end\{regest\}.*', s, flags=re.S)
        if m_reg:
            t = m_reg.group(1)
            t = re.sub(r'\\zupar[AB]\{([^\n]*)\}', 7*'\t'+r'<p xml:id="regest">\1</p>', t, flags=re.S)
        return (t+'\n') if t else ''
    def get_printed(self, s):
        prints = []
        s = re.sub(r'\s*(\\HBBWDruck)', r'\n\1', s, flags=re.S)
        s = re.sub(r'\\HBBWDruck\{Ungedruckt\}\s*', '', s, flags=re.S)
        for p_ in re.findall(r'\\HBBWDruck{([^\n]*)\}', s, flags=re.S):
            p = self.extract_notes(p_, "printed")
            p = re.sub(r'[\[\]]', '', p, flags=re.S)
            p = re.sub(r'</?bibl>', '', p, flags=re.S)
            m = re.match(r'\s*(.*?)\s*:\s*(.*)\s*', p, flags=re.S)
            if m: prints.append([re.sub(r'\s+', '__', m.group(1), flags=re.S), m.group(2)])
            else: prints.append(['', p])
        return prints
    def insert_meta_fns(self, s):
        footnotes, passed = '', []
        for fn in sorted(self.footnotes, key=lambda x: x[0], reverse=True):
            if fn[1] not in passed:
                footnotes += 2*'\t'+re.sub(r'(type="footnote")', r'\1 subtype="'+fn[0]+'"', fn[1], flags=re.S)+'\n'
                passed.append(fn[1])
        if footnotes: s = re.sub(r'(<text>\n)', r'\1'+footnotes, s, flags=re.S)
        return s
    def set_numbers(self, s):
        m, n = re.match(r'(.*?<p xml:id="regest)(">.*)', s, flags=re.S), 1
        while m: # regests
            s = re.sub(re.escape(m.group(1)), m.group(1)+str(n), s, flags=re.S)
            m = re.match(r'(.*?<p xml:id="regest)(">.*)', s, flags=re.S)
            n += 1
        m, n = re.match(r'(.*?<note xml:id="fn)(" type="footnote"[^>]*n="alpha">.*)', s, flags=re.S), 1
        while m: # footnotes: alpha
            s = re.sub(re.escape(m.group(1)), m.group(1)+self.num2alpha(n), s, flags=re.S)
            m = re.match(r'(.*?<note xml:id="fn)" type="footnote"[^>]*n="alpha">.*', s, flags=re.S)
            n += 1
        m, n = re.match(r'(.*?<note xml:id="fn)(" type="footnote"[^>]*n="num">.*)', s, flags=re.S), 1
        while m: # footnotes: num
            s = re.sub(re.escape(m.group(1)), m.group(1)+str(n), s, flags=re.S)
            m = re.match(r'(.*?<note xml:id="fn)" type="footnote"[^>]*n="num">.*', s, flags=re.S)
            n += 1
        m, n = re.match(r'(.*?<div xml:id="div)(" corresp="regest)(">).*', s, flags=re.S), 1
        while m: # divs
            s = re.sub(re.escape(m.group(1))+re.escape(m.group(2)), m.group(1)+str(n)+m.group(2)+str(n), s, flags=re.S)
            m = re.match(r'(.*?<div xml:id="div)(" corresp="regest)(">).*', s, flags=re.S)
            n += 1
        s = re.sub(r'(<note xml:id="fn)(\d+)(" type="footnote"[^>]* n=")num(">)', r'\1\2\3\2\4', s, flags=re.S)
        s = re.sub(r'(<note xml:id="fn)([^"]*)(" type="footnote"[^>]* n=")alpha(">)', r'\1\2\3\2\4', s, flags=re.S)
        return s
    def num2alpha(self, n):
        result = ""
        while n > 0:
            n -= 1
            result = chr(ord('a') + (n % 26)) + result
            n //= 26
        return result
    def cleanup(self, s):
        s = re.sub(r'\\HBBWBriefbeginn\{\d+\}\s*', '', s, flags=re.S)
        s = re.sub(r'\\begin\{regest\}.*?\\end\{regest\}\s*', '', s, flags=re.S)
        s = re.sub(r'(<s>)\{(<note)', r'\1\2', s, flags=re.S)
        s = re.sub(r'(</note>)\}(</s)', r'\1\2', s, flags=re.S)
        s = re.sub(r'\s*\\begin\{HBBWBriefkopf\}.*?\\end\{HBBWBriefkopf\}\s*', '\n\t', s, flags=re.S)
        s = re.sub(r'(<surface>)\s*(<graphic)', r'\1\2', s, flags=re.S)
        s = re.sub(r'(</graphic>)\s*(</surface>)', r'\1\2', s, flags=re.S)
        s = re.sub(r'(</div>)[ \t]+', r'\1', s, flags=re.S)
        s = re.sub(r'&', r'&amp;', s, flags=re.S)
        s = re.sub(r'\n\s*\%[^\n]*', '', s, flags=re.S)
        s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)
        return s.strip()
    def fix_structral_issues(self, s):
        s_old = ''
        while s_old != s:
            s_old = s
            s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)
            for n in re.findall(r'((<pb[^>]*next=")([^"]*)("))', s, flags=re.S):
                s = re.sub(re.escape(n[0]), n[1]+re.sub(r'\s', '__', n[2])+n[3], s, flags=re.S)
            s = re.sub(r'(<ref)[^>]*(>https://)', r'\1\2', s, flags=re.S)
            s = re.sub(r'(</s>\s*</p>\s*</div>)(<note[^\n*]*)', r'\2\1', s, flags=re.S)
            s = re.sub(r'(</s>\s*</p>\s*</div>)(<ptr[^>]*>[^\n]*)', r'\2\1', s, flags=re.S)
            for e in ["note_signature", "note_address"]:
                s = re.sub(r'([ \t]*</div>)\n(<'+e+'.*?</'+e+'>)\s*([^\n]+)', r'\t\t\t\t<p>\n\t\t\t\t\t\2\n\t\t\t\t\t<s>\3</s>\n\t\t\t\t</p>\n\1', s, flags=re.S)
            s = re.sub(r'(\s*</p>\s*</div>)([^<\s*][^\n]*)', r'\t\t\t\t\t<s>\2</s>\1', s, flags=re.S)
            for e in ["note_signature", "note_address"]:
                for x in re.findall(r'<s>.*?</s>', s, flags=re.S):
                    x_new = re.sub(r'(.*?)\s*(<'+e+'>.*?</'+e+'>)\s*(.*)', r'\1</s>\n\t\t\t\t\t\2\n\t\t\t\t\t<s>\3', x, flags=re.S)
                    if x_new != x: s = re.sub(re.escape(x), x_new, s, flags=re.S)
            s = re.sub(r'(</teiHeader>)\s*<note[^>]*>[^<]*</note>\s*(</TEI>)', r'\1\n\2', s, flags=re.S)
            s = re.sub(r'(</s>\s*</p>\s*</div>\s*)(<note type="entity">[^<]*</note>)', r'\2\1', s, flags=re.S)
            s = re.sub(r'(<note_attachment>.*?</note_attachment>)(\s*<div[^>]*>\s*<p>\n)', r'\2\t\t\t\t\t\1\n', s, flags=re.S)
            s = re.sub(r'([ \t]*</p>\s*</div>)\s*(<ptr[^\n]*)', r'\t\t\t\t\t<s>\2</s>\n\1', s, flags=re.S)
        t = r"\t<text>\n\t\t<body>\n\t\t\t<div>\n\t\t\t\t<p>\n\t\t\t\t\t<bibl>[Keine Transkription verfügbar.]</bibl>\n\t\t\t\t</p>\n\t\t\t</div>\n\t\t</body>\n\t</text>\n"
        s = re.sub(r'(</teiHeader>\s*|</facsimile>\s*)(</TEI>)', r'\1'+t+r'\2', s, flags=re.S)
        s = re.sub(r'[ \t]*<s>\s*</s>\n', '', s, flags=re.S)
        s = re.sub(r'>\s*[\{\}]+\s*<', '><', s, flags=re.S)
        s = re.sub(r'\s*(<div)', r'\n\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s+(</note>)', r'\1', s, flags=re.S)
        # facsimile
        s = re.sub(r'\s*(</?surface)', r'\n\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*(</?graphic)', r'\n\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*(<desc)', r'\n\t\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*(</desc)', r'\1', s, flags=re.S)
        return s
    def rename_notes(self, s):
        for t in ["address", "attachment", "signature"]:
            s = re.sub(r'(<note)_'+t+'>(.*?)</note_'+t+'>', r'\1 type="'+t+r'">\2</note>', s, flags=re.S)
        return s
