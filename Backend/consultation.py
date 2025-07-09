from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import *

from Backend.decorateur import permission_requise
from Backend.formulaire import *
from Backend.models import *


def retournerTontine(request):
    tontine = Tontine.objects.all()
    a = Association.objects.first()
    return render(request, "consultation/tontine.html", context={"tontine": tontine, "a": a})

def retournerSession(request, tontine_id):
    sessions = SessionTontine.objects.filter(tontine_id=tontine_id)
    a = Association.objects.first()
    return render(request, "consultation/session.html", context={"sessions": sessions, "a": a})

def retournerParamettrage(request, session_id):
    parametrages = ParametrageTontine.objects.filter(session_id=session_id)
    a = Association.objects.first()
    session = SessionTontine.objects.get(pk=session_id)
    return render(request, "consultation/paramettrage.html", context={"parametrages":parametrages, "a": a, "session": session})


def retournerCotisation(request, parametrage_id):
    cotisations = Cotisation.objects.filter(paramettrageTontine_id=parametrage_id, etat=True).order_by('date', 'membre__nom')
    a = Association.objects.first()
    parametrages = ParametrageTontine.objects.filter(pk=parametrage_id)
    parametrage = ParametrageTontine.objects.get(pk=parametrage_id)
    return render(request, "consultation/cotisation.html", context={"cotisation_terminer": cotisations, "a": a, "parametrages": parametrages, "parametrage": parametrage})