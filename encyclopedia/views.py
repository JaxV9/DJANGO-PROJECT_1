from django.shortcuts import render
from django import forms
from django.shortcuts import redirect
from markdown2 import Markdown


from . import util

markdowner = Markdown() #Convert the markdown to html

from django import forms



def newpage(request): #______________________Create a new page_____________________________

    def AlreadyExists(request): #Page not found
        return render(request, "encyclopedia/404.html", {
            "error": "This page already exists !"
        })

    class NewTitle(forms.Form): #a form to create a new title
        title = forms.CharField(label="", max_length=100)

    class NewContent(forms.Form): #a form to create a new content
        content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Content', 'class':'myForm'}))

    titles_pages = NewTitle(request.POST) #Take the form to create a new title
    contents_pages = NewContent(request.POST) #Take the form to create a new content

    if request.method == "POST": #If the user is creating a new page
        if titles_pages.is_valid() and contents_pages.is_valid():
            title = titles_pages.cleaned_data["title"] #Clean the title form
            content = contents_pages.cleaned_data["content"] #Clean the content form

            if util.get_entry(title) is not None: #If the title already exists
                return AlreadyExists(request) #return the def

            else:
                util.save_entry(title, '#' + title + '\n' + content) #Save the new title and content
                return titles(request, title) #Go to the new page

    else:
        return render(request, "encyclopedia/newpage.html", {
            "NewTitle": NewTitle(), #Render the form to create a new title
            "NewContent": NewContent() #Render the form to create a new content
        })



def index(request): #______________________Index_____________________________
    
    class SearchTool(forms.Form):   #Create the search tool
        search = forms.CharField(label="Search", widget=forms.TextInput(attrs={'placeholder':'Search a Title'})
        )

    List_of_titles = [] #Get the suggestions of titles
    Stry = "" #Take the search string

    if request.method == "POST": #If the user is searching for a title
        search = SearchTool(request.POST) #Take the search form/tool

        if search.is_valid():
            Stry = search.cleaned_data["search"] #Clean my tool

            for title in util.list_entries(): #take the list of titles in util
                if Stry.lower() == title.lower(): #If the search string is equal to a title
                    return titles(request, title) #Go to the title page

                if Stry.lower() in title.lower(): #If the any search string is in a title
                    List_of_titles.append(title)    #Add the title to the list of suggestions
                    return render(request, "encyclopedia/search.html", {
                        "list_of_titles": List_of_titles    #Show the list of suggestions
                    })

        if Stry.lower() != title.lower(): #Page not found if the search string is not equal to a title
            return error(request)


    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), #Show the list of titles
            "search": SearchTool() #Show the search tool
        })



def mod(request, title):

    class Content(forms.Form): #a form who take the content
        content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Content', 'class': 'myForm'}))


    if request.method == "GET": #If the user is modifying a page
        return render(request, "encyclopedia/mod.html", {
            "mod": Content(initial={'content': util.get_entry(title)}), #Render the form with the content of the title
        })

    else:
        Contents = Content(request.POST) #Take the form
        if Contents.is_valid():  #If the form is valid
            content = Contents.cleaned_data["content"] #Clean the form
            util.save_entry(title, content) #Save the new content
            return redirect("entry", title=title) #Go to this title page


def error(request): #__________________Page not found_________________________
    return render(request, "encyclopedia/404.html", {
        "error": "Page not found"
    })

def random(request): #______________________Random_titles_____________________________
    import random
    title = random.choice(util.list_entries())
    return titles(request, title)


def titles(request, title): #______________________ENTRY_Titles_____________________________

    if util.get_entry(title) is None:
        return error(request)
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": markdowner.convert(util.get_entry(title))
        })