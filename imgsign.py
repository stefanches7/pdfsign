from argparse import ArgumentParser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os
import re
parser = ArgumentParser("Edits already existing pdf adding text at the specified position. Thought to be most "
                        "effective performing a massive uniform editing of more PDFs than one.")

parser.add_argument('-m', '--model', action='store', nargs='?', help="The model file to modify. By default, "
                                                                   "the $root\\certificate.jpg is used.", default="certificate.jpg",
                    required=False)
parser.add_argument('-posX', '--positionX', action='store', type=int, nargs=1, help="X-axis start position of the " \
                                                                                  "future text "
                                                                          "frame. Measured in pixels.", required=True)
parser.add_argument('-posY', '--positionY', action='store', type=int, nargs=1, help="Y-axis start position of the "
                                                                                    "future text "
                                                                          "frame. Measured in pixels.", required=True)
parser.add_argument('-pl', '--padLine', action='store', type=int, nargs="?", help="Padding between the lines, substract from font size. Default 0.", default = 0, required=False)
parser.add_argument('-ps', '--padSide', action='store', type=int, nargs="?", help="Padding of second line from the left border. Default is 40.", default = 40, required=False)

parser.add_argument('-p', '--prefix', action='store', nargs='?', help="Prefix to add before each participant name", 
                    default="Dear",
                    required=False)
parser.add_argument('-botUp', '--bottomup', action='store',nargs="?", help="Specify this flag if you " \
                                                                                        "want to " \
                                                                                 "place "
                                                                            "your text frames counting distance from "
                                                                            "the bottom of the documents.", default=False)
parser.add_argument('-in', '--input', nargs="+", action='store', help="Specify the input. One argument here is "
                                                                      "treated as a relative path to the file "
                                                                      "containing the list of the text strings to "
                                                                      "insert into your file. If arguments are however more than one string, they are treated as "
                                                                      "a list of strings themselves", required=True)
parser.add_argument('-fS', '--fontSize', nargs="?", type=int, action='store', help="Specify the font size",
                    default=14, required=False)
parser.add_argument('-c', '--color', nargs=3, type=int, action='store', help="Text color, encoded as R G B.",
                    default=(255, 0, 0), required=False)

parser.add_argument('-f', '--font', nargs="?", action='store', help="Specify the font. By default, Verdana is used "
                                                                    "because of its good encoding capacities",
                    default='verdana.ttf', required=False)
parser.add_argument('-o', '--output', nargs="?", action='store', help="Specify the output directory. By default, "
                                                                      "$program's_root\pdfout is used.",
                    default='pdfout', required=False)
settings = parser.parse_args()
prefix = settings.prefix
col = settings.color
paddingX = settings.positionX[0]
paddingY = settings.positionY[0]
modelFile = settings.model
bottomUp= settings.bottomup
font = settings.font
fontSize = settings.fontSize
outputDir = settings.output
pl = settings.padLine
ps = settings.padSide

participantNames = []
if (len(settings.input)==1): #file with the list entered
    with open(settings.input[0]) as names:
        participantNames = names.readlines()
        participantNames = [x.strip() for x in participantNames]
else:
    participantNames = settings.input

if not os.path.exists(outputDir):
  os.mkdir(outputDir)

fontDrawer = ImageFont.truetype(font, fontSize)
for participantName in participantNames:
  m = Image.open(modelFile)
  draw = ImageDraw.Draw(m)
  if (re.match("(Ms|Mr|Mrs)", participantName)):  
    draw.text((paddingX, paddingY), "{0} {1}".format(prefix, " ".join(participantName.split(" ")[0:2])), (col[0],col[1],col[2]),
     font=fontDrawer)
    #rest of the name
    draw.text((paddingX + ps, paddingY + fontSize-pl), "{0}!".format(' '.join(participantName.split(" ")[2:])), (col[0],col[1],col[2]),
     font=fontDrawer)
  else:
    draw.text((paddingX, paddingY), "{0} {1}".format(prefix, participantName.split(" ")[0]), (col[0],col[1],col[2]),
     font=fontDrawer)
    #rest of the name
    draw.text((paddingX + ps, paddingY + fontSize-pl), "{0}!".format(' '.join(participantName.split(" ")[1:])), (col[0],col[1],col[2]),
     font=fontDrawer)
  m.save("{3}/{0}_{1}.{2}".format(modelFile.split(".")[0], participantName.replace(" ", "_"), modelFile.split(".")[1], outputDir ))