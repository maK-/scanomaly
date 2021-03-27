This directory contains all the post processing modules.
Modules you may find here
    - Generate scans based on directories or links within HTML page (crawl)
    - generate scans of endpoints with POST/GET params (into request.data)
    - if dirs like js,script etc -> brute js files in them
    - remove duplicate 403's whereby /server-status* results in same result
    - grab dirs and scan them from js files


A post module takes 3 arguments
    - requests
    - responses
    - config

returns a multi_Req list of configs for each interesting response:
i_status:   []
i_size:     []
mods:       []
flagsame:   bool
content:    bool
session:    bool
force:      bool
timeout:    int
req:        requestObject

it also returns a list to pass to default configs
