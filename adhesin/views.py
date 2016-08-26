from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import date, timedelta
from .adhesinprediction import PRED_CLASS
from .models import *
from .forms import UploadFileForm
from .fasta import extract_FASTA_Seq, clear_invalids, reading, purge_fasta, getIP, uniprot, genBank, get_client_ip
from .mail import sendMail
import os
from myproject.settings import MEDIA_ROOT
from django.http import Http404
from django.core.mail import EmailMessage
import requests
from django.http import StreamingHttpResponse
#import shutil


def index(request):

    form = UploadFileForm()
    return render(request, 'adhesin/index.html', {"form": form})
    
def inText(request):

    if 'seq' in request.POST and 'algo' in request.POST and 'thr' in request.POST and 'IP' in request.POST and 'format' in request.POST:
        
        id2 = len(ProteinData.objects.all())*100 + timezone.now().day
        p = ProteinData(pk = id2, pub_date=strftime('%m_%d_'), algo=request.POST['algo'], inFormat = request.POST['format'])
        add = os.path.join(MEDIA_ROOT, ("output/TextBoxOutput/"))
        p.save()
        if len(ProteinData.objects.filter(pub_date=strftime('%m_%d_'))) == 1:
            yesterday = date.today() - timedelta(2)
            del_date = yesterday.strftime('%m_%d_')
            for obj in ProteinData.objects.filter(pub_date=del_date):
                try:
                   os.remove(os.path.join(add,str(del_date+p.pk+".txt")))
                except:
                   continue
            ProteinData.objects.filter(pub_date=del_date).delete()
        filename = p.pub_date + str(p.pk)
        try:
            cd,og = getIP(request.POST['IP'])
        except:
            try:
                ip = get_client_ip(request)
                re = requests.get('http://ip-api.com/json/'+ip)
                if(re.status_code ==200):
                    cd,og = getIP(re.text)  
                else:
                    fun = 2/0
            except:
                cd="IN"
                og= 'unknown'
        mail = user_details(email = request.POST["E-mail"], country_cd =cd, address = 't'+ str(p.pk), mode = 't', org = og ) 
        mail.save()
        if (request.POST['format'] == 'F'):
            fasta = request.POST['seq']
        elif (request.POST['format'] == 'G'):
            fasta = genBank(request.POST['seq'])
        elif (request.POST['format'] == 'U'):
            fasta = uniprot(request.POST['seq'])
        else :
            raise Http404("Error: Unexpected Request")

        if (not (fasta[0])== '>') and (request.POST['format'] == 'F') :
            raise Http404("Error:You submitted invalid data.")
        err_FASTA = []
        a = extract_FASTA_Seq(fasta)
        for i in a:
            if i.sequence == 'invalid':
                err_FASTA.append(i)
        a = clear_invalids(a)
        if len(a) > 0:
            predicted, probability = PRED_CLASS().main_process( a, request.POST['algo'])
        c = 0
        for i in a:
            i.ans = probability[c]
            i.cls = predicted[c]
            c+=1
        a = sorted(a, key=lambda FASTA: FASTA.ans, reverse=True)
        c = 0
        with open(os.path.join(add, filename)+'.txt', 'wb') as fh:
            fh.writelines("Rank"+".,"+"Header"+","+"Prediction"+','+"Adhesin Probability"+"\n")
            for i in a:
                c += 1
                i.rank = c
                i.save()
                mtxt = ( str(i.rank) + str(",")+str(i.header) + str(","))
                if i.cls == 1:
                    mtxt += ('Adhesin' +str(",")+str(i.ans)+"\n" )
                else:
                    mtxt += ('Non-Adhesin' +str(",")+str(i.ans)+"\n" )
                fh.writelines(mtxt)  
        a = purge_fasta(float(request.POST['thr']),a)
        try :
            if mail.email != "" :
                sendMail(mail.email , filename, add)
                email_result = "You were sent a mail at " + mail.email + " with results as attachments."
            else :
                email_result = ""    
        except :        
                email_result = "We falied to send mail to " + mail.email 
                
        context = {'results': a, 'algo': request.POST['algo'], 'total': 10, 'perPage': 11, 'pageNo': 1, 'format' : request.POST['format'],
                   'err_no': len(err_FASTA), 'err': err_FASTA,'thr' : request.POST['thr'],'err': err_FASTA,
                   'base': '/media/output/TextBoxOutput/', 'fname': str(filename), 'email_result' : email_result }
        return render(request, 'adhesin/result.html', context)
    else:
        raise Http404("Error: Unexpected Request")


def wait(request):

    if request.method == 'POST' and 'thr' in request.POST and 'format' in request.POST :
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            add = (len(FileData.objects.all())+1)*100 + timezone.now().day
            p = FileData(address=add, pub_date=strftime('%m_%d_'), algo=request.POST['algo'], perPage=10, upFile=request.FILES['upFile'], inFormat = request.POST['format'])
            p.save()
            filename = p.pub_date + str(p.address)
            try:
                cd,og = getIP(request.POST['IP'])
            except:
                try:
                    ip = get_client_ip(request)
                    re = requests.get('http://ip-api.com/json/'+ip)
                    if(re.status_code ==200):
                        cd,og = getIP(re.text)  
                    else:
                        fun = 2/0
                except:
                    cd="IN"
                    og= 'unknown'
            mail = user_details(email = request.POST["E-mail"], country_cd =cd, address = 'f' + str(p.pk), mode = 'f', org = og ) 
            mail.save()
            a = os.path.join(MEDIA_ROOT, 'fileUpload/')
            pathb = os.path.join(MEDIA_ROOT, 'output/FileOutput/')
            if len(FileData.objects.filter(pub_date=strftime('%m_%d_'))) == 1:
                yesterday = date.today() - timedelta(2)
                del_date = yesterday.strftime('%m_%d_')
                for obj in ProteinData.objects.filter(pub_date=del_date):
                    try:
                        os.remove(os.path.join(a,str(del_date+p.pk+".txt")))
                        os.remove(os.path.join(pathb,str(del_date+p.pk+".txt")))
                    except:
                        continue
                ProteinData.objects.filter(pub_date=del_date).delete()
            with open(os.path.join(a, filename), 'r') as dfh:
                pline = dfh.readline()
                pline += dfh.read()
            if (request.POST['format'] == 'F'):
                fasta = pline
            elif (request.POST['format'] == 'G'):
                fasta = genBank(pline)
            elif (request.POST['format'] == 'U'):
                fasta = uniprot(pline)
            else :
                raise Http404("Error: Unexpected Request")
            a = extract_FASTA_Seq(fasta)
            err_FASTA = []
            for i in a:
                if i.sequence == 'invalid':
                    err_FASTA.append(i)
                else:
                    i.address=filename
            a = clear_invalids(a)
            p.total = len(a)
            for i in a:
                i.save() 
            p.save()     
            context = { 'total': p.total, 'perPage': p.perPage,
                        'thr' : request.POST['thr'],'err_no': len(err_FASTA), 'err': err_FASTA, 'frmt' : p.inFormat,
                         'email' : request.POST["E-mail"],'fname': filename, 'key': p.pk, 'time': round((p.total*12.0)/60,2)}
            return render(request, 'adhesin/wait.html', context)
        raise Http404("Error: Invalid form Data")
    raise Http404("Error: Unexpected Request")              


def inFile(request):

        if request.method == 'POST' and 'value' in request.POST and 'thr' in request.POST and 'fname' in request.POST and 'perPage' in request.POST:
            p = get_object_or_404(FileData, pk=int(request.POST['value']))
            mail = get_object_or_404(user_details, address = ("f" + str(p.pk)))
            p.perPage = int(request.POST['perPage'])
            p.save()
            filename = request.POST['fname']
            a = FASTA.objects.filter(address = filename)
            pathb = os.path.join(MEDIA_ROOT, 'output/FileOutput/')
            if (len( FASTA.objects.filter(address = filename).filter(rank = 0)) == 0):
                cheatPage(request, a, p)    
            predicted, probability = PRED_CLASS().main_process(a, p.algo)
            c = 0
            for i in a:
               i.ans = probability[c]
               i.cls = predicted[c]
               c+=1
            a = sorted(a, key=lambda FASTA: FASTA.ans, reverse=True)
            with open(os.path.join(pathb, filename)+".txt", 'w') as fh:
                c = 0
                fh.writelines("Rank"+".,"+"Header"+","+"Prediction"+','+"Adhesin Probability"+"\n")
                for i in a:
                    c += 1
                    i.rank = c
                    i.save()
                    mtxt = ( str(i.rank) + str(",")+str(i.header) + str(","))
                    if i.cls == 1:
                        mtxt += ('Adhesin' +str(",")+str(i.ans)+"\n" )
                    else:
                        mtxt += ('Non-Adhesin' +str(",")+str(i.ans)+"\n" )
                    fh.writelines(mtxt)  
            b = purge_fasta(float(request.POST['thr']),a)
            p.thr_total = len(b)
            results = []
            next = 2
            totp = 0
            if p.thr_total <= p.perPage:
                for i in range(0, p.thr_total):
                     results.append(a[i])
                next = 0
            else:
                for i in range(0, p.perPage):
                    results.append(a[i])
            totp = p.thr_total/p.perPage 
            if p.thr_total%p.perPage:
                totp += 1       
            try :
                if mail.email != "" :
                    sendMail(mail.email , filename, pathb)
                    email_result = "You were sent a mail at " + mail.email + " with results as attachments." 
                else :
                    email_result = ""   
            except :        
                email_result = "We falied to send mail to " + mail.email
            p.save()   
            context = {'results': results, 'algo':p.algo, 'total': p.thr_total, 'perPage': p.perPage, 'totp' : totp,
                       'pageNo': 1, 'next': next, 'prev': 0, 'thr' : request.POST['thr'],
                       'base': '/media/output/FileOutput/', 'pub_date': p.pub_date, 'fname': filename, 'key': p.pk,
                        'email_result' : email_result}
            return render(request, 'adhesin/resultFile.html', context)
        raise Http404("Error: Unexpected Request")


def cheatPage(request, a, p):
        page = 1
        s = 0
        a = sorted(a, key=lambda FASTA: FASTA.ans, reverse=True)       
        if page >= 1 :
                t = int(p.thr_total) - int(p.perPage)*(page-1)
                results = []
                if t < p.perPage:
                    flag = t
                else:
                    flag = p.perPage       
                results.append(a[p.perPage*(page-1):flag])
                if (int(p.thr_total) > int(p.perPage)*int(page)):
                    d = (page + 1)
                else:
                    d = 0
                totp = p.thr_total/p.perPage 
                if  p.thr_total%p.perPage:
                    totp += 1          
                context = {'results': results, 'algo': p.algo, 'total':p.thr_total, 'perPage': p.perPage, 'pageNo': page,'next': d,'prev': page-1, 'totp' : totp,
                           'base': '/media/output/FileOutput/','thr' : request.POST['thr'], 'pub_date': p.pub_date, 'fname': request.POST['fname'], 'key': p.pk}
                return render(request, 'adhesin/resultFile.html', context)
        else:
            raise Http404("Invalid Page Number <!>:" + str(page))
    
def nPage(request):
    if request.method == 'POST' and 'value' in request.POST and 'pageNo' in request.POST and 'thr' in request.POST:
        page = int(request.POST['pageNo'].strip())
       
        p = get_object_or_404(FileData, pk=int(request.POST['value']))
        s = 0
        filename = p.pub_date + str(p.address)
        b = FASTA.objects.filter(address = filename)
        a = sorted(b, key=lambda FASTA: FASTA.ans, reverse=True)      
        if page >= 1 and p.thr_total > p.perPage*(page-1):
                t = p.thr_total - p.perPage*(page-1)
                results = []
                if t < p.perPage:
                    flag = t
                else:
                    flag = p.perPage 
                for i in range((p.perPage*(page-1)),(p.perPage*(page-1)+flag)):    
                    results.append(a[i])
                if (int(p.thr_total) > int(p.perPage)*int(page)):
                    d = (page + 1)
                else:
                    d = 0
                totp = p.thr_total/p.perPage 
                if  p.thr_total%p.perPage:
                    totp += 1          
                context = {'results': results, 'algo': p.algo, 'total':p.thr_total, 'perPage': p.perPage, 'pageNo': page,'next': d,'prev': page-1, 'totp' : totp,
                           'base': '/media/output/FileOutput/','thr' : request.POST['thr'], 'pub_date': p.pub_date, 'fname': filename, 'key': p.pk}
                return render(request, 'adhesin/resultFile.html', context)
        else:
            raise Http404("Invalid Page Number <!>:" + str(page))
    raise Http404("Error: Unexpected Request")   
    


def scrambler(s):
    sr = str(s)
    f = ""
    k = 0
    m = [1,9,5,3,7,0,2,4]
    for i in sr:
        b = m[k%8] + int(i)
        f += b
        k +=1
    return f
    
     
def descrambler(s):
    sr = str(s)
    f = ""
    k = 0
    m = [1,9,5,3,7,0,2,4]
    for i in sr:
        b =  int(i) - m[k%8]
        f += str(b)
        k +=1
    return f
    
    
    
    
    
    
    
    
    
    
    
    
    
