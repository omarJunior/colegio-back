from django.shortcuts import render, redirect

# Create your views here.
def redirect_(request):
    return redirect("/admin/")