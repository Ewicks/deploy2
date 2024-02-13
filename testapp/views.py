from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from .bots.richmond_bot import richmond_bot
from .bots.kingston_bot import kingston_bot
from .bots.woking_bot import woking_bot
from .bots.southwark_bot import southwark_bot
from .bots.guildford_bot import guildford_bot
from .bots.epsom_bot import epsom_bot
from .bots.lewisham_bot import lewisham_bot
from .bots.hammersmith_fulham_bot import hammersmith_fulham_bot
from .bots.bromley_bot import bromley_bot
from .bots.merton_bot import merton_bot
from .bots.kensington_chelsea_bot import kensington_chelsea_bot
from .bots.elmbridge_bot import elmbridge_bot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse
from django.core.files.base import ContentFile
import os
if os.path.isfile('env.py'):
    import env



# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def get_word_objects(request):
    words = Word.objects.filter(user=request.user).values_list('word', flat=True)
	# words = Word.objects.values_list('word', flat=True)
    objectlist = list(words)

    return objectlist


def pricing(request):
    return render(request, 'pricing.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def about(request):
    return render(request, 'about.html', {})

def reviews(request):

    return render(request, 'reviews.html', {})


def delete_scrape(request, pk):
    scrape = get_object_or_404(Scrape, pk=pk)
    redirect_to = 'bots'  
    scrape.delete()
  
    return redirect(reverse(redirect_to))

def deleteword(request, pk, redirect_to):
    word = Word.objects.get(id=pk, user=request.user)
    word.delete()
  
    return redirect(reverse(redirect_to))


@login_required
def richmond(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            return redirect('richmond')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'richmond.html', context)


def kensington_chelsea(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user 
            word_instance.save()
            print(form)
            form.save()
        return redirect('kensington_chelsea')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'kensington_chelsea.html', context)

def epsom(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user 
            word_instance.save()
            print(form)
            form.save()
        return redirect('epsom')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'epsom.html', context)

def merton(request):
    words = Word.objects.filter(user=request.user)
    
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user 
            word_instance.save()
            print(form)
            form.save()
        return redirect('merton')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'merton.html', context)

def bromley(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user 
            word_instance.save()
            print(form)
            form.save()
        return redirect('bromley')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'bromley.html', context)

def hammersmith_fulham(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            print(form)
            form.save()
        return redirect('hammersmith_fulham')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'hammersmith_fulham.html', context)

def woking(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            print(form)
            form.save()
        return redirect('woking')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'woking.html', context)

def lewisham(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            print(form)
            form.save()
        return redirect('lewisham')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'lewisham.html', context)

def elmbridge(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()

    if request.method == 'POST':
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            print(form)
            form.save()
        return redirect('elmbridge')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'elmbridge.html', context)

def kingston(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()


    if request.method == 'POST':
        print(request.POST)
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            print(form)
            form.save()
        return redirect('kingston')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'kingston.html', context)

def southwark(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()


    if request.method == 'POST':
        print(request.POST)
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            print(form)
            form.save()
        return redirect('southwark')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'southwark.html', context)

def guildford(request):
    words = Word.objects.filter(user=request.user)
    form = WordForm()
    dateform = DateForm()


    if request.method == 'POST':
        print(request.POST)
        form = WordForm(request.POST or None)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.user = request.user
            word_instance.save()
            print(form)
            form.save()
        return redirect('guildford')

    context = {
        'form': form,
        'words': words,
        'dateform': dateform,
    }
    return render(request, 'guildford.html', context)


def download_spreadsheet(request, pk):
    scrape_instance = get_object_or_404(Scrape, pk=pk)

    # Retrieve the worksheet file content
    worksheet_content = scrape_instance.worksheet_file.read()

    response = HttpResponse(worksheet_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{scrape_instance.borough}_results.xlsx"'
    return response


def view_results(request, pk):
    scrape_instance = get_object_or_404(Scrape, pk=pk)
    print(scrape_instance.startdate)

    data_list = json.loads(scrape_instance.data)
    num_results = scrape_instance.results_number

    context = {
        'num_results': num_results,
        'data_list': data_list,
        'scrape_instance': scrape_instance,
    }

    return render(request, 'view_results.html', context)


@login_required
def results(request):

      
    if request.method == 'POST':
        datesdict = request.POST.dict()
        startdate = datesdict['startdate']
        enddate = datesdict['enddate']
        wordlist = get_word_objects(request)
        print(request.POST)
        borough = request.POST.get('borough')
        print(borough)


        if borough == 'richmond':
            my_list = richmond_bot(startdate, enddate, wordlist)
        if borough == 'kingston':
            my_list = kingston_bot(startdate, enddate, wordlist)
        if borough == 'woking':
            my_list = woking_bot(startdate, enddate, wordlist)
        if borough == 'southwark':
            my_list = southwark_bot(startdate, enddate, wordlist)
        if borough == 'guildford':
            my_list = guildford_bot(startdate, enddate, wordlist)
        if borough == 'epsom':
            my_list = epsom_bot(startdate, enddate, wordlist)
        if borough == 'lewisham':
            my_list = lewisham_bot(startdate, enddate, wordlist)
        if borough == 'hammersmith_fulham':
            my_list = hammersmith_fulham_bot(startdate, enddate, wordlist)
        if borough == 'bromley':
            my_list = bromley_bot(startdate, enddate, wordlist)
        if borough == 'merton':
            my_list = merton_bot(startdate, enddate, wordlist)
        if borough == 'kensington_chelsea':
            my_list = kensington_chelsea_bot(startdate, enddate, wordlist)
        if borough == 'elmbridge':
            my_list = elmbridge_bot(startdate, enddate, wordlist)

        data_list = my_list[0]
        num_results = my_list[1]
        data_list_json = json.dumps(data_list)
        # Open the Google Spreadsheet using its title
        # Set up the credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        print(os.environ.get('CREDENTIALS_JSON_PATH'))
        lol = os.environ.get('CREDENTIALS_JSON_PATH')
        testing = ('/Users/ethanwicks/Documents/' + lol)
        print(testing)
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json' , scope)
        client = gspread.authorize(creds)

        # Open the Google Spreadsheet using its title
        spreadsheet = client.open("project")

        # Select the desired worksheet
        worksheet = spreadsheet.get_worksheet(0)  # You can change the index to select a different sheet

        worksheet.clear()

        # Define column titles
        column_titles = ["Index", "Name", "Address"]

        # Initialize data_to_write with header row
        data_to_write = [column_titles]

        # Loop through your_list with index
        for index, item in enumerate(data_list):
            row_data = [index + 1] + list(item)
            data_to_write.append(row_data)

        # Write data to the spreadsheet
        worksheet.append_rows(data_to_write)
        # print(testing)
        worksheet_content = worksheet.get_all_values()
        worksheet_data = "\n".join(["\t".join(row) for row in worksheet_content])
        worksheet_file = ContentFile(worksheet_data.encode('utf-8'))

        # Update the Scrape instance with the worksheet file
        print(worksheet_file)
        # worksheet_file.save("worksheet.txt", worksheet_file)
        

        # Close the connection
        creds = None

        if request.user and request.user.is_authenticated:
            user_instance = request.user


            # Create a new Scrape instance associated with the authenticated user
            scrape_instance = Scrape.objects.create(
                user=user_instance,
                borough=borough,
                startdate=startdate,
                enddate=enddate,
                results_number=num_results,
                data=data_list_json,
                # worksheet_file=worksheet_file,
                date_added=timezone.now()
            )
            scrape_instance.worksheet_file.save(f"{scrape_instance.borough}_worksheet.xlsx", worksheet_file)
            response = HttpResponse(worksheet_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            aaa = response['Content-Disposition'] = f'attachment; filename="{scrape_instance.borough}_results.xlsx'
            print(aaa)
            print(scrape_instance)

            scrape_results = Scrape.objects.filter(user=user_instance)


        context = {
            'my_list': data_list,
            'num_results': num_results,
            'scrape_results': scrape_results,

        }

        return redirect('bots')
    else:
        scrape_results = Scrape.objects.filter(user=request.user)

        context = {
            'scrape_results': scrape_results,
        }
        return render(request, 'bots.html', context)


