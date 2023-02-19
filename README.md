# MySQL dump to CSV with columns.

Convert single MySQL table dump into csv file with header.

# Example

```bash
-- MySQL dump 9.11
--
-- Host: localhost    Database: pdns
-- ------------------------------------------------------
-- Server version	4.0.23_Debian-7-log

--
-- Table structure for table `domains`
--

CREATE TABLE `domains` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL default '',
  `master` varchar(20) default NULL,
  `last_check` int(11) default NULL,
  `type` varchar(6) NOT NULL default '',
  `notified_serial` int(11) default NULL,
  `account` varchar(40) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name_index` (`name`)
) TYPE=InnoDB;

--
-- Dumping data for table `domains`
--

INSERT INTO `domains` VALUES (1,'test.com',NULL,NULL,'NATIVE',NULL,NULL),(2,'ouvameuh.net',NULL,NULL,'NATIVE',NULL,NULL);
```

```bash
# domain.csv
id,name,master,last_check,type,notified_serial,account
1,'test.com','','','NATIVE','',NU
2,'ouvameuh.net','','','NATIVE','',NU
```

The result with line by line style is the same.

```bash
...
INSERT INTO `domains` VALUES (1,'test.com',NULL,NULL,'NATIVE',NULL,NULL);
INSERT INTO `domains` VALUES (2,'ouvameuh.net',NULL,NULL,'NATIVE',NULL,NULL);

# domain.csv
id,name,master,last_check,type,notified_serial,account
1,'test.com','','','NATIVE','',NU
2,'ouvameuh.net','','','NATIVE','',NU
```

# Usage

```bash
git clone https://github.com/HeySlava/mysd2csv  && cd mysd2csv
chmod +x mysd2csv
./mysd2csv --input-file example.mysqldump.sql
```

```bash
usage: mysd2csv [-h] [-I INPUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -I INPUT, --input-file INPUT
                        Path to mysqldump
  -o OUTPUT, --output-file OUTPUT
                        Output filename. Default - name from dump.
```

### TODO
- [x] Replace NULL with `''` or provide a choice.
