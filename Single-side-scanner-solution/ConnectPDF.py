from PyPDF2 import PdfFileReader , PdfFileWriter

file1_name = input('First file name : ')
file2_name = input('Second pages file name : ')

file1 = PdfFileReader(open(file1_name,'rb'))
file2 = PdfFileReader(open(file2_name,'rb'))
output = PdfFileWriter()

pageNum1 = file1.getNumPages()
pageNum2 = file2.getNumPages()

for i in range(pageNum1):
    output.addPage(file1.getPage(i))
for i in range(pageNum2):
    output.addPage(file2.getPage(i))

output.write(open('Output.pdf','wb'))
