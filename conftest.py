import pytest


@pytest.fixture
def dump():
    """Return test mysql dump."""
    dump = """\
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

INSERT INTO `domains` VALUES (1,'test.com',NULL,NULL,'NATIVE',NULL,NULL),(2,'ouvameuh.net',NULL,NULL,'NATIVE',NULL,NULL);\
        """
    return dump
