from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from . import util
import markdown2


def index(request):
    search = request.GET.get("q", "").upper()
    if search:
        similar_entry = []
        all_entries = util.list_entries()
        for entry in all_entries:
            try:
                a = entry.upper().index(search)
                similar_entry.append(entry)
            except ValueError:
                continue
        return render(request, "encyclopedia/index.html", {
            "entries": similar_entry,
            "search": True
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "search":False
        })

def entry(request,title):
    entry = util.get_entry(title)
    if entry:
        converted_entry = markdown2.markdown(entry)
        print(type(converted_entry))
        return render(request, "encyclopedia/entry_page.html", {
            "entry":converted_entry,
            "title":title
        })
    else:
        raise Http404("Entry does not exist.")

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"].strip()
        content = request.POST["content"]
        all_titles = [item.upper() for item in util.list_entries()]
        try:
            a = all_titles.index(title.upper())
            messages.warning(request, "There is already an entry with the same title")
            print(request.POST["content"])
            return render(request, "encyclopedia/new_page.html", {
                "title":request.POST["title"],
                "content": content
            })
        except ValueError:
            util.save_entry(title, content)
            messages.success(request, "You've successfully created an entry")
            return HttpResponseRedirect(reverse("index"))


        

    else:
        return render(request, "encyclopedia/new_page.html")
