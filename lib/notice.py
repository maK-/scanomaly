from colored import fg, bg, attr
#This is a simple class to display information
class Notice:
    def __init__(self):
        self.rs = attr('reset')
        self.reg = fg(15)+'['+fg(14)+'*'+fg(15)+'] '+self.rs
        self.err = fg(15)+'['+fg(1)+'-'+fg(15)+'] '+self.rs
        self.info = fg(15)+'['+fg(2)+'+'+fg(15)+'] '+self.rs

    def errs(self,msg):
        print(self.err+msg+self.rs)

    def regs(self,msg):
        print(self.reg+msg+self.rs)
        
    def infos(self,msg):
        print(self.info+msg+self.rs)

    def splits(self):
        print(fg(8)+'--------------------------'+self.rs)

    def prog(self, msg):
        print(self.reg+msg+self.rs, end='\r', flush=True)

    def progress(self, msg, fst, snd):
        perc = "{:.1%}".format(fst/snd)
        print(self.reg+msg+fg(14)+str(perc)+self.rs, end='\r', flush=True)
