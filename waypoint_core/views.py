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

def catalog(request):
    from trails.models import Trail

    trails = Trail.objects.filter(is_open=True).order_by("distance_km")

    context = {
        "trails": trails
    }

    return render(request, "catalog.html", context)