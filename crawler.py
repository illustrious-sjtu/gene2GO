import urllib.request
from bs4 import  BeautifulSoup
from http import cookiejar
import os, sys, os.path
import time, socket

def crawl(gene):
    try:
        response = urllib.request.urlopen("http://www.ncbi.nlm.nih.gov/gene/?term="+gene, timeout=20)
        content = response.read()
    except:
        print("Failure in: ", gene)
        return []
    soup = BeautifulSoup(content)
    table = soup.find('div',{'class':"gene-ontology infosec"})
    if table == None:
        return []
    hrefs = table.findAll('a')
    gos = []
    for i in hrefs:
        href = i.get('href','')
        if href[-10:-7] == "GO:" and (href[-7:] not in gos):
            gos.append(href[-7:])
    return gos

socket.setdefaulttimeout(20)
file = open("genes_list.txt")
lines = file.readlines()
file.close()

dict = {}
genes = []
for line in lines:
    gene = line[:-1]
    print(gene)
    genes.append(gene)
    dict[gene] = crawl(gene)

f = open("gene2GO.txt",'w')
for gene in genes:
    f.write(gene+'\t')
    for go in dict[gene]:
        f.write(go)
    f.write('\n')
f.close()
