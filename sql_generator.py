import sys
import csv
import openpyxl


"""
Usage:
    python3 sql_generator.py {f_in} {table_name (optional)} {*data_types (optional)}
    
Input: f_in (CSV, TXT, XLSX, or XLSM)
    Delimiter: ,
    Quote character: "
    - If Excel, will use the first ("active") sheet

Data type options:
    "str" --> varchar2(35)
    "strX" --> varchar2(X); X::int
    "int" --> number(22,0)
    "intX" --> number(X, 0); X::int
    "float" --> number(22,2)
    
Output: {f_in}.sql
    create table {table_name} (col1 col1_datatype, ...);
    INSERT INTO {table_name} (col1, ...) VALUES (val1, ...);
    ...
"""


def main(f, table_name, data_types):
    ext = f.split(".")[1]

    if ext == "csv" or ext == "txt":
        load_csv(f, table_name, data_types)

    elif ext == "xlsx" or ext == "xlsm":
        load_excel(f, table_name, data_types)


def load_csv(f, table_name, data_types):
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar=r'"')

        with open("{}.sql".format(f.split("/")[-1].split(".")[0]), "w") as f_out:
            f_out.write("CREATE TABLE {} (".format(table_name))

            cols = next(csv_reader)
            col_names = ", ".join(cols)

            if data_types is None:

                first_vals = next(csv_reader)

                for i in range(len(cols) - 1):
                    f_out.write("{} {}, ".format(cols[i], get_col_type(first_vals[i])))

                f_out.write("{} {});\n".format(cols[-1], get_col_type(first_vals[-1])))

                f_out.write(
                    "INSERT INTO {} ({}) VALUES ({});\n".format(
                        table_name, col_names, ", ".join(first_vals)
                    )
                )

            else:
                for i in range(len(data_types) - 1):
                    f_out.write(
                        "{} {}, ".format(cols[i], convert_col_type(data_types[i]))
                    )

                f_out.write(
                    "{} {}); \n".format(cols[-1], convert_col_type(data_types[-1]))
                )

            for row in csv_reader:
                f_out.write(
                    "INSERT INTO {} ({}) VALUES ({});\n".format(
                        table_name, col_names, ", ".join(row)
                    )
                )


def load_excel(f, table_name, data_types):
    # Defaults to first sheet
    wb = openpyxl.load_workbook(f)
    ws = wb.active

    with open("%s.sql" % f.split("/")[-1].split(".")[0], "w") as f_out:
        f_out.write("CREATE TABLE {} (".format(table_name))

        cols = next(ws.values)
        col_names = ", ".join(cols)

        if data_types is None:

            first_vals = next(ws.values)

            for i in range(len(cols) - 1):
                f_out.write("{} {}, ".format(cols[i], get_col_type(first_vals[i])))

            f_out.write("{} {});\n".format(cols[-1], get_col_type(first_vals[-1])))

            f_out.write(
                "INSERT INTO {} ({}) VALUES ({});\n".format(
                    table_name, col_names, ", ".join(first_vals)
                )
            )

        else:
            for i in range(len(data_types) - 1):
                f_out.write("{} {}, ".format(cols[i], convert_col_type(data_types[i])))

            f_out.write("{} {}); \n".format(cols[-1], convert_col_type(data_types[-1])))

        for row_cells in ws.iter_rows(min_row=2):
            f_out.write(
                "INSERT INTO {} ({}) VALUES ({});\n".format(
                    table_name, col_names, ", ".join([str(i.value) for i in row_cells])
                )
            )


def get_col_type(val):
    # only checks if value can be converted to int or float, leaves as str if type conversion errors
    # only checks the first instance in each column -- will break if later VALUES are in different formats

    if val.isnumeric() is True or val.strip("-").isnumeric() is True:
        return "NUMBER(22,0)"

    elif val.strip("-").strip(".").isnumeric() is True:
        return "NUMBER(22,2)"

    else:
        if len(val) >= 20:
            return "VARCHAR2(128)"
        else:
            return "VARCHAR2(35)"


def convert_col_type(type_str):
    if type_str == "str":
        return "VARCHAR2(35)"
    elif type_str == "int":
        return "NUMBER(22,0)"
    elif type_str == "float":
        return "NUMBER(22,2)"
    elif type_str[:3] == "str" and type_str[3:].isnumeric():
        return "VARCHAR(%s)" % type_str[3:]
    elif type_str[:3] == "int" and type_str[3:].isnumeric():
        return "NUMBER(%s,0)" % type_str[3:]
    else:
        print("Datatype %s is invalid." % type_str)
        raise NameError


if __name__ == "__main__":
    try:
        tn = sys.argv[2]
    except IndexError:
        tn = sys.argv[1].split("/")[-1][:-4]

    try:
        dt = sys.argv[3:]
    except IndexError:
        dt = None

    main(f=sys.argv[1], table_name=tn, data_types=dt)
