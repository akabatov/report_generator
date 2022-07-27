import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from . import scanner
from django.conf import settings
import os
from os import path 


def home(response):
    remove_files()
    return render(response, 'app/base.html', {})


def scan(request):
    remove_files()
    return render(request, 'app/scan.html', {})


def scanning(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        scan = scanner.Scan(uploaded_file.name, [[]])
        scan.scan_iteration()
        report = scan.getInfo_arr()
        report_for_file = scan.getInfo_arr() 
    try: 
        create_file(report_for_file,"Report.txt")
        return render(request, 'app/scanning.html', {"report":report})
    except: return 'Error While Scanning the File'


def download(request):
    file = settings.MEDIA_ROOT + '\Report.txt'
    filename = 'Report' + "1" + ".txt"
    response = StreamingHttpResponse(FileWrapper(open(file, 'rb')), content_type=mimetypes.guess_type(file)[0])
    response['Cotent-Length'] = os.path.getsize(file)
    response['Content-Disposition'] = 'Attachment; filename=%s' %filename 
    return response


def create_file(report_info, name):
    filepath = settings.MEDIA_ROOT
    try:
        with open(filepath+ '/'+ name, 'a') as fo:
            for container in report_info:
                fo.write(container)
                fo.write('\n')
        return True 
    except: return False
    

def remove_files():
    if path.exists(settings.MEDIA_ROOT + '/containers.txt'):
         os.remove(settings.MEDIA_ROOT+'\containers.txt')
    if path.exists(settings.MEDIA_ROOT + '/Report.txt'):
        os.remove(settings.MEDIA_ROOT+'\Report.txt')


def convert_to_dict(input_list):
    return_dict = {}
    arr2 = ['ID', 'SEALINE', 'START', 'END', 'START-DATE', 'END-DATE']
    length = len(input_list)
    for i in range(length):
        return_dict[i] = dict(zip(arr2, input_list[i]))
    return return_dict
