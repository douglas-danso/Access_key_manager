from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import AccessKey
# from .models import School
# from .forms import SchoolForm
from django.core.paginator import Paginator
from authentication.models import CustomUser

@login_required
def access_key_list(request,school_id):
    
    user = request.user 
    school_id =user.id
    school = user.school_name
    access_keys = AccessKey.objects.filter(school_id=school_id).order_by('-date_of_procurement')
    paginator = Paginator(access_keys, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'access_keys': access_keys,
               'school': school,
                'user': user,
                'page_obj':page_obj,
                }
    return render(request, 'access_key_list.html',context) 

@login_required
def purchase_key(request,school_id):
    user = request.user 
    school_id = user.id
    # school = user.school_name
    active_key = AccessKey.objects.filter(school_id = school_id, status=AccessKey.ACTIVE)
    if active_key:
        messages.warning(request, 'you already have an active access key')
        return redirect('schoolapp:access_key_list',user.id)
    else:
        return redirect('adminapp:access_key_generate',user.id)
    

# @login_required
# def school_view(request):
#     form = SchoolForm()

#     if request.method == 'POST':
#         form = SchoolForm(request.POST)
#         if form.is_valid():
#             name=form.cleaned_data['school_name']
#             user = request.user
#             school = School.objects.create(school_name=name, user=user)
#             school.save()
#             return redirect('schoolapp:access_key_list', school_id=school.id)
#         else:
#             form = SchoolForm()

    # return render(request, 'school.html', {'form':form})


