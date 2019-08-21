import xlrd



def create_data_test():
    wb = xlrd.open_workbook('D:/AUTOMATION - TESTING/ProductListing/data_synonyms.xlsx')
    sheet = wb.sheet_by_index(0)
    data_user = list()
    for rownum in range(1, sheet.nrows):
        user = dict()
        row_value = sheet.row_values(rownum)
        q = row_value[0]
        expect = row_value[1]

        data_user.append((str(q), str(expect)))
    print(data_user)
    return data_user
