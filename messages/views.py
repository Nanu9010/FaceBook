from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def messages(request):
    return render(request, "messages/messages.html")

@login_required
def message(request, user_id):
    return render(request, "messages/message.html")
