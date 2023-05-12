from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import FileUploadForm,EditWordForm 
from googletrans import Translator
from .models import Words,UserWords,UserWordsNums
import re
from datetime import datetime
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.forms.models import model_to_dict
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

prev_total_words = 0 # holds total words quantity of user before translation
new_words_counter = 0 # counts new words numbers
def Home(request):
    try:
        global total_words
        total_words = UserWords.objects.filter(user=request.user).count()
    except Exception as e:
        print('bomadi')
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('neword:home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('neword:home')

def profile(request):
    global total_words,new_words_counter
    total_words = UserWords.objects.filter(user=request.user).count()
    user = request.user
    words_list = UserWords.objects.filter(user=request.user).order_by('-date_added')
    total = total_words
    # create a dictionary to pass to the template
    context = {
        'words_list': words_list,
        'user': user,
        'total_words':total,
        'new_added':new_words_counter,
    }
    new_words_counter = 0
    return render(request, 'registration/profile.html', context)	

@login_required
def text_trans(request):
    if request.method == 'POST':
        count = 0
        # Logic to handle form submission goes here
        global new_words_counter
        percent = 0
        user = request.user
        text = request.POST.get('text')
        words = purify_words(text.split(' '))
        translator = Translator()
        user_words = UserWords.objects.filter(user=request.user).values_list('word', flat=True)
        user_words_list = list(user_words)
        new_words_counter = newbies(words,user_words_list)
        new_words = new_word(words,user_words_list)
        for word in new_words:
            try:
                translation = translator.translate(word, dest='uz').text
                UserWords.objects.create(word=word.lower(), translation=translation.lower(),user=user,date_added=datetime.now())
                user_words_list.append(word.lower())
            except Exception as e:
                print('No words')
 
        return redirect('neword:profile')
    else:
        return render(request, 'text_trans.html')

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Do something with the uploaded file
            uploaded_file = request.FILES['file']
            # Process the file and find new words
            # ...
            return render(request, 'file_upload_success.html')
    else:
        form = FileUploadForm()
    return render(request, 'file_trans.html', {'form': form})

@login_required
def delete_word(request, word_id):
    word = get_object_or_404(UserWords, id=word_id, user=request.user)
    word.delete()
    return JsonResponse({'success': True})

@csrf_exempt
def edit_word(request, pk):
    if request.method == 'POST':
        word = get_object_or_404(UserWords, pk=pk)
        word.word = request.POST.get('word')
        word.translation = request.POST.get('translation')
        word.save()
        data = {
            'success': True,
            'word': {
                'word': word.word,
                'translation': word.translation,
            },
        }
        return JsonResponse(data)

def purify_words(words):
    clean_words = [re.sub(r'\W+', '', word) for word in words]
    return clean_words

def get_data(request,data):
    return JsonResponse(data)


def newbies(words,user_words_list):
    count = 0
    new_words = []
    for i in words:
        if i not in user_words_list:
            count+=1
            new_words.append(i)
    return count

def new_word(words,user_words_list):
    new_words = []
    count = 0
    for i in words:
        count += 1
        if not i in user_words_list and not i in new_words:
            new_words.append(i)
    print(len(user_words_list),count)
    return new_words