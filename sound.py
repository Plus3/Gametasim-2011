import subprocess

class Sound():
	def __init__(self, name, File):
		self.name = name
		self.file = File
		self.process = None
	
	def play(self):
		self.process = subprocess.Popen(["afplay", self.file])
	
	def stop(self):
		if self.process != None:
			try: self.process.kill()
			except: pass