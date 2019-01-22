'''Program which prompts the user for a word and returns its dictionary definition if the word is contained in dictionary. If it is not, the program finds the words most closely matching the input word and prompts the user for confirmation'''

#import necessary libraries

import json
import difflib
from difflib import SequenceMatcher as sm, get_close_matches as gcm
data = json.load(open("data.json"))

def define_word(word):
	word = word.lower()
	if word in data.keys():		#If searched word is a key in dict, return it
		return data[word]
	elif len(gcm(word, data.keys(), cutoff = 0.8)) > 0:	#If word does not exist in keys, but is similar enough to words that do
		mist = input("Did you mean %s instead of %s ? Enter Y for yes, and N for no:\n" %(gcm(word, data.keys(), cutoff = 0.8)[0], word)) 
		if mist == 'Y':
			return data[gcm(word, data.keys(), cutoff = 0.8)[0]]	#Return first element of the list of similar words returned by function get_close_matches
		elif mist == 'N':
			return "Sorry, the word does not exist"
		else: 
			return "Sorry, invalid input"
		
	else:
		print("Sorry, invalid input")

while input("Welcome to word definer, enter any character to continue, or press enter to quit.\n"):
	w = input("Enter word to define:\n")
	output = define_word(w)
	if type(output) == list:
		for item in output:
			print(item+'\n')
