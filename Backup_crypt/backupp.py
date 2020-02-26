import posixpath
import os
import datetime
import zipfile
import yadisk
def backup_db(self):
	dt = datetime.datetime.now()
	currentdate = dt.strftime('%Y_%m_%d')
	current_date = dt.strftime('%Y_%m_%d %H-%M')
	from_dir = 'Backup'+str(currentdate)+'.zip' 
	fille = zipfile.ZipFile(from_dir , 'w')
	fille.write('encrypt.enc', compress_type=zipfile.ZIP_DEFLATED)
	fille.close()
	to_dir = '/backup'+str(current_date)
	token = yadisk.YaDisk(token="You_token")
	token.upload(str(from_dir),str(to_dir))
    


    