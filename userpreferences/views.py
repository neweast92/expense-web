from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from userpreferences.models import UserPreference
from django.contrib import messages


# Create your views here.
def index(request):
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            for k, v in data.items():
                currency_data.append({'name':k, 'value':v})
        return render(request, 'preferences/index.html', context={'currencies':currency_data, 'user_preferences':user_preferences})
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
            
        messages.success(request, 'Changes saved')
        return redirect('preference')
    