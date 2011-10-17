import subprocess

class Sound():
    def __init__(self, name, File, use=False):
        self.name = name
        self.file = File
        self.process = None
        self.use = use
    
    def play(self):
        if self.use is True:
            try: self.process = subprocess.Popen(["afplay", self.file])
            except Exception, e: print e
            
    def stop(self):
        if self.use is True:
            if self.process != None:
                try: self.process.kill()
                except: pass
