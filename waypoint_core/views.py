
from django.shortcuts import get_object_or_404, render


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
    from trails.models import Park, Trail

    park_id = request.GET.get("park")

    trails = Trail.objects.filter(is_open=True).order_by("distance_km")

    selected_park = None

    if park_id:
        selected_park = Park.objects.filter(id=park_id).first()

        if selected_park:
            trails = trails.filter(park=selected_park)

    parks = Park.objects.all().order_by("name")

    context = {
        "trails": trails,
        "parks": parks,
        "selected_park": selected_park,
    }

    return render(request, "catalog.html", context)

def trail_detail(request, trail_id):
    from trails.models import Trail

    trail = get_object_or_404(Trail, id=trail_id)

    return render(request, "trail_detail.html", {"trail": trail})