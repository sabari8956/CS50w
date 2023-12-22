from django.shortcuts import render
from . import util
from django.shortcuts import redirect
from markdown2 import markdown as render_md
from random import choice

def index(request):
    print("here")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def url_direct(request, entry):

    if file := util.get_entry(entry):
        return render(request, "encyclopedia/entries.html",{
            "title": entry,
            "mdfile": render_md(file),
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "title": "File not found",
        })


def search(request):
    query = request.GET.get('q')
    if not query:
        return redirect("index")
    if file := util.get_entry(query):
        return render(request, "encyclopedia/entries.html",{
            "title": query,
            "mdfile": render_md(file),
        })
    else:
        similar_entries = []
        for entries in util.list_entries():
            if query in entries.lower():
                similar_entries.append(entries)
        if similar_entries:
            return render(request, "encyclopedia/index.html", {
                "entries": similar_entries,
            })
        return redirect('index')


def new_page(request):
    if request.POST:
        data = request.POST
        entries = [entry.lower() for entry in util.list_entries()]

        title = data['title']
        if title.lower() in entries:
            return render(request, "encyclopedia/error.html", {
                "title": "File already exists"
            })
        util.save_entry(title,data['cnt'])
        print("done ig")
        return redirect("index")
    return render(request,"encyclopedia/newpg.html")


def random_page(request):
    entries = util.list_entries()
    choosen_entry = choice(entries)
    file = util.get_entry(choosen_entry)
    return render(request, "encyclopedia/entries.html",{
            "title": choosen_entry,
            "mdfile": render_md(file),
        })


def edit_pg(request, entry):

    if data := request.POST:
        file = data["content"]
        util.save_entry(entry, file)
        return redirect("redir", entry= entry)
    file = util.get_entry(entry)
    return render(request, "encyclopedia/edit.html",{
        "title": entry,
        "content": file,
    })