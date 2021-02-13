import click
from sql_insert_generator.sql_generator import load_csv, load_excel
from os import path


@click.command()
@click.option(
    "--types",
    default=None,
    help="""String of datatypes to be used for each field in the same order as in the input file. \n
              Will infer type from first row of data if not enough type values are supplied. \n
              Pass as a quoted string: 'type1 type2 type3'. """,
)
@click.option("--outfile", default=None, help="Output file if -p is not enabled.")
@click.option("--table", default=None, help="Table name used for SQL statements.")
@click.option(
    "-p",
    flag_value=True,
    is_flag=True,
    help="Prints SQL statements to terminal instead of creating a SQL file. Will override outfile argument.",
)
@click.argument("infile")
def cli(infile, outfile, table, p, types):
    if p:
        outfile = None
    elif not outfile:
        outfile = ".".join(infile.split(".")[:-1]) + ".sql"

    if types:
        types = types.split(" ")

    if not table:
        table = path.basename(path.normpath(path.splitext(infile)[0]))

    ext = infile.split(".")[-1]

    if ext == "csv":
        e = load_csv(infile, outfile, table, types, p)

    elif ext == "xlsx" or ext == "xlsm":
        e = load_excel(infile, outfile, table, types, p)

    else:
        raise click.ClickException(
            "Invalid filetype. Input file extension should be .csv, .xlsx, or .xlsm"
        )

    if e:
        raise click.ClickException(e)


if __name__ == "__main__":
    cli()
