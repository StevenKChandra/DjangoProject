from django.http import HttpResponse

# Create your views here.

def Index(request):
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits
    resp = HttpResponse(f'Hi, you have viewed this page {num_visits} times')
    resp.set_cookie('dj4e_cookie', '60bbae9c', max_age=1000)
    return resp