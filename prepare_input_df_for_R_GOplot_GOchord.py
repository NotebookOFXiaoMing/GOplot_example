'''
R语言的GOplot包画弦图展示GO富集分析的结果
图还挺好看的，但是准备自己的数据还相对比较麻烦
我这边写一个python脚本，希望可以让你准备数据方便一点

需要你自己准备三个数据
1、GO富集分析的结果
2、是感兴趣的Term
3、感兴趣的基因名
'''

import sys

aa = sys.argv[1:]

print(aa)

sepwhat = {'a':"\t",'b':',','d':'/'}

inputgene = aa[0]

inputterm = aa[1]

inputgoenrichresult = aa[2]

filesep = sepwhat[aa[3]]

genesep = sepwhat[aa[4]]

termcol = aa[5]

genecol = aa[6]

outputfile = aa[7]

fr = open(inputgene,'r')
genes = []
for line in fr:
    genes.append(line.strip())
print("Total",len(genes),"Genes")
print(genes)

fprocess = open(inputterm,'r')
process_list = []
for line in fprocess:
    process_list.append(line.strip())
    
print("Total",len(process_list),"Term")
print(process_list)


fr = open(inputgoenrichresult,'r')
process2gene = {}
for line in fr:
    if line.split(filesep)[int(termcol)-1] in process_list:
        process2gene[line.split(filesep)[int(termcol)-1]] = line.split(filesep)[int(genecol)-1].replace(" ","").split(genesep)
        
fw = open(outputfile,'w')
fw.write("\t")
for process in process_list:
    fw.write("%s\t"%(process))
for gene in genes:
    fw.write("\n%s\t"%(gene))
    for process in process_list:
        if gene in process2gene[process]:
            fw.write("%d\t"%(1))
        else:
            fw.write("%d\t"%(0))
fw.close()
print("------")
print("------")

print("The result was stored in",outputfile,". Then you need use R.")


