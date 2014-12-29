import sys, getopt
import csv

from reportlab.pdfgen import canvas

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

	# data = parseInputFile(inputfile)
	c = canvas.Canvas("hello.pdf")
	generateOutput(c)
	c.showPage()
	c.save()


def parseInputFile(inFile):
	data = []

	fileReader = csv.reader(open(inFile, 'rb'))
	for row in fileReader:
		data.append(row)
	return data

def generateOutput(output):
	output.drawString(100, 100, "Hello World")

if __name__ == "__main__":
	main(sys.argv[1:])