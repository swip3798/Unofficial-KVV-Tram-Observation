import ftplib


'''
The files have to be arrays in an array. [[dir1, target1],[dir2, target2]]. The items are all the filenames
'''

def uploadFile(url, username, passFilename, files):
	session = ftplib.FTP(url, username, open(passFilename, "r").read())
	for i in files:
		file = open(i[0], "rb")
		session.storbinary("STOR " + i[1], file)
		file.close()
	session.quit()