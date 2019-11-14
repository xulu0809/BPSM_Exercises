#!/usr/bin/python3
import os,sys
import subprocess
# Get information from user's input
# use AND to search for more items?
# capitalize...
protein_name = input("Please enter the protein name: ")
organism = input("Please enter the organism: ")
#protein_name = "glucose-6-phosphatase"
#organism = "aves"

#need delete space?
file_name = protein_name+"_"+organism
# run in unix command line; bytes -> string
def shell_out(command):
	output = subprocess.check_output(command,shell=True).decode()
	return output

#could be in a function?
cmd_search = "esearch -db protein -query '"+protein_name+"[PROT] AND "+organism+"[ORGN] NOT partial NOT predicted'"
info = shell_out(cmd_search).split()
count = (info[4])[7:-8]

if count == "0":
	print("No hits. Please check the spelling of protein and organism.")
# how to exit?
	exit()

print("There are "+count+" results found.")
cmd_fetch = cmd_search+" | efetch -db protein -format fasta >"+file_name+".fa"
#sequence = shell_out(cmd_fetch)
os.system(cmd_fetch)
raw_fasta = open(file_name+".fa")
sequences = {} #dictionary for raw sequence fasta
list_species = []
for line in raw_fasta:
	if line.startswith(">"):
		name = line.split()[0].replace(">","")
		species = line[line.find("[")+1:line.find("]")]
		list_species.append(species)
		sequences[name] = line
	else:
		sequences[name] += line.replace("\n","")

all_species = set(list_species)
#sort? how many for each species?


print("There are "+str(len(all_species))+" species:\n"+", ".join(all_species))

# continue or not?
def ifcontinue():
	y_n = input("Do you want to continue? (y/n): ")
	if y_n.upper() == "N":
		print("Quiting...")
		exit()
	elif y_n.upper() != "Y":
		print("Sorry, you can only use 'y' or 'no'.")
		ifcontinue()
ifcontinue()

cmd_clus = "clustalo -i "+file_name+".fa -o "+file_name+"_clus.fa --outfmt fasta -v --threads=256 --force"

#5 -> 250
if len(sequences) > 20:
	cmd_cons = "cons -sequence "+file_name+"_clus.fa -outseq "+file_name+"_cons.fa"
	cmd_blastdb = "makeblastdb -in "+file_name+".fa -dbtype prot -out "+file_name
	cmd_blastp = "blastp -db "+file_name+" -query "+file_name+"_cons.fa -outfmt 7 > blastp.out"
	#subprocess.call(cmd_clus+";"+cmd_cons+";"+cmd_blastdb+";"+cmd_blastp,shell=True)
	os.system(cmd_clus)
	os.system(cmd_cons)
	os.system(cmd_blastdb)
	os.system(cmd_blastp)
	#blastout = shell_out(cmd_blastp)
	blastp = open("blastp.out")
	#blastp.write(blastout)
	#blastp.close()
	acc250 = []
	count = 0
	for line in blastp:
		if line.startswith("#") == False and count < 20:
			count += 1
			acc250.append(line.split()[1])
	sequences250 = {}
	file250 = open("seq250.fa","a")
	for acc in acc250:
		seq_in250 = sequences.get(acc)
		sequences250[acc] = seq_in250
		file250.write(seq_in250.replace(">","\n>"))
	file250.close()
	#delete the raw sequence? rename the 250 sequences
	os.remove(file_name+".fa")
	os.rename("seq250.fa",file_name+".fa")
	os.system(cmd_clus)
os.system("plotcon -winsize 4 -graph svg -gsubtitle '"+protein_name+" in "+organism+"' -goutfile "+file_name+" "+file_name+"_clus.fa;display "+file_name+".svg")


