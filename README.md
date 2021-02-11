# IST 441 crawl repository
basic template to crawl for [Data Science Stack Exchange](https://datascience.stackexchange.com/) using scrapy

Some quirks of this project - 

 - Crawls only question pages
 - Crawls preferably accepted answers, if available
 - Uses bs4 for finer parsing of the data and can be replaced with xpath
 - Can be extended to other stackexchange webpages listed on - [Hot Questions - Stack Exchange](https://stackexchange.com/)

to run the code - `stack crawl getquestions`
