# This script marks all sentences with regards
#   with the attribute  ana="salute"
# and it also marks the sentences with "vale" etc. 
#   with the attribute  ana="farewell"
# and it inserts the XML version line as 1st line into the output
# and it removes spurious blanks in "empty" XML elements
# by MVolk

import sys  ## necessary for command line arguments
import xml.etree.ElementTree as ET ## for handling XML files
import re
import os   ## for operating systems access
import glob ## for filename pattern matching

# Briefe in TEI Corpus
path = './data/letters'
# path = '.'

# Define the namespace - is this necessary ???
namespace = {"tei": "http://www.tei-c.org/ns/1.0"}

# here we list sentences, that should be marked as "regards", 
#   even though they do not contain a trigger word.
# the format is: letter_id, sentence_id (as a tuple)
special_sent_set = {('5333','11'), # DE sent without verb
  ('8971','12'), # LA sent with backref
  ('12360','62'), # DE sent with bracket in verb
  ('12536','33')} # DE sent with bracket in verb: gruͤtz[en]d

##################################################
## collect all the XML filenames from the folder specified in path
# file_list = glob.glob(os.path.join(path, '8971.xml'))
file_list = glob.glob(os.path.join(path, '*.xml'))

# counters for Latin and ENH German regards sentences
reg_sentence_LA_counter = 0
reg_sentence_ENHG_counter = 0
# ... and farewell sentences
farewell_sentence_LA_counter = 0

# for every file
for xml_path_file in sorted(file_list):

	# get file name without path
	my_match = re.search('(\d+)\.xml$', xml_path_file)
	xml_file_name = my_match.group()
	print("Working on file", xml_file_name)
	letter_id = my_match.group(1)
	
	# parse the XML file and store the XML tree
	my_tree = ET.parse(xml_path_file)
#	ET.dump(my_tree)

	# initialise the flag
	marked_sent_flag = False

	# for each <s> element 
#	for sentence in my_tree.iter("s"):
	for sentence in my_tree.iter("{http://www.tei-c.org/ns/1.0}s"):

		# exclude the 1st and 2nd sentence of each letter
		if (sentence.attrib['n'] in {'1', '2'}):
			continue
		# special treatment for sentences in the "special sentences set"
		elif ((letter_id, sentence.attrib['n']) in special_sent_set):
#			print('Sentence', sentence.attrib['n'], 'is a regards sent')
			## add the attribute 'ana' with value 'salute'
			sentence.attrib['ana'] = 'salute'
			reg_sentence_LA_counter += 1
			marked_sent_flag = True
			continue

		# initialize the variable which is used to collect the text of the sentence
		sent_wo_tags = ''
	
		# collect the complete sentence text (skipping all tags)
		if (sentence.text != None):
			sent_wo_tags = sentence.text
		for child in sentence:
			if (child.tag == '{http://www.tei-c.org/ns/1.0}persName'):
				# add a tag as placeholder - only important for the screen output
				sent_wo_tags += '<persN>'
			elif (child.tag == '{http://www.tei-c.org/ns/1.0}placeName'):
				sent_wo_tags += '<placeN>'
			
			# for code-switching sentences
			elif (child.tag == '{http://www.tei-c.org/ns/1.0}foreign'):
				# include the foreign language text into the sentence
				if (child.text != None):
					if (child.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == 'la'):
	#					print('Test', child.attrib)
						sent_wo_tags += '<la>' + child.text + '</la>'
					elif (child.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == 'de'):
						sent_wo_tags += '<de>' + child.text + '</de>'

			if (child.tail != None):
				sent_wo_tags += child.tail

		# build the regular expression to identify regards sentences in Latin
		reg_ex_LA = '(Salut(a|at|o|em|es)[\s,;]|'
		# with brackets _[]_ !
		reg_ex_LA += 'Salut\[a\]|Saluta\[bis\]|Saluta\[n\]t|Salut\[em\]|'
		reg_ex_LA += 'Saluta(bis|bitis|mus|nt|re|ri|runt|ta|te|tiones|to|tum|tus|vi)|'
		reg_ex_LA += ' (re)?salut(a|at|o|em|es)[\s\.,;]|'
		# I dropped 'salutaris' which is more 'saving' rather than 'greeting'
		reg_ex_LA += ' (re)?saluta(bis|bit(is)?|mus|ndi|nt|ret?|ri|runt|te|tib|tis|tos?|tum|tus|vi)[\s\.,;]|'
		reg_ex_LA += 'Salv(eat|eant|um|us|os)|[Ss]alvere|'
		# Not really regards sentences, rather safety sentences (similar to blessing sentences)
		# roughly 135 hits !?
#		reg_ex_LA += '[Ss]alva sit|[Ss]alvi (sint|sitis)|Salvi sunt|' 
		reg_ex_LA += 'Resaluta|'
		reg_ex_LA += 'Commenda me|'
		reg_ex_LA += ' commenda me| me commenda| me commendar[ei]\b|'
		reg_ex_LA += '(diligenter|diligentissime|accuratissime) commenda)'

		# for Latin
		if (re.search(reg_ex_LA, sent_wo_tags)):
			print(sentence.attrib['n'], sent_wo_tags)
			## add the attribute 'ana' with value 'salute'
			sentence.attrib['ana'] = 'salute'
			reg_sentence_LA_counter += 1
			marked_sent_flag = True
			
		# for ENH-DE
			# exclude: 'ein grusenlich ellend', 'Ein gruselich persecution', 'ain grußelich geschrey', 'grusamlich verfolgt'
			# exclude: 'von grusamem wüten'
			# exclude: 'Grüschii' (unmarkierter persName)
			# include: Grüetzent, Groetzt, Gruuͤßend
#		elif (re.search('(Gr(uͦ|uͤ|ü)[et]?[ßsz]|Gru[eo]?t?[ßsz]|Grie[szß]+(en)?[t]|Grie[szß]+en |Gritzen|Groiz| gru[eo]?t?[ßsz]| gr(uͦ|uͤ|ü|ys|ie|ouͤ|ye|üi|üe|is)t?[ßsz])', sent_wo_tags)) and not (re.search('(gr[uü]\w+lich|gr[uü]sam|Grüschii)', sent_wo_tags)):
		elif (re.search('(Gru?(uͦ|uͤ|ü)e?t?[ßsz]|Gru[eo]?t?[ßsz]|Grie[szß]+(en)?[t]|Grie[szß]+en |[Gg]ritzen|Groiz|Groetzt| gru[eo]?t?[ßsz]| gr(uͦ|uͤ|ü|ys|ie|ouͤ|ye|üi|üe|is)t?[ßsz]|Begrützen)', sent_wo_tags)) and not (re.search('(gr[uü]\w+lich|gr[uü]sam|Grüschii)', sent_wo_tags)):
			print(sentence.attrib['n'], sent_wo_tags)
			## add the attribute 'ana' with value 'salute'
			sentence.attrib['ana'] = 'salute'
			reg_sentence_ENHG_counter += 1
			marked_sent_flag = True

		# for Latin _Vale_ sentences (= farewell sentences)
		# if the farewell sentence has been marked as regards sentence, we do not mark it.
		elif (re.search('(Vale(te)?[\s\.,;]| vale(te)?[\s\.,;])', sent_wo_tags)):
			print(sentence.attrib['n'], sent_wo_tags)
			## add the attribute 'ana' with value 'farewell'
			sentence.attrib['ana'] = 'farewell'
			farewell_sentence_LA_counter += 1
			marked_sent_flag = True


	# if at least one regards sentence or farewell sentence was found and marked
	#   then write the outfile
	if (marked_sent_flag == True):
		# set the empty string as namespace
		ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

	#	out_path = '/Users/martinvolk/Documents/Zurich/Uni_Projects/2020_Bullinger_Briefe/Regards_Gruss_Sentences/marked_letters_temp'
		out_path = './data/letters/'
		
		# Write the XML tree to the file
		# This omits the XML version line (= first line of the input file) :-{
#		with open(out_path + xml_file_name, 'wb') as f:
#			my_tree.write(f, encoding='utf-8')

		##### in order to reinsert the XML version line and to remove spurious blanks
		#####    convert the XML tree into a string
		# Get the root element
		my_root = my_tree.getroot()
		# convert the XML ElementTree into a string
		xml_string = ET.tostring(my_root, encoding='unicode')
		# does not work properly with utf-8 !?
#		xml_string = ET.tostring(my_root, encoding='utf-8')
	
		# insert the XML version line at the beginning of the file
		xml_string = re.sub(r'(<TEI )', r'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\1', xml_string, flags=re.S) # re-add
		# remove spurious blanks before the end of "empty" XML elements
		xml_string = re.sub(r'\s*/>', r'/>', xml_string, flags=re.S) # rm blanks
#		print(xml_string)
		
		# Open the output file in write mode
		with open(out_path + xml_file_name, "w") as file:
			# Write the XML string to the output file
			file.write(xml_string)
    
print('\nI worked on', len(file_list), 'files.')
print('I marked', reg_sentence_LA_counter, 'Latin regards sentences.')
print('I marked', reg_sentence_ENHG_counter, 'ENH German regards sentences.')
print('I marked', farewell_sentence_LA_counter, 'Latin farewell sentences.')
