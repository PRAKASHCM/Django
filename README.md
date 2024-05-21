# myapp/forms.py

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


# myapp/views.py

import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            html_table = df.to_html(classes='table table-striped', index=False)
            return render(request, 'display_data.html', {'table': html_table})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

<!-- myapp/templates/upload.html -->

{% load widget_tweaks %}
<!DOCTYPE html>
<html>
<head>
    <title>Upload File</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h2>Upload Excel File</h2>
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form|crispy }}
            <button type="submit" class="btn btn-primary">Upload</button>
        </form>
    </div>
</body>
</html>

<!-- myapp/templates/display_data.html -->

<!DOCTYPE html>
<html>
<head>
    <title>Display Data</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">
</head>
<body>
    <div class="container">
        <h2>Data Table</h2>
        <table id="data_table" class="display">
            {{ table|safe }}
        </table>
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
    <script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#data_table').DataTable({
                "paging": true,
                "ordering": true,
                "info": true,
                "searching": true
            });
        });
    </script>
</body>
</html>



# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
]
