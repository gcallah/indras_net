"""
Filename: data_methods.py
Author: Gene Callahan
A collection of functions for exporting Indra data
"""

def pop_report(file_nm, varieties):
    """
    Write CSV file with pop data.
    Args:
        file_nm: file to write
        varieties: data to output
    """
    if len(file_nm) > 0:
        f = open(file_nm, "w")
        cols = []
        head = ''
        for i, var in enumerate(varieties):
            head += (var + ",")
            list = []
            cols.append(
                varieties[var]["data"])
        head = head[:-1]  # remove last comma!
        f.write(head + "\n")
        num_cols = len(cols)
        if num_cols > 0:
            num_rows = len(cols[0])
            for i in range(0, num_rows):
                srow = ''
                for j in range(0, num_cols):
                    srow += (str(cols[j][i]) + ',')
                srow = srow[:-1]  # remove last comma!
                f.write(srow + "\n")
        f.close()

