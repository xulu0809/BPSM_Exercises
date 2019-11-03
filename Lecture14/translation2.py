#!/usr/bin/python3
def translate_dna(dna,frame=1):
	dna = dna.upper()
	if frame not in [-3,-2,-1,1,2,3]:
		print("Not a valid translation frame,\nHas to be one of these: -3, -2, -1, 1, 2, 3.\nExiting...")
		return
	if frame in [-3,-2,-1]:
		print("Need to make the reverse complement to do the reverse strand translation...")
		c_dna = dna.replace("G","c").replace("A","t").replace("T","a").replace("C","g").upper()
		rc_dna = c_dna[::-1]
		print("Was\n",dna,"\nnow\n",rc_dna)
		dna = rc_dna
	framestart = abs(frame) - 1
	last_codon_start = len(dna) - 2
	protein = ""
	for start in list(range(framestart,last_codon_start,3)):
		codon = dna[start:start+3]
		aa = gencode.get(codon,"X")
		protein = protein + aa
	#return protein
	print(protein)
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

translate_dna("ATGTTCGGT",-1)
