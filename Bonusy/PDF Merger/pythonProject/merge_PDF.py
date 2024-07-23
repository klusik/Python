import PyPDF2


def merge_pdfs(paths, output):
    pdf_merger = PyPDF2.PdfMerger()
    for path in paths:
        pdf_merger.append(path)
    with open(output, 'wb') as f:
        pdf_merger.write(f)


pdfs = ['p1.pdf', 'p2.pdf']
merge_pdfs(pdfs, 'p1p2.pdf')
