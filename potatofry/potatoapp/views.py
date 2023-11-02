from django.shortcuts import render,redirect
from . models import Song,Artist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

songlist = []
lost = []
songlistobj = Song.objects.all()
for i in songlistobj:
    songlist.append(i.title)
    lost.append(i.artist)

artistlist = []
artistobj = Artist.objects.all()
for i in artistobj:
    artistlist.append(i.name)

@login_required
def index(request):
    leest = []
    listobj = Song.objects.all()
    artistobj = Artist.objects.all()
    for i in artistobj:
        leest.append(i.name)
    newleest = []
    for i in listobj:
        if i.artist not in leest:
            newleest.append(i)
    context={"song":newleest,'artist':artistobj,'uname':'Good day Mate, See you soon!'}
    return render(request,"list.html",context)


def home(request):
    if request.method == 'POST':

        namee = request.POST['search'].upper()
        
        if namee in songlist:
            song = Song.objects.get(title=namee)
            data = request.POST['data']
            if data == 'list':
                context={"song":song,'home2':'Home','uname':'Good day Mate, See you soon!'}
            else:
                context={"song":song,'home2':'Back','uname':'Good day Mate, See you soon!'}

            return render(request,"index.html",context)
        
        elif namee in artistlist:
            if namee in lost:
            # artsong = Song.objects.filter(artist=namee).first()
                id = Song.objects.filter(artist=namee).first().id
                return redirect('potatoapp:artist',pk=id)
        
            else:
                allsongs = Song.objects.filter(artist=namee)
                return render(request,'artist.html',{'song':allsongs})

        listobj = Song.objects.all()
        artistobj = Artist.objects.all()
        context={"song":listobj,'artist':artistobj,'Search':'Invalid Song or Artist    '}
        return render(request,"library.html",context)
 

def prev(request):
    if request.method == 'POST':

        decider = request.POST['decider']
        art =  request.POST['artist']
        songid = int(request.POST['songid'])
        artobj = Song.objects.filter(artist=art)
        leest = []

        for i in artobj:
            leest.append(i)

        if decider == 'Back':
            for i in leest:
                if i.id == songid:
                    newid = leest.index(i)-1
                    if newid < 0:
                        newid = len(leest)-1
                
                    song = leest[newid]
                    context={"song":song,'home2':'Back','uname':'Good day Mate, See you soon!'}
                    break
        else:
            value = request.POST['prev']
            listobj = Song.objects.all()
            lastobj = 20

            for i in listobj:
                lastobj += 1

            context={"song":listobj}
            currentid = Song.objects.get(title=value).id

            if currentid != 21:
                currentid -= 1
                song = Song.objects.get(id=currentid)
                context={"song":song, 'home2':'Home','uname':'Good day Mate, See you soon!'}
                
            else:
                song = Song.objects.get(id=lastobj)
                context={"song":song , 'home2':'Home','uname':'Good day Mate, See you soon!'}

        return render(request,"index.html",context)
            

def next(request):

    if request.method == 'POST':

        listobj = Song.objects.all()
        lastobj = 20
        for i in listobj:
            lastobj += 1
       
        decider = request.POST['decider']
        art =  request.POST['artist']
        songid = int(request.POST['songid'])
        artobj = Song.objects.filter(artist=art)
        lastart = 0
        leest = []
        for i in artobj:
            lastart += 1
            leest.append(i)

        if decider == 'Back':
            for i in artobj:
                if i.id == songid:
                    newid = leest.index(i)+1
                    if newid > lastart-1:
                        newid = 0
                
                    song = leest[newid]
                    context={"song":song,'home2':'Back','uname':'Good day Mate, See you soon!'}
                    break

        else:
            value = request.POST['next']
            currentid = Song.objects.get(title=value).id
            if currentid != lastobj:
                currentid += 1
                song = Song.objects.get(id=currentid)
                context={"song":song,'home2':'Home','uname':'Good day Mate, See you soon!'}
                
            else:
                song = Song.objects.get(id=21)
                context={"song":song, 'home2':'Home','uname':'Good day Mate, See you soon!'}

        return render(request,"index.html",context)

def loginview(request):
    uname = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(request, username=uname, password=pwd)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        return render(request,"login.html")
        
def logout_view(request):
    logout(request)
    return redirect('potatoapp:index')

def sign_up(request):
        uform = UserCreationForm(request.POST)
        if request.method == "POST":
            if uform.is_valid():
                uname = uform.cleaned_data.get('username')
                pwd = uform.cleaned_data.get('password1')
                email=uform.cleaned_data.get('email')
                user1=User.objects.create_user(username=uname,password=pwd,email=email)
                user1.save()
                user = authenticate(request, username=uname, password=pwd)
                login(request,user)
                return redirect('potatoapp:index')
        else:
            form1 = UserCreationForm()
            return render(request, 'registration/sign_up.html', {'form': form1})
        return render(request, 'registration/sign_up.html', {'form': uform})
    
def Resethome(request):
    return render(request,'registration/ResetPassword.html')

def resetPassword(request):
    responseDic={}
    try:
        usern = request.POST['uname']
        # recepient=request.POST['email']
        pwd=request.POST['password']
        #subject="Password reset"
        try:
            user=User.objects.get(username=usern)
            if user is not None:
                user.set_password(pwd)
                user.save()
                #send_mail(subject,message, EMAIL_HOST_USER, [recepient])
                responseDic["errmsg"]="Password Reset Successfully"
                return render(request,"registration/ResetPassword.html",responseDic)
        except Exception as e:
            print(e)
            responseDic["errmsg"]="Email doesnt exist"
            return render(request,"registration/ResetPassword.html",responseDic)
        
    except Exception as e:
        print(e)
        responseDic["errmsg"]="Failed to reset password"
        return render(request,"registration/ResetPassword.html",responseDic)
    
def artist(request,pk=1):
    if request.method == 'POST':
        value = request.POST['art']
        allsongs = Song.objects.filter(artist=value)
    else: 
        value = pk
        song = Song.objects.get(id=value)
        name = song.artist
        allsongs = Song.objects.filter(artist=name)

    return render(request,'artist.html',{'song':allsongs,'uname':'Good day Mate, See you soon!'})

def library(request):
    listobj = Song.objects.all()
    artistobj = Artist.objects.all()
    context={"song":listobj,'artist':artistobj,'uname':'Good day Mate, See you soon!'}
    return render(request,"library.html",context)  