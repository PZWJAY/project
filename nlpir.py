# -*- coding: UTF-8 -*-
from __future__ import division  #使用‘/’号进行两个整数相除获得小数
__author__ = 'Peter_Howe<haobibo@gmail.com>'

'''
Python Warpper for ICTCLAS2014
Loading functions from Dynamic Link Library  directly.
'''
from ctypes import *
import math
import re

#NLPIR2014 Lib File (NLPIR64, NLPIR32, libNLPIR64.so, libNLPIR32.so),
#Change this when you are not using a Win64 environment:
libFile = './nlpir/NLPIR64.dll'

NUM = 1000 #选择的特征数
FILE_SIZE = 10000

dll =  CDLL(libFile)
def loadFun(exportName, restype, argtypes):
	global dll
	f = getattr(dll,exportName)
	f.restype = restype
	f.argtypes = argtypes
	return f

class ENCODING:
	GBK_CODE        =   0               #默认支持GBK编码
	UTF8_CODE       =   GBK_CODE+1      #UTF8编码
	BIG5_CODE       =   GBK_CODE+2      #BIG5编码
	GBK_FANTI_CODE  =   GBK_CODE+3      #GBK编码，里面包含繁体字

class POSMap:
	ICT_POS_MAP_SECOND  = 0 #计算所二级标注集
	ICT_POS_MAP_FIRST   = 1 #计算所一级标注集
	PKU_POS_MAP_SECOND  = 2 #北大二级标注集
	PKU_POS_MAP_FIRST   = 3	#北大一级标注集

POS = {
	"n": {  #1.	名词  (1个一类，7个二类，5个三类)
		"n":"名词",
		"nr":"人名",
		"nr1":"汉语姓氏",
		"nr2":"汉语名字",
		"nrj":"日语人名",
		"nrf":"音译人名",
		"ns":"地名",
		"nsf":"音译地名",
		"nt":"机构团体名",
		"nz":"其它专名",
		"nl":"名词性惯用语",
		"ng":"名词性语素"
	},
	"t": {  #2.	时间词(1个一类，1个二类)
		"t":"时间词",
		"tg":"时间词性语素"
	},
	"s": {  #3.	处所词(1个一类)
		"s":"处所词"
	},
	"f": {  #4.	方位词(1个一类)
		"f":"方位词"
	},
	"v": {  #5.	动词(1个一类，9个二类)
		"v":"动词",
		"vd":"副动词",
		"vn":"名动词",
		"vshi":"动词“是”",
		"vyou":"动词“有”",
		"vf":"趋向动词",
		"vx":"形式动词",
		"vi":"不及物动词（内动词）",
		"vl":"动词性惯用语",
		"vg":"动词性语素"
	},
	"a": {  #6.	形容词(1个一类，4个二类)
		"a":"形容词",
		"ad":"副形词",
		"an":"名形词",
		"ag":"形容词性语素",
		"al":"形容词性惯用语"
	},
	"b": {  #7.	区别词(1个一类，2个二类)
		"b":"区别词",
		"bl":"区别词性惯用语"
	},
	"z": {  #8.	状态词(1个一类)
		"z":"状态词"
	},
	"r": {  #9.	代词(1个一类，4个二类，6个三类)
		"r":"代词",
		"rr":"人称代词",
		"rz":"指示代词",
		"rzt":"时间指示代词",
		"rzs":"处所指示代词",
		"rzv":"谓词性指示代词",
		"ry":"疑问代词",
		"ryt":"时间疑问代词",
		"rys":"处所疑问代词",
		"ryv":"谓词性疑问代词",
		"rg":"代词性语素"
	},
	"m": {  #10.	数词(1个一类，1个二类)
		"m":"数词",
		"mq":"数量词"
	},
	"q": {  #11.	量词(1个一类，2个二类)
		"q":"量词",
		"qv":"动量词",
		"qt":"时量词"
	},
	"d": {  #12.	副词(1个一类)
		"d":"副词",
		"dl":"成语",
		"dg":" 副词性语素"
	},
	"p": {  #13.	介词(1个一类，2个二类)
		"p":"介词",
		"pba":"介词“把”",
		"pbei":"介词“被”"
	},
	"c": {  #14.	连词(1个一类，1个二类)
		"c":"连词",
		"cc":"并列连词"
	},
	"u": {  #15.	助词(1个一类，15个二类)
		"u":"助词",
		"uzhe":"着",
		"ule":"了 喽",
		"uguo":"过",
		"ude1":"的 底",
		"ude2":"地",
		"ude3":"得",
		"usuo":"所",
		"udeng":"等 等等 云云",
		"uyy":"一样 一般 似的 般",
		"udh":"的话",
		"uls":"来讲 来说 而言 说来",
		"uzhi":"之",
		"ulian":"连 " #（“连小学生都会”）
	},
	"e": {  #16.	叹词(1个一类)
		"e":"叹词"
	},
	"y": {  #17.	语气词(1个一类)
		"y":"语气词(delete yg)"
	},
	"o": {  #18.	拟声词(1个一类)
		"o":"拟声词"
	},
	"h": {  #19.	前缀(1个一类)
		"h":"前缀"
	},
	"k": {  #20.	后缀(1个一类)
		"k":"后缀"
	},
	"x": {  #21.	字符串(1个一类，2个二类)
		"x":"字符串",
		"xe":"Email字符串",
		"xs":"微博会话分隔符",
		"xx":"非语素字",
		"xu":"网址URL",
		"xm":"表情"
	},
	"w":{   #22.	标点符号(1个一类，16个二类)
		"w":"标点符号",
		"wkz":"左括号", 	#（ 〔  ［  ｛  《 【  〖 〈   半角：( [ { <
		"wky":"右括号", 	#） 〕  ］ ｝ 》  】 〗 〉 半角： ) ] { >
		"wyz":"全角左引号", 	#“ ‘ 『
		"wyy":"全角右引号", 	#” ’ 』
		"wj":"全角句号",	#。
		"ww":"问号",	#全角：？ 半角：?
		"wt":"叹号",	#全角：！ 半角：!
		"wd":"逗号",	#全角：， 半角：,
		"wf":"分号",	#全角：； 半角： ;
		"wn":"顿号",	#全角：、
		"wm":"冒号",	#全角：： 半角： :
		"ws":"省略号",	#全角：……  …
		"wp":"破折号",	#全角：——   －－   ——－   半角：---  ----
		"wb":"百分号千分号",	#全角：％ ‰   半角：%
		"wh":"单位符号"	#全角：￥ ＄ ￡  °  ℃  半角：$
	}
}

class SegAtom(Structure):
	_fields_ = [("start", c_int32), ("length", c_int32),
		("sPOS", c_char * 40),      ("iPOS", c_int32),
		("word_ID", c_int32),       ("word_type", c_int32), ("weight", c_int32)
	]

def translatePOS(sPOS):
	global POS
	if sPOS=='url': sPOS = 'xu'
	c = sPOS[0]
	return POS[c][sPOS]

Init = loadFun('NLPIR_Init',c_int, [c_char_p, c_int, c_char_p])
Exit = loadFun('NLPIR_Exit',c_bool, None)
ParagraphProcess = loadFun('NLPIR_ParagraphProcess',c_char_p, [c_char_p, c_int])
ParagraphProcessA = loadFun('NLPIR_ParagraphProcessA',POINTER(SegAtom), [c_char_p, c_void_p, c_bool])
#ParagraphProcessAW = loadFun('NLPIR_ParagraphProcessAW',None, [c_int, POINTER(SegAtom)])
FileProcess = loadFun('NLPIR_FileProcess',c_double, [c_char_p, c_char_p, c_int])
ImportUserDict = loadFun('NLPIR_ImportUserDict',c_uint, [c_char_p])
AddUserWord = loadFun('NLPIR_AddUserWord', c_int, [c_char_p])
SaveTheUsrDic = loadFun('NLPIR_SaveTheUsrDic', c_int, None)
DelUsrWord = loadFun('NLPIR_DelUsrWord',c_int, [c_char_p])
GetUniProb = loadFun('NLPIR_GetUniProb', c_double, [c_char_p])
IsWord = loadFun('NLPIR_IsWord',c_bool, [c_char_p])
GetKeyWords = loadFun('NLPIR_GetKeyWords',c_char_p, [c_char_p, c_int, c_bool])
GetFileKeyWords = loadFun('NLPIR_GetNewWords',c_char_p, [c_char_p, c_int, c_bool])
GetNewWords = loadFun('NLPIR_GetNewWords', c_char_p, [c_char_p, c_int, c_bool])
GetFileNewWords = loadFun('NLPIR_GetFileNewWords',c_char_p, [c_char_p, c_int, c_bool])
FingerPrint = loadFun('NLPIR_FingerPrint',c_ulong, [c_char_p])
SetPOSmap = loadFun('NLPIR_SetPOSmap',c_int, [c_int])
#New Word Identification
NWI_Start = loadFun('NLPIR_NWI_Start', c_bool, None)
NWI_AddFile = loadFun('NLPIR_NWI_AddFile',c_bool, [c_char_p])
NWI_AddMem = loadFun('NLPIR_NWI_AddMem',c_bool, [c_char_p])
NWI_Complete = loadFun('NLPIR_NWI_Complete', c_bool, None)
NWI_GetResult = loadFun('NLPIR_NWI_GetResult',c_char_p, [c_int])
NWI_Result2UserDict = loadFun('NLPIR_NWI_Result2UserDict',c_uint, None)

if not Init(b'',ENCODING.UTF8_CODE,b''):
	print("Initialization failed!")
	exit(-111111)

'''
if not SetPOSmap(3): #POSMap.ICT_POS_MAP_SECOND
	print("Setting POS Map failed!")
	exit(-22222)
'''

def seg(paragraph):
	result = ParagraphProcess(paragraph, c_int(1))
	atoms = [i.strip().split('/') for i in result.split(' ') if len(i)>=1 and i[0]!=' ']
	atoms = [(a[0],a[1]) for a in atoms if len(a[0])>0]
	return atoms

def segment(paragraph):
	count = c_int32()
	result = ParagraphProcessA(paragraph, byref(count),c_bool(True))
	count = count.value
	atoms = cast(result, POINTER(SegAtom))
	return [atoms[i] for i in range(0,count)]

def Seg(paragraph):
	atoms = segment(paragraph)
	for a in atoms:
		if len(a.sPOS) < 1: continue
		i = paragraph[a.start: a.start + a.length]#.decode('utf-8')#.encode('ascii')
		yield (i.decode('UTF8'), a.sPOS.decode('UTF8'))

def calIG(word_ls,word_dic1,word_dic2,num_pos,num_neg,Entropy,whole_file): #计算IG
	for word in word_dic1:
		if word in word_ls:
			continue
		num2 = 0
		if word in word_dic2:
			num2= word_dic2[word]
		num1 = word_dic1[word]
		num3 = num_pos - num1
		num4 = num_neg - num2
		occur_file = num1 + num2
		inoccur_file = num3 + num4
		freq1 = num1 / occur_file
		freq2 = num2 / occur_file
		freq3 = num3 / inoccur_file
		freq4 = num4 / inoccur_file
		if freq1 == 0:
			part1 = 0
		else:
			part1 = freq1 * math.log(freq1,2)
		if freq2 == 0:
			part2 = 0
		else:
			part2 = freq2 * math.log(freq2, 2)
		Entropy0 = part1 + part2
		if freq3 == 0:
			part3 = 0
		else:
			part3 = freq3 * math.log(freq3,2)
		if freq4 == 0:
			part4 = 0
		else:
			part4 = freq4 * math.log(freq4,2)
		Entropy1 = part3 + part4
		InfoGain = Entropy + (occur_file / whole_file) * Entropy0 + (inoccur_file / whole_file) * Entropy1
		word_ls[word] = InfoGain
	return word_ls

def saveFile(filename,src):
	file = open(filename, 'w', encoding='UTF-8')
	for rcd in src:
		if isinstance(rcd,dict):
			if len(rcd) == 0:
				continue
			for item in rcd:
				file.write(item)
				file.write(' ')
				file.write(str(rcd[item]))
				file.write(' ')
			file.write('\n')
		elif isinstance(rcd,str):
			file.write(rcd)
			file.write(' ')
	file.close()

def cal_tf_idf(file,num,chac,word):
	tf = []
	for ps in file:
		dic = {}
		for c in ps:
			if c in chac:
				dic[c] = ps[c] * math.log((num / (word[c] + 1)), 2)  # 计算TF-IDF
		tf.append(dic)
	return tf

#def Word_process(unprocess_path0,unprocess_path1):
if __name__=="__main__":
	stopwords = []
	word_pos = {} #统计正文本中词以及出现的次数
	word_neg = {} #统计负文本中词以及出现的次数
	file_pos = [] #正文本特征集及权重
	file_neg = [] #负文本特征集及权重
	file_test_pos = []
	file_test_neg = []
	word_pos_test = {}
	word_neg_test = {}
	#读入停用词列表
	fs = open('stopwords.txt',encoding='UTF-8')
	line = fs.readline()
	while line:
		stopwords.append(line.replace('\n',''))
		line = fs.readline()
	fs.close()

	#读取文本并对文本进行分词、去停用词、统计词频率
	filePath = 'all.txt'
	file = open(filePath,encoding='UTF-8')
	lines = file.readlines()
	num_pos = 0
	num_neg = 0
	num_test_pos = 0
	num_test_neg = 0
	tmp_pos_file = []
	tmp_neg_file = []
	tmp_pos_num = 0
	tmp_neg_num = 0
	tmp_word_pos = {}
	tmp_word_neg = {}
	for line in lines:
		if len(tmp_pos_file) >= FILE_SIZE and len(tmp_neg_file) >= FILE_SIZE and num_pos == 0:
			file_pos = tmp_pos_file.copy()
			file_neg = tmp_neg_file.copy()
			num_pos = tmp_pos_num
			num_neg = tmp_neg_num
			word_pos = tmp_word_pos.copy()
			word_neg = tmp_word_neg.copy()
			tmp_pos_file = []
			tmp_neg_file = []
			tmp_pos_num = 0
			tmp_neg_num = 0
			tmp_word_pos = {}
			tmp_word_neg = {}
		elif len(tmp_pos_file) >= FILE_SIZE/2 and len(tmp_neg_file) >= FILE_SIZE/2 and num_pos != 0:
			file_test_pos = tmp_pos_file.copy()
			file_test_neg = tmp_neg_file.copy()
			num_test_pos = tmp_pos_num
			num_test_neg = tmp_neg_num
			word_pos_test = tmp_word_pos.copy()
			word_neg_test = tmp_word_neg.copy()
			break
		word = {}
		ln = set()
		var = line.split(' ')
		p = var[1].replace('\n','')
		print(p)
		p = p.encode('UTF8')
		try:
			for t in Seg(p):
				if re.match(r'\xe2\x80\x8b',t[0]):
					continue
				if t[0] not in stopwords and t[1] not in ['xu','xe']:
					if t[0] in word:
						word[t[0]] += 1
					else:
						word[t[0]] = 1
					if t[0] in ln:
						continue
					ln.add(t[0])
					if var[0] == '0':#positive file
						tmp_pos_num += 1
						if t[0] in tmp_word_pos:
							tmp_word_pos[t[0]] += 1
						else:
							tmp_word_pos[t[0]] = 1
					else :
						tmp_neg_num += 1
						if t[0] in tmp_word_neg:
							tmp_word_neg[t[0]] += 1
						else:
							tmp_word_neg[t[0]] = 1
		except:
			continue
		for w in word:
			word[w] = word[w] / len(word)
		if var[0] == '0':
			tmp_pos_file.append(word)
		else:
			tmp_neg_file.append(word)
	file.close()
	whole_file = num_pos + num_neg
	#计算信息熵
	freq_pos = num_pos / whole_file
	freq_neg = num_neg / whole_file
	Entropy = -(freq_pos * math.log(freq_pos,2) + freq_neg * math.log(freq_neg,2))
	#print Entropy

	#计算每个词的信息增益
	word_ls = {}
	chac_pos = []
	chac_neg = []
	word_ls = calIG(word_ls,word_pos,word_neg,num_pos,num_neg,Entropy,whole_file)
	word_setpos = sorted(word_ls.items(),key=lambda item:item[1],reverse=True)
	cnt = 0
	while cnt < NUM:
		chac_pos.append(word_setpos[cnt][0])
		cnt += 1

	word_ln = {}
	word_ln = calIG(word_ln,word_neg,word_pos,num_neg,num_pos,Entropy,whole_file)
	word_setneg = sorted(word_ln.items(),key=lambda item:item[1],reverse=True)
	cnt = 0
	while cnt < NUM:
		chac_neg.append(word_setneg[cnt][0])
		cnt += 1

	chac_set = set(chac_pos) | set(chac_neg)

	tf_pos = cal_tf_idf(file_pos,num_pos,chac_pos,word_pos)
	tf_neg = cal_tf_idf(file_neg,num_neg,chac_neg,word_neg)
	tf_pos_test = cal_tf_idf(file_test_pos,num_test_pos,chac_pos,word_pos_test)
	tf_neg_test = cal_tf_idf(file_test_neg,num_test_neg,chac_neg,word_neg_test)
	print(len(tf_pos))
	print(len(tf_neg))
	print(len(tf_pos_test))
	print(len(tf_neg_test))
	saveFile('posFile.txt',tf_pos)
	saveFile('negFile.txt',tf_neg)
	saveFile('chacSet.txt',chac_set)
	saveFile('posFileTest.txt',tf_pos_test)
	saveFile('negFileTest.txt',tf_neg_test)
	#return NUM,chac_pos,chac_neg,tf_pos,tf_neg
