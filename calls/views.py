from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
#calls/views.py

User = get_user_model()

@login_required
def video_call(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        try:
            receiver = User.objects.get(id=receiver_id)
            return JsonResponse({
                'status': 'success',
                'message': f'Call initiated to {receiver.username}'
            })
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})

    users = User.objects.exclude(id=request.user.id)  # show all except self
    return render(request, 'calls/video_call.html', {'users': users})
