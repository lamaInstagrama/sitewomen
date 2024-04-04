from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect


def start_page(request: HttpRequest):
    return redirect('women_start_page')