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
    trails = [
        {
            "name": "Maple Ridge Trail",
            "distance": 5.2,
            "elevation": 180,
            "difficulty": "easy",
            "is_open": True,
        },
        {
            "name": "Pine Valley Loop",
            "distance": 8.7,
            "elevation": 320,
            "difficulty": "moderate",
            "is_open": True,
        },
        {
            "name": "Eagle Peak",
            "distance": 12.4,
            "elevation": 650,
            "difficulty": "expert",
            "is_open": True,
        },
        {
            "name": "Cedar Creek Trail",
            "distance": 4.8,
            "elevation": 120,
            "difficulty": "easy",
            "is_open": False,
        },
        {
            "name": "Rocky Summit",
            "distance": 15.6,
            "elevation": 890,
            "difficulty": "expert",
            "is_open": True,
        },
        {
            "name": "Willow Forest Path",
            "distance": 7.3,
            "elevation": 240,
            "difficulty": "moderate",
            "is_open": True,
        },
    ]

    context = {
        "trails": trails
    }

    return render(request, "catalog.html", context)