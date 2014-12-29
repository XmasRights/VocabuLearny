import sys, getopt
import csv

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer
 

# http://www.blog.pythonlibrary.org/2013/08/09/reportlab-how-to-combine-static-content-and-multipage-tables/ 
########################################################################
class Test(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
 
    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """

http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab

        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y
 
    #----------------------------------------------------------------------
    def run(self, appData):
        """
        Run the report
        """
        self.doc = SimpleDocTemplate("test.pdf")
        self.story = [Spacer(1, 2.5*inch)]
        self.createLineItems(appData)
 
        self.doc.build(self.story, onFirstPage=self.createDocument)
        print "finished!"
 
    #----------------------------------------------------------------------
    def createDocument(self, canvas, doc):
        """
        Create the document
        """
        self.c = canvas
        normal = self.styles["Normal"]
 
        header_text = "<b>This is a test header</b>"
        p = Paragraph(header_text, normal)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(100, 12, mm))
 
        ptext = """This is a descriptive paragraph"""
 
        p = Paragraph(ptext, style=normal)
        p.wrapOn(self.c, self.width-50, self.height)
        p.drawOn(self.c, 30, 700)
 
    #----------------------------------------------------------------------
    def createLineItems(self, appData):
        """
        Create the line items
        """
        text_data = ["Number", "English", "French"]
        d = []
        font_size = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in text_data:
            ptext = "<font size=%s><b>%s</b></font>" % (font_size, text)
            p = Paragraph(ptext, centered)
            d.append(p)
 
        data = [d]
 
        line_num = 1
 
        formatted_line_data = []

        for line in appData:
            for item in line:
                ptext = "<font size=%s>%s</font>" % (font_size-1, item)
                p = Paragraph(ptext, centered)
                formatted_line_data.append(p)
            data.append(formatted_line_data)
            formatted_line_data = []
            line_num += 1
 
        table = Table(data, colWidths=[60, 60, 60])
 
        self.story.append(table)
 
#----------------------------------------------------------------------


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

	t = Test()
	t.run(data)


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


