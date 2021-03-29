# scanomaly
Automated web fuzzing for anomalies (use python 3.6+)

# Project Roadmap
The project needs a few upgrades, for starters I'll be addressing the following in the short term

 + Improved Documentation (scanomaly.com/docs/) - This is *highest priority*
 + Fixing old broken modules (at a minimum, ones covered in this document)
 + Documenting the module/plugin creation process and Usage guides
 + Url tree (a way of tracking covered ground) and removing duplicate scans
 + Post Processing modules (do more things with the results)

## Description
The goal of this tool is to be a flexible request fuzzer. Modules generate a list of requests. A module can be used to alterate any part of a request. Each element of a request is configurable via the CLI too, the method types, user agents, headers, parameters. 
You can provide a single URL or list of urls to scan. 

The options below are mostly compulsory. By default it used 2 threads

`-u` provide a URL or `-ul` provide a file with a list of URLs 

`-scan` Runs a scan only if modules have been selected

`-t` is the number of threads to scan with

`-db` SQLite database name to store it in (example.db)


The following are mostly optional...

`-a` set a user agent for all requests

`-al` select a random user agent and use for all requests

`-ar` select a random user agent for each request

`-d` POST data to pass

`-c` Cookies to use

`-ic` Store full response content too

`-dl` Pass cli params into a module

## Modules
To view all modules and their info use `-m all -mi`
If you want to store the responses for the folowing modules, add `-db [databasename]`

`-m archives dirb parameth` Load specified modules

`-mx dirb-files` exclude a module by name

Some modules require arguments, it's important not to use these at the same time.

For example **dirb-files** takes an argument of filetypes `-dl html php asp` etc. If this is loaded at the same time as the vhost module it will interpret html as a passed domain and php as a list to be read.

#### baseline
This module will be used as a means of establishing baselines, this can be useful when later assessing the responses for anomalies.

` ./scanomaly.py -u http://127.0.0.1 -m baseline -scan -t 10 -db example.db`

#### dirb
This module scans a directory for common directories and filenames. An example use is the following:

` ./scanomaly.py -u http://127.0.0.1/ -m dirb -scan -t 10 -db example.db`

#### parameth
This module is used to brute force parameters and is based on (mak-/parameth)

` ./scanomaly.py -u http://127.0.0.1/ -m parameth -scan -t 10 -db example.db`

#### repo
This module scans a directory for common config, meta-info and code repo files.

` ./scanomaly.py -u http://127.0.0.1/ -m repo -scan -t 10 -db example.db`

#### archives
This module scans a directory for common archive files and generates additional archive names from the provided URL

` ./scanomaly.py -u http://127.0.0.1/ -m archives -scan -t 10 -db example.db`

#### dirb-files
This modules scans a directory for common file names using a specified file extension (default: html)

You can specify the filetype or file extension to use with `-dl [filetype] [filetype]...`

` ./scanomaly.py -u http://127.0.0.1/ -m dirb-files -dl php -scan -t 10 -db example.db`

#### dirb-custom
This module scans a directory for a provided file list

You can specify a file list to use by using `-dl [wordlist]`

` ./scanomaly.py -u http://127.0.0.1/ -m dirb-custom -dl [wordlist] -scan -t 10 -db example.db`

#### vhost
This scans a server for common dev virtual hosts or for a provided list of domains

You can provide a single domain to scan for using `-dl blah.com`

It is also possible to use `-dl blah.com [list of sub/domains]`

` ./scanomaly.py -u http://127.0.0.1/ -m vhost -dl localhost -scan -t 10 -db example.db`

#### fuzz / fuzzenc (url encoded)
This reads fuzz strings from a file and inserts them where specified.

\*@\* to specify where to fuzz in the url, headers, cookies or post data. You can use `-dl [fuzzlist]`

` ./scanomaly.py -u http://127.0.0.1/ -m fuzz -dl fuzzfile.txt -scan -t 10 -db example.db`

#### alt
This fuzzes all combinations of 3 chars abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 

and inserts them where specified. \*@\* to specify where to fuzz in the url, headers, cookies or post data. 

You can use `-dl [1-3]` to specify how many chars. 

` ./scanomaly.py -u http://127.0.0.1/ -m alt -dl 3 -scan -t 10 -db example.db`

#### getpost
This module is used to try a GET & POST request against each url provided

` ./scanomaly.py -u http://127.0.0.1/ -m getpost -scan -t 10 -db example.db`

#### s3bucket
This module generates permutations of a company name and brute forces AWS S# buckets

You can use `-u [1 or 2]` to specify the type of url to brute force. 1 is the old style s3.amazonaws.com/bucket/, 2 is the new style bucket.s3.amazonaws.com/

` ./scanomaly.py -u 2 -m s3bucket -dl [company_name] -scan -t 10 -db example.db`

#### basic
This module can brute force basic HTTP authentication

You can use `-dl [username] [username]...` to brute force using the specified usernames with a default password list.

`./scanomaly.py -u http://127.0.0.1/ -m basic -dl [username] -scan -t 10 -db example.db`

