"""               __ _       ____
  ___ ___  _ __  / _(_) __ _|  _ \ __ _ _ __ ___  ___ _ __
 / __/ _ \| '_ \| |_| |/ _` | |_) / _` | '__/ __|/ _ | '__|
| (_| (_) | | | |  _| | (_| |  __| (_| | |  \__ |  __| |
 \___\___/|_| |_|_| |_|\__, |_|   \__,_|_|  |___/\___|_|
                       |___/
*   This class aims to parse the scanomaly configurations
*       - default.yml = main config
*       - interesting status codes -> point to individual config for each
*       - integrate the results from baseline scans
*       - Lists of requests to process further
*           o   If dirb -> 301 -> list for recursive
*           o   403 -> attempt bypasses
*           o   401 -> for brute force
"""
import yaml
class ConfigParser:
    def __init__(self, cwd, config_dir):
        cwd += '/'
        if config_dir == None:
            self.config_dir = cwd+'config/'
        else:
            self.config_dir = cwd+config_dir
        self.default_path = self.config_dir + 'default.yml'
        self.config = self.read_main()
        
        if self.config != None:
            self._200_d = self.read_yaml(self.config['200_folder'])
            self._200_e = self.read_yaml(self.config['200_endpoint'])
            self._200_p = self.read_yaml(self.config['200_params'])
            self._301 = self.read_yaml(self.config[301])
            self._302 = self.read_yaml(self.config[302])
            self._403 = self.read_yaml(self.config[403])
            self._401 = self.read_yaml(self.config[401])
            self._500 = self.read_yaml(self.config[500])

    """
    *   Read the main default config
    """
    def read_main(self):
        try:
            with open(self.default_path) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except:
            return None
    """
    *   Read passed in yaml file
    """
    def read_yaml(self, location):
        try:
            with open(self.config_dir+location) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except:
            return None

    def print_all(self):
        print('200_d: '+str(self._200_d))
        print('200_e: '+str(self._200_e))
        print('200_p: '+str(self._200_p))
        print('301: '+str(self._301))
        print('302: '+str(self._302))
        print('403: '+str(self._403))
        print('401: '+str(self._401))
        print('500: '+str(self._500))
       
