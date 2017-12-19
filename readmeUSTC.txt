几个txt文件说明：
all.txt:中文语料库的所有语料数据；
chacSet.txt:所选出来的最终特征（正文本和负文本选出来的特征的并集）；
negFile.txt:用选出来的特征重新处理负文本的文本，每个文本为一行，由（词：权重）的形式表示；
posFile.txt:类似negFile.txt，只不过是正文本的；
stopword.txt:停用词表；
fildf.csv:将所有文本加上其类别组成的DataFrame；

几个py文件说明：
main.py:主要的代码文件(模型），但模型还没写；
nlpir.py:中科院nlpir分词的文件，里面是我增加了一部分内容的代码，增加了计算IG、TF-IDF等