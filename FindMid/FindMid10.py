# -*- coding: utf-8 -*-

import re
import math
import os
import shutil
import sys
import subprocess

source_token_list = []
document_token_size = []
stop_word_list = []
index_list = []
jacet = []
word_stock = []
compression_topic = []
word_pair = []
#compression_temp = []
word_group_count = {}
word_value = {}
WeightWikipedia = []

WordNetWords = {}


token_dict = {} 

document_num = 0
dimension = 0
all_word = 0
compression_counter = 0
index_key = 0
key_word = ""

wordIndexDict = {}
LinkDictList = []

word_inDocuments = 0

threshold = 5.0
dimensionNumber = 10
optionValue = 0


#WordNetWords = []

##############################################################

def tf_idf():

	#print "a"
	global token_dict
	global source_token_list
	global document_num
	global all_word
	global document_token_size
	global WordNetWords
	global stop_word_list
	index = 1
	doc_id = 0
	count = 0
	weight = 0.0
	
	#file = open("NaturalLanguageTFIDF.txt","w")
	#method_name = open("method_list.txt","w")
	
	wordList = open("wordList.txt","w")
	
	outputTFIDF = open("OutputTF_IDF.txt","w")
	
	LDAinput = open("LDAinput.txt", "w")
	
	#outputLSH = open("Output_LSH_Input.txt","w")
	
	#stemmer = SnowballStemmer("english")
	
	for word in token_dict.keys():
		token_dict[word] = index
		#method_name.write('%s\n'%word)
		wordList.write('%s\n'%word)
		index += 1
		
	Wiki_dict = {}
	
	for source in source_token_list:
		
		#LSHTF_array = [0.0] * (len(token_dict) + 1)
		
		doc_id += 1
		
		print doc_id
		
		for word,frequent in source.items():
			count = 0
			for temp in source_token_list:
				if temp.has_key(word) == True: count += 1
				
			#print frequent
			weight = (float(frequent) / float(document_token_size[doc_id - 1])) * math.log(float(document_num) / float(count))
			source[word] = weight
			#print weight
			source_col = token_dict[word]
			#LSHTF_array[source_col] = weight
			
			outputTFIDF.write('%d ' %doc_id)
			outputTFIDF.write('%d ' %source_col)
			outputTFIDF.write('%f\n' %weight)
			
			LDAinput.write('%d ' %source_col)
			
		LDAinput.write("\n")
			
			#file.write('%d ' %doc_id)
			#file.write('%d ' %source_col)
			#file.write('%f\n' %weight)
			
			
		#for i in xrange(len(LSHTF_array)):
		#	outputLSH.write("%f "%(LSHTF_array[i]))
		#outputLSH.write("\n")
		
		#del LSHTF_array[:]
		
		#print sorted(source.items(), key=lambda x:x[1],reverse=True)
		
		#Length = len(source)
		#Length = Length / 2
		#WordCount = 0
		#for key,value in sorted(source.items(), key=lambda x:x[1],reverse=True):
		#	if(Length < WordCount): break
		#	if(len(key) < 4): continue
			#if(key in stop_word_list): continue
		#	if(key not in WordNetWords):
		#		file.write('%s\n'%(key))
		#		WordCount += 1
			
			
	#file.close()
	outputTFIDF.close()
	#outputLSH.close()
	wordList.close()
	LDAinput.close()
	

############################################################################################

############################################################################################

def WordNet_set():
	
	global WordNetWords
	
	extraction = re.compile("[ \t\n\r\f\v]")
	
	stemmer = SnowballStemmer("english")
	
	words = []

	for index_name in open("index_list.txt"):
		index_name = index_name.rstrip("\n")
		index = open(index_name,"r")
		#word = stemmer.stem(word)
		
		for line in index:
			parameter = extraction.split(line)
			if(len(parameter[0]) > 2):
				if(parameter[0] not in WordNetWords):
					WordNetWords.append(parameter[0])
	
	#print WordNetWords
	#print len(WordNetWords)

############################################################################################

############################################################################################

def compareByWordNet():
	global token_dict
	global WordNetWords
	
	#commonWords = open("commonWords.txt","w")
	
	extraction = re.compile("[ \t\n\r\f\v]")
	extractionWordId = re.compile("[0-9]{8}")
	
	wordVector = open("wordVector.txt","r")
	outputFindMid = open("outputFindMid.txt","w")
	
	words = []
	
	wordIndex = 1
	
	for index_name in open("index_list.txt"):
		index_name = index_name.rstrip("\n")
		index = open(index_name,"r")
		#word = stemmer.stem(word)
		
		for line in index:
			parameter = extraction.split(line)
			if(len(parameter[0]) > 2):
				if(parameter[0] not in WordNetWords):
					wordID = extractionWordId.findall(line)
					#WordNetWords.append(parameter[0])
					if(wordID != []):
						WordNetWords[parameter[0]] = wordID[0]
	
	#for key, value in token_dict.items():
	for k, v in sorted(token_dict.items(), key=lambda x:x[1]):
		line = wordVector.readline()
		if(WordNetWords.has_key(k)):
			#commonWords.write("%s %s\n"%(k, WordNetWords[k]))
			outputFindMid.write("%s %s %s"%(k, WordNetWords[k], line))
			
		else:
			outputFindMid.write("%s %s %s"%(k, "NULL", line))
			
	#for key, value in token_dict.items():
		#line = wordVector.readline()
		#if(WordNetWords.has_key(key)):
			#commonWords.write("%s %s\n"%(key, WordNetWords[key]))
		
	
	#commonWords.close()
	wordVector.close()
	outputFindMid.close()


############################################################################################

############################################################################################

def source_code_analyze(src_directory):
	print "source_code_analyze"
	global source_token_list
	global token_dict
	global stop_word_list
	global document_token_size
	
	global document_num
	global dimension
	global all_word
	coment_col = 0
	coment_flag = 0
	
	program_code = []
	
	source_dict = {}
	
	#words_in_Wikipedia = open("WordPairs_In_Wikipedia.txt", "w")
	#software_pattern = open("ImplementationPattern.txt","w")
	#compression_data = open("apache_ant_SVD_topics.txt","r")
	extraction_data = re.compile("[a-zA-Z]+")
	extraction_data2 = re.compile("[ ]+[a-zA-Z]{3,}[ ]+[0-9]+[ ]+[0-9.]+")
	
	extraction_classNode = re.compile("class [a-zA-Z0-9]+|extends [a-zA-Z0-9]+|implements [a-zA-Z0-9]+")
	
	extraction_methodNode = re.compile("[a-zA-Z0-9]+[a-zA-Z0-9 ]+[a-zA-Z0-9]+[(]+")
	extraction_methodName = re.compile("[a-zA-Z0-9_-]+[(]+")
	extraction_parameter = re.compile("[a-zA-Z0-9_-]+[ ]+[a-zA-Z0-9_-]+[ ]*[,]+|[a-zA-Z0-9_-]+[ ]+[a-zA-Z0-9_-]+[ ]*\)")
	
	extraction_word = re.compile("[A-Z]+[a-z]*|[a-z]+")
	
	#nodePair = open("nodePair.txt", "w")
	
	objectListFile = open("objectList.txt", "w")
	#LDAinput = open("LDAinput.txt", "w")
	MalletData = open("MalletData.txt", "w")
	
	
	count = 0
	
	classTerm = ""
	words = []
	
	commentFlag = 0
	
	for root,dirs,files in os.walk(src_directory):
		#if(root == dst_directory): continue
		#print "%s %s"%(root,dst_directory)
		#print root
		commentFlag = 0
		for file in files:
			file_path = os.path.join(root,file)
			identify = os.path.splitext(file_path)
			#if(identify[1] == ".java"): print file_path
			if(identify[1] == ".java"):
				#print file
				programFile = open(file_path, "r")
				classTerm = ""
				words = []
				
				for line in programFile:
					#print line
					
					if("//" in line):
						continue
					
					if("/*" in line):
						commentFlag = 1
						
					if("*/" in line):
						commentFlag = 0
						continue
					
					if(commentFlag == 1): continue
					
					classNode = extraction_classNode.findall(line)
					if(classNode != []):
						#print classNode
						for node in classNode:
							if("class" in node):
								className = node.lstrip("class[ ]+") + ":c"
								classTerm = className
								objectListFile.write("%s\n"%classTerm)
								#print className
								continue
								
							if("extends" in node):
								className = node.lstrip("extends[ ]+") + ":c"
								#print className
								#if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, className))
								#continue
								
							if("implements" in node):
								className = node.lstrip("implements[ ]+") + ":c"
								#print className
								#if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, className))
								#continue
					
					if(classTerm == ""): continue
					methodNode = extraction_methodNode.findall(line)
					if(methodNode != []):
						#print methodNode
						for node in methodNode:
							definedMethodNode = node.split(" ")
							if(len(definedMethodNode) > 2):
								#print node
								word = extraction_methodName.findall(node)
								if(word != []):
									#print word
									term = word[0].rstrip("(")
									#print term
									if(classTerm != ""):
									#	nodePair.write("%s - %s\n"%(classTerm, term))
										#LDAinput.write("%s "%term)
										#print term
										#validateSplitTerm(term)
										
										#tmpTerm = extraction_word.findall(term)
										tmpTerm = validateSplitTerm(term)
										#print tmpTerm
										if(tmpTerm != []):
											for tmp in tmpTerm:
												#LDAinput.write("%s "%tmp.lower())
												MalletData.write("%s "%tmp.lower())
												words.append(tmp.lower())
									
									continue
									
							word = extraction_methodName.findall(node)
							if(word != []):
								#print word
								term = word[0].rstrip("(")
								#print term
								if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, term))
									#LDAinput.write("%s "%term)
									#tmpTerm = extraction_word.findall(term)
									tmpTerm = validateSplitTerm(term)
									if(tmpTerm != []):
										for tmp in tmpTerm:
											#LDAinput.write("%s "%tmp.lower())
											MalletData.write("%s "%tmp.lower())
											words.append(tmp.lower())
								
								continue
							
									
								#parameters = extraction_parameter.findall(line)
								#if(parameters != []):
									#print parameters
								#	for parameter in parameters:
								#		pramWord = parameter.split(' ')
										#print pramWord[0]
								#		if(classTerm != ""):
											#nodePair.write("%s - %s\n"%(term, pramWord[0] + ":c"))
				
				if(classTerm != ""): 
					#LDAinput.write("\n")
					MalletData.write("\n")
					source_dict = {}
					document_num += 1
					all_word = 0
					all_frequent = 0
					
					if words == []:
						all_frequent = 0
						for freq in source_dict.values():
							all_frequent += freq
						source_token_list.append(source_dict)
						document_token_size.append(all_frequent)
					
					if words != []:
						for word in words:
							word = word.lower()
							#word = stemmer.stem(word)
							if (word in stop_word_list) == True: continue
							all_word += 1
							if token_dict.has_key(word) != True: 
								token_dict[word] = 1
								source_dict[word] = 1
								continue
							if source_dict.has_key(word) != True:
								source_dict[word] = 1
								continue
							token_dict[word] = token_dict[word] + 1
							source_dict[word] = source_dict[word] + 1
						
						all_frequent = 0
						for freq in source_dict.values():
							all_frequent += freq
						source_token_list.append(source_dict)
						document_token_size.append(all_frequent)
				
				programFile.close()
				
				
	
	#print source_token_list
	
	#nodePair.close()
	objectListFile.close()
	#LDAinput.close()
	MalletData.close()

############################################################################################################

############################################################################################

def CalcBag_of_words(src_directory):
	print "source_code_analyze"
	global source_token_list
	global token_dict
	global stop_word_list
	global document_token_size
	global optionValue
	global document_num
	global dimension
	global all_word
	coment_col = 0
	coment_flag = 0
	
	program_code = []
	
	source_dict = {}
	
	#words_in_Wikipedia = open("WordPairs_In_Wikipedia.txt", "w")
	#software_pattern = open("ImplementationPattern.txt","w")
	#compression_data = open("apache_ant_SVD_topics.txt","r")
	extraction_data = re.compile("[a-zA-Z]+")
	extraction_data2 = re.compile("[ ]+[a-zA-Z]{3,}[ ]+[0-9]+[ ]+[0-9.]+")
	
	extraction_classNode = re.compile("class [a-zA-Z0-9]+|extends [a-zA-Z0-9]+|implements [a-zA-Z0-9]+")
	
	extraction_methodNode = re.compile("[a-zA-Z0-9]+[a-zA-Z0-9 ]+[a-zA-Z0-9]+[(]+")
	extraction_methodName = re.compile("[a-zA-Z0-9_-]+[(]+")
	extraction_parameter = re.compile("[a-zA-Z0-9_-]+[ ]+[a-zA-Z0-9_-]+[ ]*[,]+|[a-zA-Z0-9_-]+[ ]+[a-zA-Z0-9_-]+[ ]*\)")
	
	extraction_word = re.compile("[A-Z]+[a-z]*|[a-z]+")
	
	#nodePair = open("nodePair.txt", "w")
	
	#objectListFile = open("objectList.txt", "w")
	#LDAinput = open("LDAinput.txt", "w")
	#MalletData = open("MalletData.txt", "w")
	
	outputBoW = open("outputBoW.txt", "w")
	wordList = open("wordList.txt","w")
	
	count = 0
	
	classTerm = ""
	words = []
	
	commentFlag = 0
	
	wordIndex = 1
	
	for root,dirs,files in os.walk(src_directory):
		#if(root == dst_directory): continue
		#print "%s %s"%(root,dst_directory)
		#print root
		commentFlag = 0
		for file in files:
			file_path = os.path.join(root,file)
			identify = os.path.splitext(file_path)
			#if(identify[1] == ".java"): print file_path
			if(identify[1] == ".java"):
				#print file
				programFile = open(file_path, "r")
				classTerm = ""
				words = []
				
				for line in programFile:
					#print line
					
					if("//" in line):
						continue
					
					if("/*" in line):
						commentFlag = 1
						
					if("*/" in line):
						commentFlag = 0
						continue
					
					if(commentFlag == 1): continue
					
					classNode = extraction_classNode.findall(line)
					if(classNode != []):
						#print classNode
						for node in classNode:
							if("class" in node):
								className = node.lstrip("class[ ]+") + ":c"
								classTerm = className
								#objectListFile.write("%s\n"%classTerm)
								#print className
								if(optionValue != 1): continue
								tmpTerm = validateSplitTerm(node.lstrip("class[ ]+"))
								#print tmpTerm
								if(tmpTerm != []):
									for tmp in tmpTerm:
										#LDAinput.write("%s "%tmp.lower())
										#MalletData.write("%s "%tmp.lower())
										words.append(tmp.lower())
								continue
								
							if("extends" in node):
								className = node.lstrip("extends[ ]+") + ":c"
								#print className
								#if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, className))
								#continue
								
							if("implements" in node):
								className = node.lstrip("implements[ ]+") + ":c"
								#print className
								#if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, className))
								#continue
					
					if(classTerm == ""): continue
					methodNode = extraction_methodNode.findall(line)
					if(methodNode != []):
						#print methodNode
						for node in methodNode:
							definedMethodNode = node.split(" ")
							if(len(definedMethodNode) > 2):
								#print node
								word = extraction_methodName.findall(node)
								if(word != []):
									#print word
									term = word[0].rstrip("(")
									#print term
									if(classTerm != ""):
									#	nodePair.write("%s - %s\n"%(classTerm, term))
										#LDAinput.write("%s "%term)
										#print term
										#validateSplitTerm(term)
										
										#tmpTerm = extraction_word.findall(term)
										tmpTerm = validateSplitTerm(term)
										#print tmpTerm
										if(tmpTerm != []):
											for tmp in tmpTerm:
												#LDAinput.write("%s "%tmp.lower())
												#MalletData.write("%s "%tmp.lower())
												words.append(tmp.lower())
									
									continue
									
							word = extraction_methodName.findall(node)
							if(word != []):
								#print word
								term = word[0].rstrip("(")
								#print term
								if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, term))
									#LDAinput.write("%s "%term)
									#tmpTerm = extraction_word.findall(term)
									tmpTerm = validateSplitTerm(term)
									if(tmpTerm != []):
										for tmp in tmpTerm:
											#LDAinput.write("%s "%tmp.lower())
											#MalletData.write("%s "%tmp.lower())
											words.append(tmp.lower())
								
								continue
							
									
								#parameters = extraction_parameter.findall(line)
								#if(parameters != []):
									#print parameters
								#	for parameter in parameters:
								#		pramWord = parameter.split(' ')
										#print pramWord[0]
								#		if(classTerm != ""):
											#nodePair.write("%s - %s\n"%(term, pramWord[0] + ":c"))
				
				if(classTerm != ""): 
					#LDAinput.write("\n")
					#MalletData.write("\n")
					source_dict = {}
					document_num += 1
					all_word = 0
					all_frequent = 0
					
					#if words == []:
					#	all_frequent = 0
					#	for freq in source_dict.values():
					#		all_frequent += freq
					#	source_token_list.append(source_dict)
					#	document_token_size.append(all_frequent)
					
					if words != []:
						for word in words:
							word = word.lower()
							#word = stemmer.stem(word)
							#if (word in stop_word_list) == True: continue
							all_word += 1
							if token_dict.has_key(word) != True: 
								token_dict[word] = wordIndex
								wordIndex += 1
								#source_dict[word] = 1
								#continue
							if source_dict.has_key(word) != True:
								source_dict[word] = 0
								#continue
							#token_dict[word] = token_dict[word] + 1
							source_dict[word] = source_dict[word] + 1
							
							#LDAinput.write("%d "%token_dict[word])
						
						#LDAinput.write("\n")
						
						all_frequent = 0
						for key, freq in source_dict.items():
							outputBoW.write("%d %d %f\n"%(document_num, token_dict[key], float(freq)))
						
						#for freq in source_dict.values():
							#all_frequent += freq
						#source_token_list.append(source_dict)
						#document_token_size.append(all_frequent)
				
				programFile.close()
				
				
	
	for k, v in sorted(token_dict.items(), key=lambda x:x[1]):
		#print k, v
		wordList.write("%s\n"%k)
	
	#print source_token_list
	
	#nodePair.close()
	#objectListFile.close()
	#LDAinput.close()
	#MalletData.close()
	outputBoW.close()
	wordList.close()

############################################################################################################


############################################################################################################

def calc_NGram_Collocation(src_directory):
	global wordIndexDict
	global LinkDictList
	global word_inDocuments
	global optionValue
	
	extraction_data = re.compile("[a-zA-Z]+")
	extraction_data2 = re.compile("[ ]+[a-zA-Z]{3,}[ ]+[0-9]+[ ]+[0-9.]+")
	
	extraction_classNode = re.compile("class [a-zA-Z0-9]+|extends [a-zA-Z0-9]+|implements [a-zA-Z0-9]+")
	
	extraction_methodNode = re.compile("[a-zA-Z0-9]+[a-zA-Z0-9 ]+[a-zA-Z0-9]+[(]+")
	extraction_methodName = re.compile("[a-zA-Z0-9_-]+[(]+")
	extraction_parameter = re.compile("[a-zA-Z0-9_-]+[ ]+[a-zA-Z0-9_-]+[ ]*[,]+|[a-zA-Z0-9_-]+[ ]+[a-zA-Z0-9_-]+[ ]*\)")
	
	extraction_word = re.compile("[A-Z]+[a-z]*|[a-z]+")
	
	commentFlag = 0
	classTerm = ""
	
	wordIndex = 0
	for root,dirs,files in os.walk(src_directory):
		
		commentFlag = 0
		for file in files:
			file_path = os.path.join(root,file)
			identify = os.path.splitext(file_path)
			#if(identify[1] == ".java"): print file_path
			if(identify[1] == ".java"):
				#print file
				programFile = open(file_path, "r")
				classTerm = ""
				words = []
				
				for line in programFile:
					#print line
					if("//" in line):
						continue
					
					if("/*" in line):
						commentFlag = 1
						
					if("*/" in line):
						commentFlag = 0
						continue
					
					if(commentFlag == 1): continue
					
					
					classNode = extraction_classNode.findall(line)
					if(classNode != []):
						#print classNode
						for node in classNode:
							if("class" in node):
								className = node.lstrip("class[ ]+") + ":c"
								classTerm = className
								
								tmpTerm = extraction_word.findall(node.lstrip("class[ ]+"))
								if(tmpTerm != []):
									word_inDocuments += len(tmpTerm)
									for i in xrange(len(tmpTerm) - 1):
										tmpTermLower = tmpTerm[i].lower()
										if(wordIndexDict.has_key(tmpTermLower) == False):
											wordIndexDict[tmpTermLower] = wordIndex
											LinkDictList.append({})
											wordIndex += 1
											
										nextTmpTermLower = tmpTerm[i + 1].lower()
										if(wordIndexDict.has_key(nextTmpTermLower) == False):
											wordIndexDict[nextTmpTermLower] = wordIndex
											LinkDictList.append({})
											wordIndex += 1
										
										if(LinkDictList[wordIndexDict[nextTmpTermLower]].has_key(tmpTermLower) == False):
											LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] = 0
										if(LinkDictList[wordIndexDict[tmpTermLower]].has_key(nextTmpTermLower) == False):
											LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] = 0
											
										LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] += 1
										LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] += 1
										#wordCountDict[tmpTerm[i].lower()] += 1
										#wordCountDict[tmpTerm[i + 1].lower()] += 1
										
										#if((EdgeDict.has_key(tmpTerm[i].lower() + "-" + tmpTerm[i + 1].lower()) == False) or (EdgeDict.has_key(tmpTerm[i + 1].lower() + "-" + tmpTerm[i].lower()) == False)):
										#	EdgeDict[tmpTerm[i].lower() + "-" + tmpTerm[i + 1].lower()] = 0
										#EdgeDict[tmpTerm[i].lower() + "-" + tmpTerm[i + 1].lower()] += 1
								
									#for tmp in tmpTerm:
									#	if(wordCountDict.has_key(tmp) == False):
									#		wordCountDict[tmp] = 0
									#	wordCountDict[tmp] += 1
								#print className
								continue
								
							if("extends" in node):
								className = node.lstrip("extends[ ]+") + ":c"
								#print className
								#if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, className))
								#continue
								
							if("implements" in node):
								className = node.lstrip("implements[ ]+") + ":c"
								#print className
								#if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, className))
								#continue
					
					if(classTerm == ""): continue
					methodNode = extraction_methodNode.findall(line)
					if(methodNode != []):
						#print methodNode
						for node in methodNode:
							definedMethodNode = node.split(" ")
							if(len(definedMethodNode) > 2):
								#print node
								word = extraction_methodName.findall(node)
								if(word != []):
									#print word
									term = word[0].rstrip("(")
									#print term
									if(classTerm != ""):
									#	nodePair.write("%s - %s\n"%(classTerm, term))
										#LDAinput.write("%s "%term)
										tmpTerm = extraction_word.findall(term)
										if(tmpTerm != []):
											word_inDocuments += len(tmpTerm)
											for i in xrange(len(tmpTerm) - 1):
												tmpTermLower = tmpTerm[i].lower()
												if(wordIndexDict.has_key(tmpTermLower) == False):
													wordIndexDict[tmpTermLower] = wordIndex
													LinkDictList.append({})
													wordIndex += 1
													
												nextTmpTermLower = tmpTerm[i + 1].lower()
												if(wordIndexDict.has_key(nextTmpTermLower) == False):
													wordIndexDict[nextTmpTermLower] = wordIndex
													LinkDictList.append({})
													wordIndex += 1
												
												if(LinkDictList[wordIndexDict[nextTmpTermLower]].has_key(tmpTermLower) == False):
													LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] = 0
												if(LinkDictList[wordIndexDict[tmpTermLower]].has_key(nextTmpTermLower) == False):
													LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] = 0
													
												LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] += 1
												LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] += 1
											
									continue
									
							word = extraction_methodName.findall(node)
							if(word != []):
								#print word
								term = word[0].rstrip("(")
								#print term
								if(classTerm != ""):
								#	nodePair.write("%s - %s\n"%(classTerm, term))
									#LDAinput.write("%s "%term)
									tmpTerm = extraction_word.findall(term)
									if(tmpTerm != []):
										word_inDocuments += len(tmpTerm)
										for i in xrange(len(tmpTerm) - 1):
											tmpTermLower = tmpTerm[i].lower()
											if(wordIndexDict.has_key(tmpTermLower) == False):
												wordIndexDict[tmpTermLower] = wordIndex
												LinkDictList.append({})
												wordIndex += 1
												
											nextTmpTermLower = tmpTerm[i + 1].lower()
											if(wordIndexDict.has_key(nextTmpTermLower) == False):
												wordIndexDict[nextTmpTermLower] = wordIndex
												LinkDictList.append({})
												wordIndex += 1
											
											if(LinkDictList[wordIndexDict[nextTmpTermLower]].has_key(tmpTermLower) == False):
												LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] = 0
											if(LinkDictList[wordIndexDict[tmpTermLower]].has_key(nextTmpTermLower) == False):
												LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] = 0
												
											LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] += 1
											LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] += 1
									
								continue
							
									
								parameters = extraction_parameter.findall(line)
								if(parameters != []):
									#print parameters
									for parameter in parameters:
										pramWord = parameter.split(' ')
										#print pramWord[0]
										if(classTerm != ""):
											#nodePair.write("%s - %s\n"%(term, pramWord[0] + ":c"))
											tmpTerm = extraction_word.findall(pramWord[0])
											if(tmpTerm != []):
												word_inDocuments += len(tmpTerm)
												for i in xrange(len(tmpTerm) - 1):
													tmpTermLower = tmpTerm[i].lower()
													if(wordIndexDict.has_key(tmpTermLower) == False):
														wordIndexDict[tmpTermLower] = wordIndex
														LinkDictList.append({})
														wordIndex += 1
														
													nextTmpTermLower = tmpTerm[i + 1].lower()
													if(wordIndexDict.has_key(nextTmpTermLower) == False):
														wordIndexDict[nextTmpTermLower] = wordIndex
														LinkDictList.append({})
														wordIndex += 1
													
													if(LinkDictList[wordIndexDict[nextTmpTermLower]].has_key(tmpTermLower) == False):
														LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] = 0
													if(LinkDictList[wordIndexDict[tmpTermLower]].has_key(nextTmpTermLower) == False):
														LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] = 0
														
													LinkDictList[wordIndexDict[nextTmpTermLower]][tmpTermLower] += 1
													LinkDictList[wordIndexDict[tmpTermLower]][nextTmpTermLower] += 1
													
											
				
				programFile.close()
				
	
	#print wordIndexDict
	#print LinkDictList
	


##########################################################################################################

def validateSplitTerm(targetTerm):
	global wordIndexDict
	global LinkDictList
	global word_inDocuments
	global threshold
	
	extraction_word = re.compile("[A-Z]+[a-z]*|[a-z]+")
	
	#threshold = 5.0
	resultValue = 0.0
	
	tmpTerm = extraction_word.findall(targetTerm)
	if(len(tmpTerm) < 2):
		return [targetTerm]
	
	#print tmpTerm
	
	coocurrence = 0
	coocurrence = LinkDictList[wordIndexDict[tmpTerm[0].lower()]][tmpTerm[1].lower()]
	
	#if(EdgeDict.has_key(tmpTerm[0].lower() + "-" + tmpTerm[1].lower())):
	#	coocurrence = EdgeDict[tmpTerm[0].lower() + "-" + tmpTerm[1].lower()]
	#if(EdgeDict.has_key(tmpTerm[1].lower() + "-" + tmpTerm[0].lower())):
	#	coocurrence = EdgeDict[tmpTerm[1].lower() + "-" + tmpTerm[0].lower()]
		
	w1 = 0
	
	for key, value in LinkDictList[wordIndexDict[tmpTerm[0].lower()]].items():
		w1 += int(value)
	
	#if(wordCountDict.has_key(tmpTerm[0].lower())):
	#	w1 = wordCountDict[tmpTerm[0].lower()]
	
	w2 = 0
	for key, value in LinkDictList[wordIndexDict[tmpTerm[1].lower()]].items():
		w2 += int(value)
	
	#if(wordCountDict.has_key(tmpTerm[1].lower())):
	#	w2 = wordCountDict[tmpTerm[1].lower()]
	
	
	resultValue = (float(coocurrence) * float(word_inDocuments)) / ((float(coocurrence) + float(w1)) * (float(coocurrence) + float(w2)))
	resultValue = math.log(resultValue, 2)
	
	#resultValue = (float(coocurrence) / float(word_inDocuments)) / ((float(w1) / float(word_inDocuments)) * (float(w2) / float(word_inDocuments)))
	#resultValue = math.log(resultValue)
	
	#print resultValue
	
	if(resultValue > threshold): return [tmpTerm[0] + tmpTerm[1]]
	
	return extraction_word.findall(targetTerm)
	

###########################################################################################################

def RandomizedSVDcall():
	global argvs
	global dimensionNumber
	
	
	cmd = "Randomized_SVD_second11.exe outputBoW.txt wordList.txt %d"%(dimensionNumber)
	subprocess.call(cmd.strip().split(" "))


###########################################################################################################

if __name__ == "__main__":
	#print "a"
	#src_directory = "D:\open_source_java_data\TimeProjectData\TestData5"
	
	
	argvs = sys.argv
	argc = len(argvs)
	
	print argvs
	#print argc
	
	
	if(argc != 5):
		
		print("Usage error...\n")
		quit()
		
	if(argvs[2].isdigit()):
		threshold = float(argvs[2])
		
	else:
		print("Usage error... argvs[2] is not digit\n")
		quit()
		
	if(argvs[3].isdigit()):
		dimensionNumber = float(argvs[3])
	else:
		print("Usage error... argvs[3] is not digit\n")
		quit()
	
	if(argvs[4] == "c" or argvs[4] == "f"):
		if(argvs[4] == "f"):
			optionValue = 1
		else:
			optionValue = 0
	else:
		print("Usage error... argvs[4] is not c or f\n")
		quit()
	
	print "ok\n"
	
	src_directory = argvs[1]
	
	calc_NGram_Collocation(src_directory)
	#dst_directory = "D:\designPatternDetectionTool\data\jajukData\jajuk-java-installer-1.4"
	#source_code_analyze(src_directory)
	#tf_idf()
	
	CalcBag_of_words(src_directory)
	RandomizedSVDcall()
	compareByWordNet()
	

