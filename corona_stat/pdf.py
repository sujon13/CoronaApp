import tabula


def pdf_read(file):
    affected_number = {}
    try:
        tables = tabula.read_pdf(file, pages="all", multiple_tables=True, output_format="json")

        # district wise info

        data_table = tables[0]['data']
        data_table = data_table[1:]
        for row in data_table:
            if(row[1]['text']) != '':
                affected_number[row[1]['text']] = row[2]['text']
    except:
        print('error in reading the pdf')
    return affected_number

    # dhaka city detail info
    # = {}
    #data_table = tables[1]['data']
    # = data_table[1:]
    #for row in data_table:
    #    if(row[0]['text']) != '':
    #        affected_in_dhaka[row[0]['text']] = row[1]['text']
    #print(affected_in_dhaka)
