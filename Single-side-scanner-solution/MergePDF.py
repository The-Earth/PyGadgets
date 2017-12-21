from PyPDF2 import PdfFileReader , PdfFileWriter

odd_file_name = input('Odd pages file name : ')
even_file_name = input('Even pages file name : ')
output_file_name = input('Output file name : ')

odd_file = PdfFileReader(open(odd_file_name,'rb'))
even_file = PdfFileReader(open(even_file_name,'rb'))
output = PdfFileWriter()

page_count = odd_file.getNumPages()

for i in range(page_count):
    output.addPage(odd_file.getPage(i))
    output.addPage(even_file.getPage(page_count - 1 - i))

output.write(open(output_file_name,'wb'))
