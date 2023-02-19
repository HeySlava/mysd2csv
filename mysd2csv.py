#!/usr/bin/python3


import argparse
import pathlib
import re

from io import TextIOWrapper
from typing import List


def get_filename(
        f: TextIOWrapper,
) -> str:
    filename_pattern = re.compile(r'(create table `(.*)` \()')

    for line in f:
        line = line.strip().lower()
        if filename_groups := filename_pattern.match(line):
            filename = filename_groups.group(2)
            return filename + '.csv'
    raise ValueError('Table name not found')


def get_columns(
        f: TextIOWrapper,
) -> List[str]:
    columns = []
    for line in f:
        if column_match := re.match(r'`(.*)`', line.strip()):
            columns.append(column_match.group(1).strip())
        else:
            break
    return columns


def save_csv_from_chunk(
    line: str,
    output_file: pathlib.Path,
    null: str = '',
) -> None:
    line = line[line.find('(')+1: -2]

    with open(output_file, 'a') as f:
        values = line.split(r'),(')
        values = list(map(lambda x: x.replace('NULL', null), values))
        f.writelines('\n'.join(values) + '\n')


def init_csv_file(
    filename: pathlib.Path,
    columns: List[str],
    sep: str = ',',
) -> None:
    with filename.open('w') as f:
        f.write(sep.join(columns) + '\n')


def mysql_to_csv():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-I',
        '--input-file',
        help='Path to mysqldump',
        dest='input',
    )
    parser.add_argument(
        '-o',
        '--output-file',
        help='Output filename. Default - name from dump.',
        dest='output',
    )

    parser.add_argument(
        '--null',
        default='',
        help='How to replace NULL. Default=\'\'',
    )
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        exit(1)

    try:
        path = pathlib.Path(args.input)
        input_file = open(path, 'r')
        num_lines = sum(1 for _ in open(args.input))
    except FileNotFoundError:
        print(f'Wrong input file path {args.input:!r}')
        exit(1)

    try:
        output_filename = get_filename(f=input_file)
        if args.output:
            output_filename = args.input.lstrip('.csv') + '.csv'

        columns = get_columns(f=input_file)
        init_csv_file(
                filename=pathlib.Path(output_filename),
                columns=columns,
            )

        c = 0
        for line in input_file:
            line = line.strip()
            if line.lower().startswith('insert into'):
                line = line[line.find('('): -2]
                save_csv_from_chunk(
                    line=line,
                    output_file=pathlib.Path(output_filename),
                    null=args.null,
                )
            c += 1
            print(f'{c} / {num_lines}')
    except Exception as e:
        print(e)
        print('Can"t parse {args.input:!r}')
    finally:
        input_file.close()


def main():
    mysql_to_csv()


if __name__ == '__main__':
    main()
