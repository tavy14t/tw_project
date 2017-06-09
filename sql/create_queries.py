from pyPdf import PdfFileWriter, PdfFileReader
import os
import random

to_remove = []
idx = 1
for fileName in os.listdir('.'):
    try:
        if fileName.lower()[-3:] != "pdf":
            continue
        input1 = PdfFileReader(file(fileName, "rb"))

        # print the title of document1.pdf
        title = input1.getDocumentInfo().title
        if len(title) == 0:
            to_remove.append(fileName)
            continue
        print 'INSERT INTO POSTS(postid, userid, title, body) ' + \
            'VALUES(' + str(idx) + ',' + str(random.randint(1, 200)) + \
            ', "' + title + '","' + fileName + '");'
        idx += 1
    except:
        to_remove.append(fileName)


with open('to_remove', 'wb') as fhw:
    for file in to_remove:
        fhw.write(file + '\n')
