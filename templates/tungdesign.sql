-- phpMyAdmin SQL Dump
-- version 4.0.9
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Feb 16, 2014 at 09:27 PM
-- Server version: 5.6.14
-- PHP Version: 5.5.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `tungdesign`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_product_to_order`(IN `userid` INT, IN `prodid` INT, IN `sze` INT, IN `amnt` INT)
    NO SQL
INSERT INTO `order_product_occurrance`(`Order_ID`, `Product_ID`, `Size`, `Amount`)
VALUES (users_latest_order(userid),prodid,sze,amnt)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_name_from_user_id`(IN `ID` INT)
    NO SQL
    DETERMINISTIC
select Firstname, Surname, Username from user where User_ID=ID$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_order_info_from_id`(IN `ID` INT)
    NO SQL
select * from orderregister where Order_ID = ID$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_products_from_order_id`(IN `ID` INT)
    NO SQL
select Product_Name, Size, Amount
from order_product_occurrance inner join product 
on order_product_occurrance.Product_ID = product.Product_ID
where Order_ID=ID
Order by Product_Name$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_prod_id_from_name`(IN `Name` VARCHAR(30))
    NO SQL
Select Product_ID from product where Product_Name = Name$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_prod_name_from_id`(IN `ID` INT)
    NO SQL
Select Product_Name from product where product_ID=ID$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `place_order`(IN `User` INT, IN `Date_p` DATE, IN `Date_d` DATE)
    DETERMINISTIC
INSERT INTO `orderregister`(`User_ID`, `Date_placed`, `Date_delivered`) 
VALUES (User,Date_p,Date_d)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `users_latest_order`(IN `userid` INT, OUT `orderid` INT)
Select Order_ID into orderid from orderregister
where User_ID = userid order by Order_ID desc limit 1$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `orderregister`
--

CREATE TABLE IF NOT EXISTS `orderregister` (
  `Order_ID` int(11) NOT NULL AUTO_INCREMENT,
  `User_ID` int(11) NOT NULL,
  `Date_placed` date NOT NULL,
  `Date_delivered` date DEFAULT NULL,
  PRIMARY KEY (`Order_ID`),
  UNIQUE KEY `User_ID` (`User_ID`),
  UNIQUE KEY `Order_ID` (`Order_ID`),
  KEY `User_ID_2` (`User_ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci AUTO_INCREMENT=101 ;

--
-- Dumping data for table `orderregister`
--

INSERT INTO `orderregister` (`Order_ID`, `User_ID`, `Date_placed`, `Date_delivered`) VALUES
(100, 1, '2014-02-09', '2014-02-11');

-- --------------------------------------------------------

--
-- Table structure for table `order_product_occurrance`
--

CREATE TABLE IF NOT EXISTS `order_product_occurrance` (
  `Order_ID` int(11) NOT NULL,
  `Product_ID` int(11) NOT NULL,
  `Size` int(11) NOT NULL,
  `Amount` int(11) NOT NULL,
  PRIMARY KEY (`Order_ID`,`Product_ID`,`Size`),
  KEY `Product_ID` (`Product_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

--
-- Dumping data for table `order_product_occurrance`
--

INSERT INTO `order_product_occurrance` (`Order_ID`, `Product_ID`, `Size`, `Amount`) VALUES
(100, 80111, 40, 2),
(100, 80111, 42, 2);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE IF NOT EXISTS `product` (
  `Product_ID` int(5) NOT NULL,
  `Product_Name` varchar(20) CHARACTER SET latin1 NOT NULL,
  `Price` int(11) NOT NULL DEFAULT '0',
  `Max_size` int(11) NOT NULL DEFAULT '48',
  `Min_size` int(11) NOT NULL DEFAULT '36',
  `Brand` varchar(20) CHARACTER SET latin1 NOT NULL,
  `Category` varchar(20) CHARACTER SET latin1 NOT NULL,
  `Info` varchar(150) CHARACTER SET latin1 NOT NULL DEFAULT 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat',
  `Pic_url` varchar(50) CHARACTER SET latin1 NOT NULL,
  `Classification` varchar(3) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`Product_ID`),
  UNIQUE KEY `Product_Name` (`Product_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`Product_ID`, `Product_Name`, `Price`, `Max_size`, `Min_size`, `Brand`, `Category`, `Info`, `Pic_url`, `Classification`) VALUES
(80111, 'Triumph', 699, 48, 36, 'Solid Gear', 'Sko', 'En sko helt utan komfort!', '', 'S3'),
(80113, 'Revolt', 599, 48, 36, 'Solid Gear', 'Sko', 'En fruktansvärt ofunktionell sko!', '', 'S3');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `User_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(30) CHARACTER SET latin1 NOT NULL,
  `Password` varchar(30) CHARACTER SET latin1 NOT NULL,
  `Firstname` varchar(40) CHARACTER SET latin1 NOT NULL,
  `Surname` varchar(40) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`User_ID`),
  UNIQUE KEY `firstname` (`Firstname`),
  UNIQUE KEY `surname` (`Surname`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci AUTO_INCREMENT=3 ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`User_ID`, `Username`, `Password`, `Firstname`, `Surname`) VALUES
(1, 'David', 'hasse', 'David', 'Hedin'),
(2, 'PuttePulla', 'pulla', 'Hamrik', 'Patsten');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orderregister`
--
ALTER TABLE `orderregister`
  ADD CONSTRAINT `orderregister_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order_product_occurrance`
--
ALTER TABLE `order_product_occurrance`
  ADD CONSTRAINT `order_product_occurrance_ibfk_1` FOREIGN KEY (`Product_ID`) REFERENCES `product` (`Product_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_product_occurrance_ibfk_2` FOREIGN KEY (`Order_ID`) REFERENCES `orderregister` (`Order_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
