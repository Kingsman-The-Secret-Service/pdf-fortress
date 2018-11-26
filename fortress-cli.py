#!/usr/bin/python
import glob, os, sys
import time, getpass

class Util:

	# Print iterations progress
	@staticmethod
	def progressBar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
	    """
	    Call in a loop to create terminal progress bar
	    @params:
	        iteration   - Required  : current iteration (Int)
	        total       - Required  : total iterations (Int)
	        prefix      - Optional  : prefix string (Str)
	        suffix      - Optional  : suffix string (Str)
	        decimals    - Optional  : positive number of decimals in percent complete (Int)
	        bar_length  - Optional  : character length of bar (Int)
	    """
	    str_format = "{0:." + str(decimals) + "f}"  #{0:.1f}
	    percents = str_format.format(100 * (iteration / float(total)))  #{0:.1f}.format(100*(i/float(l))
	    filled_length = int(round(bar_length * iteration / float(total))) 
	    bar = '*' * filled_length + '-' * (bar_length - filled_length)

	    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

	    if iteration == total:
	        sys.stdout.write('\n')
	    sys.stdout.flush()


class Fortress:	

	def __init__(self, action, dirPath, password):

		# Local variables
		self._files = []
		self._action = action
		self._dirPath = dirPath
		self._password = password

		# Invoke Methods
		self.fetchFiles()
		self.setupDir()

		actionAttr = getattr(self, action)
		actionAttr()

		# print self._files

	def encrypt(self):
		# Progress bar 
		i = 0
		l = len(self._files)
		Util.progressBar(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)

		# Iterating over files list to decrypt
		for file in self._files:

			# Decrypting the pdf file
			cmd = "pdftk '" + file + "' output '" + self._action + "/" + file + "' user_pw " + self._password #pdftk 'filename' output 'encrypt/filename' user_pwd password
			os.system(cmd)

			# Progress bar
			i += 1
			suffix = file
			if i == l:
				suffix = 'Completed                                  '
			Util.progressBar(i, l, prefix = 'Encrypting:', suffix = suffix, bar_length = 50)

	def decrypt(self):

		# Progress bar 
		i = 0
		l = len(self._files)
		Util.progressBar(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)

		# Iterating over files list to decrypt
		for file in self._files:

			# Decrypting the pdf file
			cmd = "pdftk '" + file + "' input_pw " + self._password +" output '" + self._action + "/" + file +"'"
			os.system(cmd)

			# Progress bar
			i += 1
			suffix = file
			if i == l:
				suffix = 'Completed                                  '
			Util.progressBar(i, l, prefix = 'Decrypting:', suffix = suffix, bar_length = 50)

	def fetchFiles(self):

		# Changing the working directory
		try:
			os.chdir(self._dirPath)  #changes directory to the specified path. if directory is not mentioned , this will throw an error
			print "directory successfully changed to ", self._dirPath
		except OSError:
			print "Please enter only a valid directory with absolute or relative path"
			exit()
		# Iterating over *.pdf extension files using glob
		for file in glob.glob("*.pdf"):   #to match and collect all the .pdf files"

			# Appending glob files into list
		    self._files.append(file) #the files with filename is added to the list file[]

	def setupDir(self):

		# Checks directory exists
		if not os.path.isdir(self._action):

			# Create directory
			os.system("mkdir " + self._action)

# Need pdftk to be installed before using this code // sudo apt-get install pdftk

# Sample usage below
# Fortress("encrypt|decrypt", "path/to/folder", "password")
action = raw_input("Enter the action to be done\n'encrypt' for encryption\n'decrypt' for decryption:")
path = raw_input("Enter the absolute/relative path of directory in which the pdf files exists:")
password = getpass.getpass()
Fortress(action, path, password)
# Fortress("decrypt", "./sample", "12345")
