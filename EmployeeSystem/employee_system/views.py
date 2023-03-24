from django.shortcuts import render,redirect
from .models import EmployeeModel
from .models import PictureModel
from django.conf import settings
import base64
import os
from django.http import HttpResponse,JsonResponse
import shutil
import face_recognition

def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def create_employee(request):
    if request.method=='POST':
        employee=EmployeeModel()
        employee.first_name=request.POST.get('first_name')
        employee.last_name=request.POST.get('last_name')
        employee.profile_picture=request.FILES['picture_1']
        employee.profile_picture=request.FILES['picture_2']
        no=employee.save()
        print(f'This is the id: {employee.id}')
        if(request.FILES['picture_1']):
            employee.profile_picture=request.FILES['picture_1']
            save_picture(employee.id,request.FILES['picture_1'])
        if(request.FILES['picture_2']):
            employee.profile_picture=request.FILES['picture_2']
            save_picture(employee.id,request.FILES['picture_2'])
        return redirect('/employee-list')
    return render (request,'employee_create.html')

def save_picture(num,profile_picture):
    if profile_picture:
        file_path = os.path.join(settings.MEDIA_ROOT,str(profile_picture))
        with open(file_path, 'wb+') as destination:
            for chunk in profile_picture.chunks():
                destination.write(chunk)
    photo=PictureModel()
    photo.location='pictures/employees/'+str(profile_picture)
    photo.name=str(profile_picture)
    photo.employee_id=num
    photo.save()

def recognize_employee(request):
    employees=EmployeeModel.objects.all()
    return render(request, 'recognition.html',{'employees':employees})

def list_employee(request):
    employees=EmployeeModel.objects.all()
    return render(request, 'employees.html',{'employees':employees})

def recognize(file_name):
    employees=EmployeeModel.objects.all()
    for employee in employees:
        employee_images=[]
        loaded_employee_images=[]
        enc_employee_images=[]
        for picture in PictureModel.objects.filter(employee_id=employee.id):
            img=str(os.path.join(settings.BASE_DIR,'pictures/employees/'+str(picture.name)))
            employee_images.append(img)
        for image in employee_images:
            loaded_img=face_recognition.load_image_file(image)
            loaded_employee_images.append(loaded_img)
        for limg in loaded_employee_images:
            enc_img=face_recognition.face_encodings(limg)[0]
            enc_employee_images.append(enc_img)
        image_to_test=face_recognition.load_image_file(str(os.path.join(settings.BASE_DIR,'pictures/test/'+file_name)))
        enc_image_to_test=face_recognition.face_encodings(image_to_test)[0]
        results=face_recognition.compare_faces(enc_employee_images,enc_image_to_test)
        for result in results:
            if(result==True):
                return employee

def recognition_test(request): 
    file_name=''
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if image_data:
            image_data = base64.b64decode(image_data.split(',')[1])
            file_path = os.path.join(settings.BASE_DIR,'pictures/test/')
            file_name = 'test.jpg'
            with open(os.path.join(file_path, file_name), 'wb') as f:
                f.write(image_data)
            print('Image saved successfully')
    employee=recognize(file_name)   
    return render(request,'result.html',{'employee':employee})

def delete_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
            
def my_view(request):
    folder_path = '/path/to/folder'
    delete_files_in_folder(folder_path)
    return HttpResponse('Files deleted successfully')

def employee_json(request):
    employees=EmployeeModel.objects.all().values()
    data=list(employees)
    for dt in data:
       dt['profile_picture'] = '<img src="{% static \'' + str(dt['profile_picture']) + '\' %}">'

    return JsonResponse(data,safe=False)


