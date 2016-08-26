from .models import FASTA
import requests
import json
'''import shutil
from myproject.settings import MEDIA_ROOT
import os
from django.utils import timezone
from datetime import datetime, timedelta'''

def extract_FASTA_Seq(str_fasta):
    f = 0
    str_fasta += '>'
    FASTA_list = []
    crudeFASTA = ""
    for s in str_fasta:
        if s == '>':
            f = 1
            if not crudeFASTA == '':
                FASTA_list.append(refineFASTA_seq(crudeFASTA))
            crudeFASTA = '>'
        elif f == 0:
            continue
        else:
            crudeFASTA += s
    return FASTA_list

def refineFASTA_seq(crude):
    crude.strip()
    f = 0
    hd = ""
    seq = ""
    for s in crude:
        if s == ',':
            s =  ' '
        if s == '\n' and f == 0:
            f = 1
            continue
        if f == 0:
            if s == '\t':
                s = '   '
            hd += s
        else:
            if (s+' ').strip() == '':
                continue
            s = s.upper()
            t =['A','S','D','F','G','H','K','L','Q','W','E','R','T','Y','I','P','C','V','N','M']
            if s in t:
                seq += s
            else:
                seq = 'invalid'
                return FASTA(header=hd, sequence=seq, ans=0)
    return FASTA(header=hd.strip(), sequence=seq.strip(), ans=0, address = "")

def clear_invalids(c_list):
    r=[]
    for i in c_list:
        if i.sequence != 'invalid':
            r.append(i)
    return r

def reading(s):
    r=['','','','']
    b=0
    for i in s:
        if i=='\t':
            b+=1
        else:
            r[b]+=i
    return r   

def purge_fasta(t,a):
    r = []
    for i in a:
        if i.ans >= t:
            r.append(i)
    return r

def getIP(str):
    p = json.loads(str)
    return p['countryCode'],p['org']
    
def uniprot(st):
    st +=','
    uid = ''
    fasta = ''
    flag = 1
    for s in st:
        if (s+' ').strip() == '':
            continue
        if s == ',':
            re = requests.get(str("http://www.uniprot.org/uniprot/" + uid + ".fasta"))
            if (re.status_code == 200 ):
                re.text 
                fasta += re.text 
                  
            else:
                fasta += ( '>' + uid + '\n' + 'xxxx')
            uid = ""
        else :
            uid += s
    return str(fasta)
        
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip        

def genBank(st):
    st +=','
    uid = ''
    fasta = ''
    flag = 1
    for s in st:
        if (s+' ').strip() == '':
            continue
        if s == ',':
            re = requests.get(str("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=" + uid + "&rettype=fasta&retmode=text"))
            if (re.status_code == 200 ):
                re.text 
                fasta += re.text 
                  
            else:
                fasta += ( '>' + uid + '\n' + 'xxxx')
            uid = ""
        else :
            uid += s
    print fasta
    return str(fasta)

