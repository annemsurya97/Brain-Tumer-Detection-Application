from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.conf import settings
from .models import Test_data


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import preprocessing
import pickle
import seaborn as sns
from sklearn.svm import SVC
import warnings
warnings.filterwarnings('ignore')
from skimage.transform import resize
from skimage.io import imread
from skimage import io, transform
import tempfile
# Create your views here.
 
def Home(request):
    return render(request,'Home.html')

def Login_view(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request,'Please enter valid credentials')
            return redirect('login')
    return render(request,'Login.html')
def Admin_view(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request,user)
                return redirect('Home')
            else:
                messages.error(request,'Sorry Not an Admin')
            return redirect('Admin')
        else:
            messages.error(request,'Please enter valid credentials')
            return redirect('Admin')
    return render(request,'Admin.html')

def register_view(request):
    if request.method=='POST':
        name=request.POST.get('name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        email=request.POST.get('email')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already exist')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email aleady exist')
                    return redirect('register')
                else:
                    user=User.objects.create_user(username=username,password=password,first_name=name,email=email)
                    user.save()
                    messages.error(request,'Account created Sucessfully')
                    return redirect('login')
        else:
            messages.error(request,'Password Not Match')
            return redirect('register')
    return render(request,'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def users_view(request):
    data=User.objects.filter(is_staff=False,is_superuser=False)
    return render(request,'Users.html',{'data':data})

def activate_view(request,id):
    user=User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('user')
def Deactivate_view(request,id):
    user=User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('user')

def delete_view(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect('user')

def predict_view(request):
    if request.method =='POST' and request.FILES['image']:
        path =  os.path.join(settings.BASE_DIR, 'static', 'Dataset')
        model=os.path.join(settings.BASE_DIR, 'static', 'model','Classifier.pkl') 
        with open(model, 'rb') as model_file:                             
            rf_classifier=pickle.load(model_file)     
        Categories = {1:'NORMAL',0:'FIRE'}
        image_file=request.FILES['image']
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        img=imread(temp_file_path)
        Categories = {1:'NORMAL',0:'FIRE'}  # Define your categories with corresponding labels
        img_resize = resize(img, (150, 150, 3))
        l = [img_resize.flatten()]
        # Make predictions using your pre-trained model
        
        prediction = rf_classifier.predict(l)[0]
        predicted_category = Categories[prediction]
        plt.imshow(img)
        plt.text(10, 10, f'Predicted Output: {predicted_category}', color='white',fontsize=12,weight='bold',backgroundcolor='black')
        plt.axis('off')
        plt.show()
        os.remove(temp_file_path)
        return render(request,'Form.html',{'output': predicted_category})
    return render(request,'Form.html')
def recent_data(request):
    user=request.user
    user_data=Test_data.objects.filter(user=user).order_by('-id')
    admin_data=Test_data.objects.all().order_by('-id')
    return render(request,'Test_list.html',{'user_data':user_data,'admin_data':admin_data})