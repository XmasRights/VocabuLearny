import sys, getopt
import csv

def main(argv):
	inputfile = ''
	outputfile = ''

	try:
		opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
	except getopt.GetoptError:
		print "usage: VocabuLearny.py -i <input file> -o <outputfile>\n"
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print "usage: VocabuLearny.py -i <input file> -o <outputfile>\n"
			sys.exit(2)
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	data = parseInputFile(inputfile)

def parseInputFile(inFile):
	data = []
	with open(inFile, 'rb') as csvfile:
		fileReader = csv.reader(csvfile, delimiter=",", quotechar='"')
		for row in fileReader:
			data.append(row)
	return data


if __name__ == "__main__":
	main(sys.argv[1:])