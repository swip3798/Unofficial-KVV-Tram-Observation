import ftplib


session = ftplib.FTP('URL','USERNAME',input("Type in your password: "))
file = open('map.html','rb')                  # file to send
session.storbinary('STOR KVV/map.html', file)     # send the file
file.close()                                    # close file and FTP
session.quit()
