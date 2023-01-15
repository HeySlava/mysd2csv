import pytest
from mysd2csv import get_filename
from mysd2csv import get_columns
from mysd2csv import save_csv_from_chunk


@pytest.mark.parametrize(
        'ddl,expected',
        [
            (
                (
                    '-- MySQL dump 9.11\n'
                    '--\n'
                    '-- Host: localhost    Database: pdns\n'
                    '-- ------------------------------------------------------\n'
                    '-- Server version	4.0.23_Debian-7-log\n'
                    '--\n'
                    '-- Table structure for table `domains`\n'
                    '--\n'
                    r'CREATE TABLE `domains` (\n'
                    '  `id` int(11) NOT NULL auto_increment,\n'
                ),
                'domains.csv',
            ),
            (
                (
                    '-- MySQL dump 9.11\n'
                    '--\n'
                    '-- Host: localhost    Database: pdns\n'
                    '-- ------------------------------------------------------\n'
                    '-- Server version	4.0.23_Debian-7-log\n'
                    '--\n'
                    '-- Table structure for table `domains`\n'
                    '--\n'
                    r'CREATE TABLE `pytest` (\n'
                    '  `id` int(11) NOT NULL auto_increment,\n'
                ),
                'pytest.csv',
            ),
        ],
        ids=['domains_table', 'pytest_table'],
)
def test_get_filename(ddl, expected: str):
    f = ddl.split('\n')
    output = get_filename(f)
    assert output == expected


@pytest.mark.parametrize(
    'ddl,expected',
    [
        (
            (
                ' `id` int(11) NOT NULL auto_increment,\n'
                " `name` varchar(255) NOT NULL default '',\n"
                ' `master` varchar(20) default NULL,\n'
                ' `last_check` int(11) default NULL,\n'
                " `type` varchar(6) NOT NULL default '',\n"
                ' `notified_serial` int(11) default NULL,\n'
                ' `account` varchar(40) default NULL,\n'
                ' PRIMARY KEY  (`id`),\n'
                ' UNIQUE KEY `name_index` (`name`)\n'
                ') TYPE=InnoDB;\n'
            ),
            ['id', 'name', 'master', 'last_check', 'type', 'notified_serial', 'account'],
        ),
    ],
    ids=['test1'],
)
def test_get_column_names(ddl, expected):
    ddl = ddl.split('\n')
    columns = get_columns(ddl)
    assert columns == expected


@pytest.mark.parametrize(
        'line,expected',
        [
            (
                r"INSERT INTO `domains` VALUES (1,'test.com',NULL,NULL,'NATIVE',NULL,NULL),(2,'ouvameuh.net',NULL,NULL,'NATIVE',NULL,NULL);",
                (
                    "1,'test.com',NULL,NULL,'NATIVE',NULL,NULL\n"
                    "2,'ouvameuh.net',NULL,NULL,'NATIVE',NULL,NULL"
                ),
            ),
            (
                r"INSERT INTO `domains` VALUES (1,'test.com',NULL,NULL,'NATIVE',NULL,NULL);",
                "1,'test.com',NULL,NULL,'NATIVE',NULL,NULL",
            ),
        ],
        ids=['long_line', 'short_line'],
)
def test_save_csv_from_chunk(line, expected, tmp_path):
    tmpfile = tmp_path / 'pytest.csv'
    save_csv_from_chunk(line, tmpfile)
    with tmpfile.open() as f:
        content = f.read()
        content = content.strip()

    assert content == expected
