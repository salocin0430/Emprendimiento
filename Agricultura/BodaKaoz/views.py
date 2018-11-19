from django.shortcuts import redirect

def handler404View(request):
    return redirect("index")