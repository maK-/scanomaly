# To-do

## Develop and incorporate following functionality into scanomaly
	
	1. ######import requests from file functionality (**-r** *like sqlmap*)
	2. ######Finish live scan decision engine (identfiy if WAF kicks in during scanning etc)
	3. Implement post and pre processing for scans!
	   ######- post: decision trees filtering (*per url statusx & sizex logic*)
	   ######- post: filter by content or unique responses
		- post: remove duplicate entries
		- post: extract files/directories/hosts/js/paths from results
		- pre: url encode or base64 encode payloads for scanomaly primary modules
        - pre: smart things to ignore (we have full baseline requests to work with)
	4. ######yml configurations for scans - auto generation and automation
	   ######- launch scans from yml configs
	   ######- queing/automation to run all scans sequentially from a config folder
	   ######- generate configs to run from results of a scan (recursion solution)
	5. ######For recursive functionality do things like
	   ######- For 401 status codes -> Try request method bypasses & brute force with common user/passes
	   ######- For 403 status codes -> attempt bypasses and X-Forwarded-For tricks etc
	   ######- For 301 status codes -> perform subdirectory scans (recursive)
	6. ######db column to store response headers
	7. ######Save to disk while running after every x requests to avoid losing progress (examine feasibility)
	8. Further tidying of flags and codebase, Simplify and maximum flexibility where possible
	9. Finish writing proposed modules/pre/post 
	10. ######Full scan mode - context aware crawl and scan
	11. Documentation and high level design overview


    
    Noteworthy reminders:
    ---------------------
    Need to tidy up the main scanomaly.py / cleaner code etc 
    When recursive scanning -> Need a way to avoid duplicates and scanning the same endpoints more than once.
    

