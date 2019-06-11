import re
import docx
import xlrd
import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from appaaa.word_filter import WORDS


class SearchWord:

    def search_word(self, line_sting):
        texts = []
        for word in WORDS:
            t = re.search(word, line_sting.lower())
            if t is not None:
                texts.append(t.group())
        return texts


# TODO: Проверить файл с несколькими листами
# TODO: Вывод в консоль, временное решение
class Processing:
    FORMATS = ['docx', 'doc', 'xls', 'xlsx', 'excel', 'pdf', 'jpg', 'png']

    def extract_text_by_page(self, pdf_path):
        """ Работа с pdf файлами """
        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(resource_manager, fake_file_handle)
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text

                converter.close()
                fake_file_handle.close()

    def processing_pdf(self, _file):
        """ Работа с pdf файлами """
        for page in self.extract_text_by_page(_file):
            print(page)

    def processing_docx(self, _file):
        """ Работа с docx файлами """
        doc = docx.Document(_file)
        _filter = []
        for line in doc.paragraphs:
            if len(line.text) != 0:
                print(line.text)
                # _filter += list(self.search_word(line.text))
        # print(_filter)

    def processing_excel(self, f):
        """ Работа с 'xls', 'xlsx', 'excel' файлами """
        print('***********************************************')
        rb = xlrd.open_workbook(f.path)
        sheet = rb.sheet_by_index(0)
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            for c_el in row:
                print(c_el)
