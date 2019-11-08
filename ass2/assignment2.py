#!/usr/bin/python3
import os
import subprocess
# capitalize...
#protein_name = input("Please enter the protein name: ")
#organism = input("Please enter the organism: ")

protein_name = "glucose-6-phosphatase"
organism = "aves".capitalize()

#need delete space?
file_name = protein_name+"_"+organism
# run in unix command line; bytes -> string
def shell_out(command):
	output = subprocess.check_output(command,shell=True).decode()
	return output
'''
#could be in a function?
cmd_search = "esearch -db protein -query '"+protein_name+"[PROT] AND "+organism+"[ORGN] NOT partial NOT predicted'"
info = shell_out(cmd_search).split()
count = (info[4])[7:-8]

if count == "0":
	print("No hits. Please check the spelling of protein and organism.")
# how to exit?
	exit()

print("There are "+count+" results found.")
cmd_fetch = cmd_search+" | efetch -db protein -format fasta"
sequence = shell_out(cmd_fetch)
fasta_file = open(file_name+".fa","w")
fasta_file.write(sequence)
fasta_file.close()

fastas = sequence.split("\n")
list_species = []
for line in fastas:
	if line.startswith(">"):
		species = line[line.find("[")+1:line.find("]")]
		list_species.append(species)
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

subprocess.call("clustalo -i "+file_name+".fa -o clus_out.fa -outfmt fasta --force",shell=True)
'''
subprocess.call("plotcon -winsize 4 -graph svg -gsubtitle '"+protein_name+" in "+organism+"' -goutfile "+file_name+" clus_out.fa;display "+file_name+".svg",shell=True)



