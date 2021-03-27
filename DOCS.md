# Scanomaly Docs
Modules create lists of RequestObjects to be run by the RequestEngine

**RequestObject Arguments**
This represents a request TO BE performed

 * *reqID*: Request identifier ( used to match requests to responses ) 
 * *method*: Request Method ( eg: GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD )
 * *proxy*: CLI parsed proxy from (`-p` http://127.0.0.1:8080 )
 * *headers*: CLI parsed headers from (`-H` "a:b" "c:d" ) 
 * *timeout*: Timeout for a request (`-T` time for response in seconds )
 * *cookies*: CLI parsed cookies (`-C` "cookie=string;like=this; )
 * *url*: The URL being requested
 * *data*: Paramter data being passed 
 * *module*: The name of the request generation module

**ResultObject Arguments**
This represents response data AFTER a request is performed

 * *respID*: Response identifier ( used to match requests to reponses )
 * *responseSize*: Response size of the request
 * *statusCode*: HTTP response status (eg: 200, 301, 403, 500 etc)
 * *time*: Time taken for request
 * *numHeaders*: The number of headers in the response
 * *numTokens*: The number of word tokens in the response content
 * *headers*: The response headers in full
 * *content*: The full body of the response

**urlObject functions**
This allows easier manipulation of a URL in a Module

Example URL: **https://dom.com/folder/file.php?query=data**
 * *u_d*: Current URL to last directory ( https://dom.com/folder/ )
 * *u_dd*: Current URL to last directory -1
 * *u_q*: Current URL without query string ( https://dom.com/folder/file.php )
 * *full*: Full url (as Example)
 * *fullpath*: The path (/demo/test.html?x=1)
 * *host*: Network location (x.com)
 * *query*: Query string ( query=data )
 * *lastpath*: Last directory ( folder )
 * *lasfile*: Last file of URL ( file.php )
 * *lastfile_ext*: Last file of URL without extension ( file )

