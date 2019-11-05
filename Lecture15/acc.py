#!/usr/bin/python3
import re
q1 = []
q2 = []
q3 = []
q4 = []
q5 = []
q6 = []
q7 = []
q8 = []
q9 = []
accessions = ['xkn59438', 'yhdck2', 'eihd39d9', 'chdsye847', 'hedle3455', 'xjhd53e', '45da', 'de37dp']
for accession in accessions:
	if re.search(r'5',accession):
		q1.append(accession)
	if re.search(r'[de]',accession):
		q2.append(accession)
	if re.search(r'd.*e',accession):
		q3.append(accession)
	if re.search(r'd.e',accession):
		q4.append(accession)
	if re.search(r'd',accession) and re.search(r'e',accession):
		q5.append(accession)
	if re.search(r'^[xy]',accession):
		q6.append(accession)
	if re.search(r'^[xy].*e$',accession):
		q7.append(accession)
	if len(re.findall(r'[0-9]',accession)) >= 3:
		q8.append(accession)
	if re.search(r'd[arp]$',accession):
		q9.append(accession)
print("Q1: ",q1,"\nQ2: ",q2,"\nQ3: ",q3,"\nQ4: ",q4,"\nQ5: ",q5,"\nQ6: ",q6,"\nQ7: ",q7,"\nQ8: ",q8,"\nQ9: ",q9)
