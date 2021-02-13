### SQL Insert Generator
For times when you wish you had received a database link instead, don't want SQLDeveloper's import wizard to freeze your remote desktop for the 1000th time, and can't be bothered to open up Excel to concat fields into SQL inserts.

#### Requirements:
- `python3`
- `poetry`

#### Usage:
    poetry run generator {f_in} {*options}
![poetry run generator --help](images/cli_usage.png)

#### Input: f_in (CSV, TXT, XLSX, XLSM)
- If CSV/TXT: Delimiter = `,`; quote character = `"`
- If Excel: First ("active") sheet will be used

#### `Data type` options:
- `str` --> `varchar2(35)`
- `strX` --> `varchar2(X)`; `X::int`
- `int` --> `number(22,0)`
- `intX` --> `number(X, 0)`; `X::int`
- `float` --> `number(22,2)`

#### Output: {f_in}.sql
```
create table {table_name} (col1 col1_datatype, ...);
INSERT INTO {table_name} (col1, ...) VALUES (val1, ...);
...
```

#### Disclaimers:
- Datatypes use generic Oracle SQL types. 
- Number types default to 22 bits.
- `sql_generator.py` only checks the first row when determining types. If this is an issue, pass your own (encoded) types with `--types`
- Default file output is the path of the input file. Use `-outfile` parameter to redirect. 
- An output file will not be written if the print flag `-p` is used.
- Default table name is the name of the file with underscores replacing whitespaces.
