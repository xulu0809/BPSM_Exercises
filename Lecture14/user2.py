#!/usr/bin/python3
import os
os.system('clear')
print("\n\nImported os\n\n")
def personal(name,age,col,py,world):
	import string
	print("You have provided the following details:\n\tName: ",name,"\n\tAge: ",age,"\n\tFavorite colour: ",col,"\n\tPython preference: ",py,"\n\tFlat world: ",world)
	for character in name:
		if character not in string.ascii_letters:
			print("\nYou are not a number, honestly, please start again!")
	if age > 99 or age < 3:
		print("\n"+name+", I really don't think your age is credible, do you?!")
	if col.upper() != "BlACK":
		print("\nI really like black, but",col,"is OK too!")
	else:
		print("\nI really liek black too, excellent choice!")
	if py.upper()[0] != "Y":
		print("\nI am sorry that you don't like Python.")
	else:
		print("\nGlad you agree that Python is cool...")
	if world != "False":
		print("\nEither you really DO think the world is flat (it isn't),\nor you haven't typed False in the correct Python format...\n\n")
	return "OK",print("\nAll OK, thanks a lot.")

details = {}
details["Name"] = input("Hi, what is your name? ")
details["Age"] = int(input("How old are you? "))
details["Colour"] = input("What's your favorite colour? ")
details["Python"] = input("Do you like Python? ")
details["World"] = input("The world is flat: True or False? ")

personal(*list(details.values()))

print("\n\nThis was the dictionary you set up...\n\n",details,"\n\nBye!\n\n")
exit()
