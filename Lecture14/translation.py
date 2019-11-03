#!/usr/bin/python3
gencode = {
'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}

dna = input("DNA sequence:\n")
length = len(dna)
#def translate(start):
#	protein = ""
#	for start in list(range(beginning,length,3)):
#		code = dna[start:start+3].upper()
#	aa = gencode.get(code)
#	if type(aa) == str:
#		protein = protein+aa
#	return protein
#for beginning in [0,1,2]:
#	for start in list(range(beginning,length,3)):
#		code = dna[start:start+3].upper()
#		protein = translate(start)
#		aa = gencode.get(code)
#		if type(aa) == str:
#			protein = protein+aa
#	print(protein)
def translate(dna):
	for beginning in [0,1,2]:
		protein = ""
		for start in list(range(beginning,length,3)):
			code = dna[start:start+3].upper()
			aa = gencode.get(code)
			if type(aa) == str:
				protein = protein + aa
		print(protein)
translate(dna)
