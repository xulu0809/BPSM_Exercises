#!/usr/bin/python3
import os
import subprocess

#protein_name = input("Please enter the protein name: ")
#organism = input("Please enter the organism: ")

protein_name = "glucose-6-phosphatase"
organism = "aves"

#need delete space?
file_name = protein_name+"_"+organism+".fa"
# run in unix command line; bytes -> string
def shell_run(command):
	output = subprocess.check_output(command,shell=True).decode()
	return output

#could be in a function?
cmd_search = "esearch -db protein -query '"+protein_name+"[PROT] AND "+organism+"[ORGN] NOT partial NOT predicted'"
info = shell_run(cmd_search).split()
count = (info[4])[7:-8]

if count == "0":
	print("No hits. Please check the spelling of protein and organism.")
# how to exit?
	exit()

print("There are "+count+" results found.")
cmd_fetch = cmd_search+" | efetch -db protein -format fasta"
sequence = shell_run(cmd_fetch)
fasta_file = open(file_name,"w")
fasta_file.write(sequence)
fasta_file.close()

fastas = sequence.split("\n")
list_species = []
for line in fastas:
	if line.find(">") == 0:
		species = line[line.find("[")+1:line.find("]")]
		list_species.append(species)
all_species = set(list_species)
print("There are "+str(len(all_species))+" species:\n"+"\n".join(all_species))
# continue or not?

