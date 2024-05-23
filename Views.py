import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            data = df.to_html(index=False, table_id="excelTable")
            columns = df.columns.tolist()
            unique_values = {col: df[col].dropna().unique().tolist() for col in columns}
            return render(request, 'excelapp/display.html', {'data': data, 'columns': columns, 'unique_values': unique_values})
    else:
        form = UploadFileForm()
    return render(request, 'excelapp/upload.html', {'form': form})
