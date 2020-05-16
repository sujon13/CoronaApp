import tabula


def pdf_read(file):
    affected_number = {}
    try:
        tables = tabula.read_pdf(file, output_format="json")

        # district wise info

        data_table = tables['data']
        data_table = data_table[1:]
        for row in data_table:
            if(row[1]['text']) != '':
                affected_number[row[1]['text']] = row[2]['text']
    except:
        print('error in reading the pdf')
    return affected_number

