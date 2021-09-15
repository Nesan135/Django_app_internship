from django.shortcuts import render
from .forms import CsvModelForm
from .models import Csv
import csv
from irdp.models import Ahli
# Create your views here.

def upload_seats(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                #first line in excel file is passed
                if i==0:
                    pass
                else:
                    #first column entries become names --> row[0]
                    #second column entries become names --> row[1]
                    #second column entires will become the primary keys
                    Ahli.objects.create(
                        name =  row[0],
                        state = row[1].lower(),
                    )
            obj.activated = True
            obj.save()
    return render(request, 'csvs/upload.html',{'form' : form})

def upload_data(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    try:
                        exo = Ahli.objects.get(pk=row[1].lower())
                        exo.name = row[0]
                        exo.save()
                    except:
                        continue
    return render(request, 'csvs/uploaded.html',{'form' : form})