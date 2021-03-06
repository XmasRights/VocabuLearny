import sys, getopt
import csv

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from random import sample

# http://www.reportlab.com/docs/reportlab-userguide.pdf
# http://www.blog.pythonlibrary.org/2013/08/09/reportlab-how-to-combine-static-content-and-multipage-tables/ 
########################################################################

class DocumentMaker(object):

    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
 
    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y
 
    #----------------------------------------------------------------------
    def run(self, appData, heading = "Worksheet", outputName = "test.pdf", removeCount = 1):
        """
        Run the report
        """
        self.removeCount = removeCount
        self.heading = heading
        self.doc = SimpleDocTemplate(outputName)
        self.story = [Spacer(1, 0.1*inch)]
        self.createLineItems(appData)
 
        self.doc.build(self.story, onFirstPage=self.createDocument)
 
    #----------------------------------------------------------------------
    def createDocument(self, canvas, doc):
        """
        Create the document
        """
        font_size = 18
        self.c = canvas
        normal = self.styles["Normal"]
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
 
        header_text = "<font size=%s><b>%s</b></font>" % (font_size, self.heading)
        p = Paragraph(header_text, centered)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(0, 12, mm))
 	
 	#----------------------------------------------------------------------

    def randData(self, appData):
 		output = []
 		for line in list(x for x in appData):
 			change_locations = set(sample(range(len(line)), self.removeCount))
 			changed = ("" if i in change_locations else c for i,c in enumerate(line))
 			output.append(list(x for x in changed))
 		return output

    #----------------------------------------------------------------------
    def createLineItems(self, appData):
        """
        Create the line items
        """
        headers = appData[0]
        table_data = self.randData(appData[1:])

        header_font_size = 14
        table_font_size = 12
        column_width = 140
        row_height = 40
        table_style = [ ('GRID', (0,0), (-1,-1), 1, colors.black), ('VALIGN',(0,0),(-1,-1),'MIDDLE') ]
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)

        # Format Header
        d = []
        for text in headers:
            ptext = "<font size=%s><b>%s</b></font>" % (header_font_size, text)
            p = Paragraph(ptext, centered)
            d.append(p)
 
        data = [d]

        # Format Table Data
        formatted_line_data = []
        for line in table_data:
            for item in line:
                ptext = "<font size=%s>%s</font>" % (table_font_size, item)
                p = Paragraph(ptext, centered)
                formatted_line_data.append(p)
            data.append(formatted_line_data)
            formatted_line_data = []
 
        table = Table(data, style = table_style, rowHeights=row_height, colWidths=[column_width, column_width, column_width])
 
        self.story.append(table)
 
#----------------------------------------------------------------------

def main(argv):
	inputfile = ''
	outputfile = ''
	count = 1
	answers = 0
	blank_cells = 1

	try:
		opts, args = getopt.getopt(argv, "hi:o:c:b:a:", ["ifile=", "ofile=", "ocount", "oblanks", "oanswers"])
	except getopt.GetoptError:
		print "usage: VocabuLearny.py -i <input file> -o <outputfile> -c <number of output sheets> -b <number of blank cells per row> -a <create answer sheet>\n"
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print "usage: VocabuLearny.py -i <input file> -o <outputfile> -c <number of output sheets> -b <number of blank cells per row> -a <create answer sheet>\n"
			sys.exit(2)
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-c", "ocount"):
			count = int(arg)
		elif opt in ("-b", "oblanks"):
			blank_cells = int(arg)
		elif opt in ("-a", "oanswers"):
			answers = 1

	data = parseInputFile(inputfile)
	heading = data[0][0]
	data.pop(0)

	t = DocumentMaker()
	for x in range(count):
		title = heading + " " + str(x)
		t.run(data, title, title + ".pdf", blank_cells)

	if answers:
		page_header = heading + " Answers"
		file_title = heading + " Answers.pdf"
		page_blank_cells = 0
		t.run(data, page_header, file_title, page_blank_cells)

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


