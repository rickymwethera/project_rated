from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Project, Rate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    projects = Project.objects.all()
    return render(request, 'index.html',{"projects":projects})


def create_post(request):
    current_user = request.user
    form = ProjectPostForm()
    if request.method == 'POST':
        form = ProjectPostForm(request.POST, request.FILES or None)
        if form.is_valid():
            add=form.save(commit=False)
            add.user = request.user
            add.save()
            return redirect('index')
    

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