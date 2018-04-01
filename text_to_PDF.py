from fpdf import FPDF
import numpy as np
from random import randint


letters = [i for i in 'abcdefghijklmnopqrtuvwxyz0123456789      ']
NO_OF_LETTERS = 500


text = " ".join([letters[randint(0,len(letters)-1)] for i in range(0,NO_OF_LETTERS)])

pdf=FPDF()
pdf.add_page()
pdf.set_font('Courier')
pdf.cell(40,10,text)
pdf.output('tuto1.pdf','F')
