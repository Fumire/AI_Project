import time
import gtts
import konlpy.tag
import pymysql

kkma = konlpy.tag.Kkma()
print(kkma.pos(input("Enter: "), join=True))
