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
'''def shell_out(command):
	output = subprocess.check_output(command,shell=True).decode()
	return output
'''
#could be in a function?
cmd_search = "esearch -db protein -query '"+protein_name+"[PROT] AND "+organism+"[ORGN] NOT partial NOT predicted'"
cmd_getcount = "xtract -pattern ENTREZ_DIRECT -element Count"
#info = shell_out(cmd_search).split()
count = subprocess.check_output(cmd_search+" | "+cmd_getcount,shell=True).decode().strip()
#count = (info[4])[7:-8]

if count == "0":
	print("No hits. Please check the spelling of protein and organism.")
# how to exit?
	exit()

print("There are "+count+" results found.")

def ifcontinue():
        y_n = input("Do you want to continue? (y/n): ")
        if y_n.upper() == "N":
                print("Quiting...")
                exit()
        elif y_n.upper() != "Y":
                print("Sorry, you can only use 'y' or 'no'.")
                ifcontinue()
ifcontinue()
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


ifcontinue()

cmd_clus = "clustalo -i "+file_name+".fa -o "+file_name+"_clus.fa --outfmt fasta -v --threads=32 --force"
cmd_info = "infoalign -sequence "+file_name+"_clus.fa -outfile "+file_name+".info -nousa"
os.system(cmd_clus)
os.system(cmd_info)
print("Some information about the clustalo result is saved in the file "+file_name+".info.\nShowing the first 10 lines for you.\n\n")
#get the most consensus sequence, least difference
aligninfo = open(file_name+".info")
count = 0
diffcount = 100000
for line in aligninfo:
	count += 1
	if count<=10:
		print(line)
	if line.startswith("#") == False and int(line.split()[7]) < diffcount:
		diffcount = int(line.split()[7])
		name = line.split()[0]


def seqdic(seqfilename,dicname):
	
	seqfile = open(seqfilename)
	for line in seqfile:
		if line.startswith(">"):
			seqname = line.split()[0].replace(">","")
			dicname[seqname] = line
		else:
			dicname[seqname] += line.replace("\n","")
clusseqs = {}
seqdic(file_name+"_clus.fa",clusseqs)
conseq = clusseqs.get(name)
print(conseq)

#5 -> 250
if len(sequences) > 20:
#	cmd_cons = "cons -sequence "+file_name+"_clus.fa -outseq "+file_name+"_cons.fa"
	cmd_blastdb = "makeblastdb -in "+file_name+".fa -dbtype prot -out "+file_name
	cmd_blastp = "blastp -db "+file_name+" -query "+file_name+"_cons.fa -outfmt 7 > blastp.out"
	#subprocess.call(cmd_clus+";"+cmd_cons+";"+cmd_blastdb+";"+cmd_blastp,shell=True)
#	os.system(cmd_clus)
#	os.system(cmd_cons)
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
#for seq in sequences250.values():
#	os.system("wget -O out.fa 'https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq="+seq+"&output=fasta';grep '^>' out.fa >> res.fa")
motifs = []
for seq in sequences250.values():
	temfile = open("temfile.fa","w")
	temfile.write(seq)
	temfile.close()
	os.system("patmatmotifs -sequence temfile.fa -outfile site.tem -noprune > nouseout")
	site = open("site.tem")
#	siteout = open("site.out","a")
	for line in site:
		if line.startswith("Motif"):
#			siteout.write(line)
			motifs.append(line.split(" = ")[1].rstrip())
print("The known motifs are: "+",".join(set(motifs)))
#siteout.close()

