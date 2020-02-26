from pygost import gost3412
def Crypt_db(self):
	old = open('database.db','rb').read()
	new = open('encrypt.enc','wb')
	gost = gost3412.GOST3412Kuznechik(b'1'*32)
	new.write(gost.encrypt(old))
	new.close()
	