from django.shortcuts import render
from django.http import HttpResponse
from .models import UploadFile
from .forms import UploadCdrForm
from PDFNetPython3 import *
import cloudconvert
from PyPDF2 import PdfFileReader

cloudconvert.configure(api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiOGEwOWM5MTg1NGVlYjU4OTE2OTMyNDgwNDc5N2M0ZTJmNDk3NzcwMDA0M2EyOGQ4NzliY2JiYWY5YTgyN2VmMDUzZDBmZmI3NTQxMjg5ZTkiLCJpYXQiOjE2MTkxNTI2NDkuNjczNDE5LCJuYmYiOjE2MTkxNTI2NDkuNjczNDIyLCJleHAiOjQ3NzQ4MjYyNDkuNjM0MjU3LCJzdWIiOiI1MDU2ODI0NCIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIl19.OJnAE2i489NfXYjIhjHJ7Xlwz01AlZBBBz2cQOsxHXQHfHr2PO97FDLSzFjWDqBIEJOTBglNpK3jt6O6tN_jsjMdnI11cETlMQfnY3l4Eyc0JYcO4cH0MYi1OLVUe-qKNJ56QC_XVp5csbJEnqFxGNyAnY5ZsPtRD4P_e3i6a3ehmJIfHAypcXuvPtXei2FCrswsDaBmK4rDqEihxBbeG9qg31zneBApFfSGOPfbsFxg-6rZKWvcRnEA-CA8Ks0lIojtDouCjhnRly4X81LaRNSlNeiDZcLSU0TyBW783gNLfp8thLP9KxAEgOC_LIuwprHc63-m4WaOab5jmQUrHpXEnGlhGpuNsB7G5oKl23tsCKgJO0AtoeWgyL4YjB9QruFKu1DlL-e3A5Dzry1Zwrn9B4Sl_rYbg2FxwXV46IrTP41nL-sE1n7FSato3O2fM23zhkVEtKFyTck7Hwoi1ym1-ehR5RbUdr8zzkMaxUGxaxH-h3newzOVA7VEUKntM4CYKFUIwU1PNLcdGgdmWiLsBMbk8lIFmq_EBuGfU5sDgq3efqqAseAs9D0RnX5JRqVKu4FmjafPPZfFylnjOd0kOROLp6Fe0OUIF-nHv0p4-qT6-tYxgMQeM32CW-aarOYy8hmYSQcU7s_NpBjyK-JWG6ZE8fEi6aieMn799xM', sandbox = False)

# Create your views here.
def index(request):
    form = UploadCdrForm()

    if request.method == 'POST':
        form = UploadCdrForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    context = {
        'form' : form
    }
    return render(request, 'opencdr/index.html', context)


def cdrView(request):
    cdrfile = UploadFile.objects.all()

    context = {
        'cdrfile' : cdrfile
    }
    return render(request, 'opencdr/cdr.html', context)

def convert(request):

    name = True
    if name:
        job = cloudconvert.Job.create(payload={
            "tasks": {
                'import-my-file': {
                    'operation': 'import/url',
                    'url': 'https://github.com/chintan-dw/laxmi/raw/master/static/uploads/tiger1.cdr',
                    "filename": "tiger1.cdr"
                },
                'convert-my-file': {
                    'operation': 'convert',
                    "input_format": "cdr",
                    'output_format': 'pdf',
                    "engine": "inkscape",
                    'input': [
                        'import-my-file'
                    ],
                    "text_to_path": False
                },
                'export-my-file': {
                    'operation': 'export/url',
                    'input': [
                        'convert-my-file'
                    ],
                    "inline": True,
                    "archive_multiple_files": False
                }
            }
        })
        job = cloudconvert.Job.wait(id=job['id'])
        for task in job["tasks"]:
            if task.get("name") == "export-my-file" and task.get("status") == "finished":
                export_task = task
                print('here')
                
                file = export_task.get("result").get("files")[0]
                print(file)
                print(file['url'])
                cloudconvert.download(filename=file['filename'], url=file['url'])
    
    context = {
    
    }
    return render(request, 'opencdr/convert.html', context)

