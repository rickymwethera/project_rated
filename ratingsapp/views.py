from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Project, Rate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProjectUploadForm, ProfileEditForm, RatingsForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import status
# Create your views here.
def home(request):
    projects = Project.objects.all()
    return render(request, 'index.html',{"projects":projects})


def create_post(request):
    current_user = request.user
    form = ProjectUploadForm()
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES or None)
        if form.is_valid():
            add=form.save(commit=False)
            add.user = request.user
            add.save()
            return redirect('home')
    

    context = {'form':form}
    return render(request,'create_post.html',context)

def search_results(request):
    if request.method == 'GET':
        title = request.GET.get("query")
        results = Project.objects.filter(title__icontains=title).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'search.html', {'message': message})


def detail(request,pk):
   
    project = Project.objects.get(id=pk)
    ratings = Rate.objects.filter(user=request.user, project=project).first()
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            project_rating = Rate.objects.filter(project=project)
            design = sum([design.design for design in project_rating])/len([design.design for design in project_rating])
            usability = sum([use.usability for use in project_rating])/len([use.usability for use in project_rating])
            content = sum([content.content for content in project_rating])/len([content.content for content in project_rating])

            score =(design + usability + content) / 3
            rate.score = round(score, 2)
            print(rate.score)
            rate.save()
            
            
    else:
        form = RatingsForm()
    
    params = {
        'project': project,
        'form':form,
       
            }

    return render(request,"project_detail.html", params)


def profile(request):
    projects = Profile.objects.all()
    user= request.user
    params = {
        'projects':projects,
        'user_form':user_form,
        'profile_form':profile_form,
        'user':user,
        
       
    }
   
    return render(request, 'profile.html', params)


class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
            serializers = ProjectSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
            serializers = ProfileSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)