import xlrd


def load_xl_workbook(file_loc):
    """
    Load the XL workbook using file location and return a workbook obj
    :param file_loc: string
    :return:
    """
    try:
        wb = xlrd.open_workbook(file_loc)
        return wb
    except Exception as e:
        raise e


def parse_wb_sheet(workbook, sheet_index=0, skip_first_nrow=1, skip_last_nrow=0):
    """
    Parse workbook obj and extract values from it.
    :param workbook: xl workbook
    :param sheet_index: int, index start from 0
    :param skip_first_nrow: int, skip first N number rows, default: 1
    :param skip_last_nrow: int, skip last N number rows, default: 0
    :return:
    """
    try:
        sheet = workbook.sheet_by_index(sheet_index)
        values = [sheet.row_values(r) for r in range(skip_first_nrow, sheet.nrows-skip_last_nrow)]
        return values
    except Exception as e:
        raise e


if __name__ == '__main__':
    pass
