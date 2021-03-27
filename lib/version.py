from colored import fg, bg, attr
from lib.fileOp import FileOp

class VersionInfo:

    def __init__(self, cwd):
        self.rs = attr('reset')
        self.logo = FileOp(cwd+'/img/scanomaly.ico').reader()
        self.author = fg(8)+'Author: '+self.rs
        self.author += "© "+fg(2)+"Ciar"+fg(15)+"án McN"+fg(3)
        self.author += 'ally'+self.rs+" ~ "+fg(12)+'www.securit.ie'+self.rs
        self.software = fg(8)+'Software: '+self.rs
        self.software += 'https://github.com/mak-/scanomaly.git'
        self.software += self.rs
        self.breaker = fg(8)+'================================================'
        self.breaker += self.rs

    
    def logoshow(self):
        for i in self.logo:
            print(i)

    def show(self):
        self.logoshow()
        print(self.author)
        print(self.software)
        print(self.breaker)
