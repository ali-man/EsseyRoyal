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
    sw = SearchWord()

    def extract_text_by_page(self, pdf_path):
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
        """ Работа с pdf файлами
            Читает все страницы
        """
        filter_words = []
        for page in self.extract_text_by_page(_file.path):
            filter_words += list(self.sw.search_word(page))
        print(filter_words)

    def processing_docx(self, _file):
        """ Работа с docx файлами
            Читает все страницы по строчкам, пустые строки пропускает
        """
        doc = docx.Document(_file.path)
        filter_words = []
        for line in doc.paragraphs:
            if len(line.text) != 0:
                filter_words += list(self.sw.search_word(line.text))
        print(filter_words)

    def processing_excel(self, f):
        """
        Работа с 'xls', 'xlsx', 'excel' файлами
        Читает все страницы по строчкам, пустые строчки пропускает
        :param f: полученный файл из модели '' из метода save()
        :return:
        """
        rb = xlrd.open_workbook(f.path)
        filter_words = []
        for i in range(rb.nsheets):
            sheet = rb.sheet_by_index(i)
            for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)
                for c_el in row:
                    if len(str(c_el)) > 0:
                        filter_words += list(self.sw.search_word(str(c_el)))
        print(filter_words)
