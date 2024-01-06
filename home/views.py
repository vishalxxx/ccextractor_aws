from django.shortcuts import render
import os, shutil
from django.shortcuts import render, redirect
from django.views import View
from .models import Video
from  forms import VideoForm
import requests
import json
from django.core.management import call_command
# Create your views here.
api_url = 'http://127.0.0.1:8000/api/'

def home(request):
    return render(request, "home.html", {})




file_path = 'media/videos/'
def delete_files_in_directory(directory_path):
        try:
            files = os.listdir(directory_path)
            for file in files:
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("All files deleted successfully.")
        except OSError:
            print("Error occurred while deleting files.")

class VideoUploadView(View):
    template_name = 'home.html'
    
    
    delete_files_in_directory(file_path)
    def get(self, request):
        form = VideoForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        delete_files_in_directory(file_path)
        headers = {'Content-Type': 'application/json'}
        form = VideoForm(request.POST, request.FILES)
        uploaded_file = request.FILES['file']
        print(uploaded_file)
        if form.is_valid():
            form.save()
            data = {'file': 'media/videos/'+uploaded_file.name,
                    'searched_key': 'null'
                    }
            print(data)
            print(f"Data is here {data}")
            response = requests.post(api_url,data=json.dumps(data), headers=headers)
            print(f"POST Request Status Code: {response.status_code}")
            print("POST Request Response:")
            print(response.json())
            print("\n")
            return redirect('sub_search')
        return render(request, self.template_name, {'form': form})
    

    
    


class SubSearch(View):
    template_name = 'search.html'

    def get(self, request):
        query = request.GET.get('q', '')
        print(query)
        result = []  
        headers = {'Content-Type': 'application/json'}
        data = {'file': 'media/videos/',
                'searched_key': query
                }
        print(data)
        print(f"Data is here {data}")
        response = requests.post(api_url,data=json.dumps(data), headers=headers)
        print(f"POST Request Status Code: {response.status_code}")
        print("POST Request Response:")
        print(response.json())
        result = response.json()
        results_list = result.get('results', [])
        print("\n")
        context = {'query': query, 'results': results_list}
        return render(request, self.template_name, context)
    
    
