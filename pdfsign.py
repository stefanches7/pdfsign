from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from argparse import ArgumentParser

pdfmetrics.registerFont(TTFont("Verdana", "Verdana.ttf"))

parser = ArgumentParser("Edits already existing pdf adding text at the specified position. Thought to be most "
                        "effective performing a massive uniform editing of more PDFs than one.")

parser.add_argument('-m', '--model', action='store', nargs='?', help="The model file to modify. By default, "
                                                                   "the $root\\certificate.pdf is used.", default="certificate.pdf",
                    required=False)
parser.add_argument('-posX', '--positionX', action='store', type=int, nargs=1, help="X-axis start position of the " \
                                                                                  "future text "
                                                                          "frame. Measured in pixels.", required=True)
parser.add_argument('-posY', '--positionY', action='store', type=int, nargs=1, help="Y-axis start position of the "
                                                                                    "future text "
                                                                          "frame. Measured in pixels.", required=True)
parser.add_argument('-botUp', '--bottomup', action='store',nargs="?", help="Specify this flag if you " \
                                                                                        "want to " \
                                                                                 "place "
                                                                            "your text frames counting distance from "
                                                                            "the bottom of the documents.", default=False)
parser.add_argument('-in', '--input', nargs="+", action='store', help="Specify the input. One argument here is "
                                                                      "treated as a relative path to the file "
                                                                      "containing the list of the text strings to "
                                                                      "insert into your file, more than one - as "
                                                                      "a list of strings themselves", required=True)
parser.add_argument('-fS', '--fontSize', nargs="?", type=int, action='store', help="Specify the font size",
                    default=14, required=False)
parser.add_argument('-f', '--font', nargs="?", action='store', help="Specify the font. By default, Verdana is used "
                                                                    "because of its good encoding capacities",
                    default='Verdana', required=False)
parser.add_argument('-o', '--output', nargs="?", action='store', help="Specify the output directory. By default, "
                                                                      "$program's_root\pdfout is used.",
                    default='pdfout', required=False)
settings = parser.parse_args()

paddingX = settings.positionX[0]
paddingY = settings.positionY[0]
modelPDF = settings.model
bottomUp= settings.bottomup
font = settings.font
fontSize = settings.fontSize
outputDir = settings.output

participantNames = []
if (len(settings.input)==1): #file with the list entered
    with open(settings.input[0]) as names:
        participantNames = names.readlines()
        participantNames = [x.strip() for x in participantNames]
else:
    participantNames = settings.input

print("Names were", participantNames, ", posx:", paddingX, "model file:", modelPDF)

def drawname(overlayer, name): #sign the name of the participant
    overlayer.setFont(font, fontSize)
    overlayer.drawString(paddingX, paddingY, name)

for participantName in participantNames:
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    certOverlay = canvas.Canvas(packet, bottomup=bottomUp)
    drawname(certOverlay, participantName)
    certOverlay.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(modelPDF, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(outputDir + "/certificate-" + participantName + ".pdf", "wb")
    output.write(outputStream)
    outputStream.close()