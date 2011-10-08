import subprocess

class Sound():
    def __init__(self, name, File):
        self.name = name
        self.file = File
        self.process = None
    
    def play(self):
        try: self.process = subprocess.Popen(["afplay", self.file])
        except Exception, e: print e
            
    def stop(self):
        if self.process != None:
            try: self.process.kill()
            except: pass