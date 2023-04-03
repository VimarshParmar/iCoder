from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact, CreatePost
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def home(request):
    # return HttpResponse("This is home")
    return render(request,'home/home.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name, email, phone, content)
        
        if len(name)<3 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent ")

    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>80:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains =query)
        allPostContent = Post.objects.filter(content__icontains = query)
        allPosts = allPostsTitle.union(allPostContent)
    
    if allPosts.count() == 0:
        messages.warning(request, "No search result found. refine your query")
    params = {'allPosts':allPosts, 'query':query}
    return render(request,"home/search.html", params)


def handleSignup(request):
    if request.method == 'POST':
        #Get parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #Username should be 10 char
        if len(username)>10:
            messages.error(request, " Username must be under 10 characters ")
            return redirect('home')
        
        #Username must be alphanumeric
        if not username.isalnum():
            messages.error(request," username must be in alphanumeric ")
            return redirect('home')
        
        #password should be same
        if pass1 != pass2:
            messages.error(request,"Password must be same")
            return redirect('home')

        #Create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been created succesfully")
        return redirect('home')

    else:
        return HttpResponse('404- Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request,"Successfully Loged in")
            return redirect('home')
        
        else:
            messages.error(request,"Invalid credential, Please try again")
            return redirect('home')

    return HttpResponse('404- Page not found')


def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Loged out")
    return redirect('home')

def create_post(request):
    if request.POST:
        author = request.POST['name']
        description = request.POST['description']
        title = request.POST['title']
        slug = title
        # image = request.POST['image']
        # print(name, description, title, image)
        # user_id = request.session['user_id']

        if len(author)<3 or len(description)<3 or len(title)<3 :
            messages.error(request, "Please fill the form correctly")
        else:
            createpost = Post( title=title, content=description, author=author, slug=slug)
            # createpost.user_id_id = user_id
            createpost.save()

            messages.success(request, 'your post has been sucessfully')
        return redirect('home')
    return render(request,'home/CreatePost.html')
  
def about(request):
    return render(request, 'home/about.html')   
