from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("practice_logs:dashboard")
        else:
            errors = form.errors.get_json_data()
            error_messages = [errors[error][0]["message"] for error in errors]
            
    else:
        form = SignUpForm()
        error_messages = ""
        
    context = {"form": form, "error_messages": error_messages}
    
    return render(request, "registration/signup.html", context)