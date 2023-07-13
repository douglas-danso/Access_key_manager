from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import AccessKey
# from schoolapp.models import School
from .forms import AccessKeyForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import datetime
from authentication.models import CustomUser


@method_decorator(login_required, name='dispatch')
class AccessKeyListView(ListView):
    model = AccessKey
    template_name = 'adminapp/dashboard.html'
    context_object_name = 'access_keys'
    ordering = ['date_of_procurement']
    paginate_by = 10


@login_required
def access_key_generate(request,school_id):
    user = request.user
    school_id = user.id
    schools =user.school_name
    form = AccessKeyForm()
   
    
    if request.method == 'POST':
        form = AccessKeyForm(request.POST)
        if form.is_valid():
            access_key = form.save(commit=False)
            
            # access_key.key = form.generate_key()
            access_key.school = user
            if access_key.expiry_date and access_key.expiry_date < datetime.date.today():
                messages.warning(request,'Expiry date cannot be in the past.')
                return redirect('adminapp:access_key_generate',user.id)
            else:
                access_key.expiry_date = form.cleaned_data['expiry_date']
            access_key.save()
            
            current_site = get_current_site(request)
            access_key = AccessKey.objects.filter(school_id=school_id, status='active').first()
            
            
            message=render_to_string('message.html', {
                'user': user,
                'domain': current_site.domain,
                'access_key':access_key,
                'schools':schools
            })
       
            message = strip_tags(message)
            mail_subject = 'Access key Purchase'
            email_from = user.email
            recipient_list =["douglasdanso66@gmail.com"]
            send_mail( mail_subject, message, email_from, recipient_list )
            return redirect('schoolapp:access_key_list', user.id)
        else:
            form = AccessKeyForm()
    context = {
        'form':form,
        'schools':schools,
    }  
    
    return render(request, 'adminapp/access_key_generate.html', context)

@login_required
def revoke_key(request, access_key_id):
    access_key = get_object_or_404(AccessKey, id=access_key_id)
    access_key.status = 'revoked'
    access_key.save()
    messages.success(request, 'Key revoked successfully.')
    return redirect('adminapp:access_key_list')

@login_required
def access_key_update(request, access_key_id):
    access_key = get_object_or_404(AccessKey, pk=access_key_id)

    if request.method == 'POST':
        form = AccessKeyForm(request.POST, instance=access_key)
        if form.is_valid():
            if access_key.expiry_date and access_key.expiry_date < datetime.date.today():
                messages.warning(request,'Expiry date cannot be in the past.')
                return redirect('adminapp:access_key_update',access_key.id)
            else:
                access_key.expiry_date = form.cleaned_data['expiry_date']
            access_key = form.save()
            
            messages.success(request, f'Access key {access_key.key} has been updated.')
            return redirect('adminapp:access_key_list')
    else:
        form = AccessKeyForm(instance=access_key)

    return render(request, 'adminapp/access_key_update.html', {'form': form, 'access_key': access_key})