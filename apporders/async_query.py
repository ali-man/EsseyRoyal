from apporders.processing_files import Processing


def checking_files(f):
    pc = Processing()
    file_format = f.name.split('.')[-1]

    if file_format == 'docx':
        pc.processing_docx(f)

    elif file_format == 'xls' or file_format == 'xlsx' or file_format == 'excel':
        pc.processing_excel(f)

    elif file_format == 'pdf':
        pc.processing_pdf(f)

    elif file_format == 'jpg' or file_format == 'png':
        pass

    elif file_format == 'doc':
        pass

    else:
        pass
