from PyPDF2 import PdfFileReader , PdfFileWriter


def connector(f1n, f2n, out):
    file1_name = f1n
    file2_name = f2n
    
    file1 = PdfFileReader(open(file1_name,'rb'))
    file2 = PdfFileReader(open(file2_name,'rb'))
    output = PdfFileWriter()

    pageNum1 = file1.getNumPages()
    pageNum2 = file2.getNumPages()

    for i in range(pageNum1):
        output.addPage(file1.getPage(i))
    for i in range(pageNum2):
        output.addPage(file2.getPage(i))

    output.write(open(out,'wb'))


def merger(oname, ename, out):
    odd_file_name = oname
    even_file_name = ename

    odd_file = PdfFileReader(open(odd_file_name,'rb'))
    even_file = PdfFileReader(open(even_file_name,'rb'))
    output = PdfFileWriter()

    page_count = odd_file.getNumPages()

    for i in range(page_count):
        output.addPage(odd_file.getPage(i))
        output.addPage(even_file.getPage(page_count - 1 - i))

    output.write(open(out,'wb'))



if __name__ == '__main__':
    while 1:
        sw = input('[C]onnect or [M]erge: ')
        if sw in {'C', 'c'}:
            f1n = input('First file name : ')
            f2n = input('Second file name : ')
            out = input('Output file name: ')
            connector(f1n, f2n, out)
        elif sw in {'M', 'm'}:
            oname = input('Odd pages file name : ')
            ename = input('Even pages file name : ')
            out = input('Output file name: ')
            merger(oname, ename, out)

