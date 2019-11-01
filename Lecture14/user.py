#!/usr/bin/python3
name = input("What's your name?\n\t")
print("\tHello, "+name+"!")

age = input("How old are you?\n\t")
if int(age) > 23:
	print("\tYou are elder than me!")
else:
	print("\tYou are younger than me!")

colour = input("What's your favourite colour?\n\t")
print("\tI like "+colour+" too!")

python = input("Do you like Python?(yes/no)\n\t")
if python == "yes":
	print("\tMe too!")
else:
	print("\tHope you'll like it in the future!")

world = input("The world is flat?(True or False)\n\t")
if world.lower() == "true":
	print("I don't think so.")
elif world.lower() == "false":
	print("Same with my opinion.")

