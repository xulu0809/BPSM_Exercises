#!/usr/bin/python3
import os,sys
import subprocess

# some information about this program
print("###This is a program which will give you some useful information \
about a protein family of a taxonomic group. ")
# some input hints for the user
print('If the protein name or the taxonomic group consists of several words, you need to put them in a ""!\
\n\tFor example: kinase, mammals, "ABC transporter"')

# read input from the user
protein_name = input("Please enter the protein name (singular form): ")
organism = input("Please enter the taxonomic group (plural form): ")
# delete space and quotation marks for using it as filename
file_name = (protein_name+"_"+organism).replace(" ","").replace('"',"")
# check input
if ((" " in protein_name) and (protein_name.startswith('"')==False or protein_name.endswith('"')==False))\
 or ((" " in organism) and (organism.startswith('"')==False or organism.endswith('"')==False)):
	print("Please check if you added the right double quotation marks! Please start again!")
	exit()

# ask the user if the predicted sequences need to be excluded from the results
# the return value will be added in the esearch query
def exclude_predicted():
	pre = input("Do you want to exclude predicted sequences? (y/n): ")
	if pre.upper() == "Y":
		return " NOT predicted"
	elif pre.upper() == "N":
		return ""
	else:
		print("Sorry, you can only use 'y' or 'no'.")
		exclude_predicted()
predicted = exclude_predicted()
	
# search for proteins and get result counts information 
def search(prot,orgn):
	cmd_search = "esearch -db protein -query '"+prot+"[PROT] AND "+orgn+\
	"[ORGN] NOT partial"+predicted+"'"
	cmd_getcount = "xtract -pattern ENTREZ_DIRECT -element Count"
	# read the output in the shell, and change it to String format, delete the new line symbol
	count = subprocess.check_output(cmd_search+" | "+cmd_getcount,shell=True).decode().strip()
	# check if there is result, if the count is 0, let user start again
	if count == "0":
		print("No hits. Please check the spelling of protein and organism and start again.")
		exit()
	print("There are "+count+" results found.\nIf there are more than 10000 \
results, then we strongly recommend you to find a smaller taxonomic group")

# ask the user whether to continue
def ifcontinue():
	y_n = input("Do you want to continue? (y/n): ")
	if y_n == "n":
		print("Quiting...")
		exit()
	elif y_n != "y":
		print("Sorry, you can only use 'y' or 'n'.")
		ifcontinue()
# fasta file -> dictionary
# accession as key, fasta sequence as value
def seqdic(seqfilename):
	dic = {}
	seqfile = open(seqfilename)
	for line in seqfile:
		if line.startswith(">"):
			# delete ">" in the accession
			seqname = line.split()[0].replace(">","")
			dic[seqname] = line
		else:
			# get the sequences all in one line
			dic[seqname] += line.replace("\n","")
	return dic

# download the sequences from NCBI and print the number of species and their names.
def fetch(prot,orgn,flnm):
	os.system("esearch -db protein -query '"+prot+"[PROT] AND "+orgn+"[ORGN] NOT partial"\
		+predicted+"' | efetch -db protein -format fasta >"+flnm+".fa")
	# get the list of all species of these sequences
	raw_fasta = open(flnm+".fa")
	list_species = []
	for line in raw_fasta:
		if line.startswith(">"):
			# find the species name
			species = line[line.find("[")+1:line.find("]")]
			list_species.append(species)
	# list -> set, use length to get the number of species, print the information
	all_species = set(list_species)
	print("There are "+str(len(all_species))+" species:\n"+", ".join(all_species))
	
# use clustalo to align all the sequences, and from the infoalign
#find one sequence with the smallest number of differences
def getcons(flnm): 
	# don't know why the default 64 threads runs slower than 32 threads...
	os.system("clustalo -i "+flnm+".fa -o "+flnm+"_clus.fa --outfmt fasta -v --threads=32 --force")
	os.system("infoalign -sequence "+flnm+"_clus.fa -outfile "+flnm+".info -nousa")
	print("Some information about the clustalo result is saved in the file "+flnm\
		+".info.\nShowing the first 5 lines for you.\n\n")
	aligninfo = open(flnm+".info")
	count = 0
	# compare the differ column of every sequence, find the smallest one
	# set diffcount at a large number
	diffcount = 100000
	for line in aligninfo:
		count += 1
		if count<=5:
			print(line)
		if line.startswith("#") == False and int(line.split()[7]) < diffcount:
			diffcount = int(line.split()[7])
			name = line.split()[0]
	return name

# get 250 most similar sequences
def find250(flnm): 
	os.system("makeblastdb -in "+flnm+".fa -dbtype prot -out "+flnm)
	os.system("blastp -db "+flnm+" -query cons.fa -outfmt 7 > blastp.out")
	blastp = open("blastp.out")
	# a list to store the accessions of the 250 sequences
	acc250 = []
	count = 0
	for line in blastp:
		if line.startswith("#") == False and count < 250:
			count += 1
			acc250.append(line.split()[1])
	# build a dictionary, from the accession list, get the sequences from raw swquences dictionary
	sequences250 = {}
	file250 = open("seq250.fa","a")
	for acc in acc250:
		seq_in250 = rawseqs.get(acc)
		sequences250[acc] = seq_in250
		file250.write(seq_in250.replace(">","\n>"))
	file250.close()
	os.remove(flnm+".fa")
	os.rename("seq250.fa",flnm+".fa")
	# align the chosen sequences
	print("Multi-align for the subset of sequences...")
	os.system("clustalo -i "+flnm+".fa -o "+flnm+"_clus.fa --outfmt fasta -v --threads=32 --force")
	return sequences250

# plot the conservation of aligned sequences
def plotcon(flnm):
	os.system("plotcon -winsize 4 -graph svg -gsubtitle '"+flnm+"' -goutfile "\
		+flnm+" "+flnm+"_clus.fa;display "+flnm+".svg")

# scan motif from PROSITE
def scanmotif(sequence_dictionary):
	motifs = []
	for seq in sequence_dictionary.values():
		# build a temperory file to store one sequence a time
		temfile = open("temfile.fa","w")
		temfile.write(seq)
		temfile.close()
		os.system("patmatmotifs -sequence temfile.fa -outfile site.tem -auto")
		site = open("site.tem")
		for line in site:
			# find the line of information about motif name
			if line.startswith("Motif"):
				# get the name of the motif, delete useless space or other stuff
				motifs.append(line.split(" = ")[1].rstrip())
	if len(set(motifs)) == 0:
		print("There are no known motifs.")
	else:
		print("There are "+str(len(set(motifs)))+" known motifs.\nMotif: "+",".join(set(motifs)))
	os.remove("temfile.fa")
	os.remove("site.tem")

# calculate statistics of protein properties
def stat(flnm):
	os.system("pepstats -sequence "+flnm+".fa -outfile "+flnm+".pepstats")
	print("All the statistic information for sequences are saved in file "+flnm+".pepstats.")
	print("Showing the statics of the most consensus sequence...")
	os.system("pepstats -sequence cons.fa -outfile cons.pepstats; cat cons.pepstats")
# plot the sequence alignment.
def prettyplot(flnm):
	os.system("prettyplot -sequence "+flnm+"_clus.fa -graph x11 -residuesperline 100")

# steps to run
search(protein_name,organism)
ifcontinue()
print("Downloading protein sequences from NCBI...")
fetch(protein_name,organism,file_name)
ifcontinue()
print("Multi-align for protein sequences...")
conseqfile = open("cons.fa","w")
# dictionary for raw sequence fasta
rawseqs = seqdic(file_name+".fa")
# get the most consensus sequence, and store it in a file
conseq = rawseqs.get(getcons(file_name))
conseqfile.write(conseq)
conseqfile.close()
# if there are more than 250 sequences, than find the most simialr 250 sequences
dic = rawseqs
if len(rawseqs) > 250:
	print("#The number of sequences is more than 250, Using blastp to find the most similar one...")
	dic = find250(file_name)
plotcon(file_name)
print("Searching for known motifs of protein sequences...")
scanmotif(dic)
print("If you continue, we will calculate the statics of the sequences and show the plot of alignment.")
ifcontinue()
stat(file_name)
print("Showing the plot of alignment, press 'Enter' to the next page and finish.")
prettyplot(file_name)
