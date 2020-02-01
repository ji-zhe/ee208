import jieba
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

for root, di, filenames in os.walk('plaintext'):
	for filename in filenames: 
		f = open('plaintext/'+filename)
		content = f.read()
		l = jieba.cut(content)
		content = ' '.join(l)
		g = open('cuttext/'+filename, 'w')
		g.write(content)
		print filename
		g.close()
		f.close()

