from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("learning_logs:dashboard")
        else:
            errors = form.errors.get_json_data()
            error_messages = [errors[error][0]["message"] for error in errors]
            
    else:
        form = UserCreationForm()
        error_messages = ""
        
    context = {"form": form, "error_messages": error_messages}
    
    return render(request, "registration/signup.html", context)