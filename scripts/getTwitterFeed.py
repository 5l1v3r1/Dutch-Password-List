import requests
import json

from time import sleep
import string

bearer_token = open("twitterkey/basicAuth",'r').read().strip()
API_URL = "https://api.twitter.com/2/"
allowed_chars = string.ascii_lowercase


def filterLine(line):
	line = line.replace('.',' ')
	line = line.replace(',',' ')
	line = line.replace('!',' ')
	line = line.replace('?',' ')

	words = line.split()
	new_words = []

	for word in words:

		if word == 'rt': # twitter thing
			continue
		
		isCleanWord = True
		for x in word.lower():
			if x not in allowed_chars:
				isCleanWord = False
				break
		
		if isCleanWord:
			new_words.append(word)

	if len(new_words) < 3:
		return ""

	return ' '.join(new_words)

def buildAPIURL(endpoint):
	return "%s%s" % (API_URL,endpoint)

def buildDutchSearchEndpoint(word):
	return 'tweets/search/recent?query=%s lang:nl' % word

def twitterGET(url):
	headers={'authorization':'Bearer %s' % bearer_token}
	resp = requests.get(url, headers=headers)

	return resp.text

fout = open('data/tweetData','a')
top100_words = ["als","zijn","dat","hij","was","voor","op","zijn","met","ze","zijn","bij","een","hebben","deze","van","door","heet","woord","maar","wat","sommige","is","het","of","had","de","van","aan","en","een","in","we","kan","uit","andere","waren","die","doen","hun","tijd","indien","zal","hoe","zei","een","elk","vertellen","doet","willen","lucht","goed","ook","klein","zetten","thuis","lezen","de","grote","toevoegen","zelfs","land","hier","moet","grote","hoog","dergelijke","volgen","waarom","vragen","mannen","verandering","ging","licht","soort","nodig","huis","proberen","ons","weer","dier","punt","moeder","wereld","dichtbij","bouwen","zelf","aarde","vader"]

while True:
	for word in top100_words:
		endpoint = buildDutchSearchEndpoint(word)
		# print("-----------Calling %s" % endpoint)

		url = buildAPIURL(endpoint)
		responseData = twitterGET(url)
		parsedData = json.loads(responseData)

		for tweet in parsedData["data"]:
			tweetText = tweet["text"].lower()
			filteredTweet = filterLine(tweetText)
			print("%s" % filteredTweet)
			fout.write(filteredTweet + "\n")
			
		sleep(2.5) # api is capped at max 30 requests per minute
