from django.shortcuts import render


def home(request):
    context = {
        "greeting": "Welcome to Waypoint!"
    }

    return render(request, "home.html", context)


def report(request):
    if request.method == "POST":
        name = request.POST.get("name", "")

        context = {
            "name": name
        }

        return render(request, "report_thanks.html", context)

    return render(request, "report.html")


def search(request):
    query = request.GET.get("q", "")

    context = {
        "query": query
    }

    return render(request, "search.html", context)