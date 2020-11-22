from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.forms import profileUpdateForm, userUpdateForm
from users.models import Profile as Pro
from users.models import  Requests
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
# from memberships.models import Membership, UserMembership, Subscription
from django.core.mail import send_mail
from django.core.mail import EmailMessage

# Create your views here.

# def get_user_membership(request):
#     user_membership_qs = UserMembership.objects.filter(user=request.user)
#     if user_membership_qs.exists():
#         return user_membership_qs.first()
#     return None
#
# def get_user_subscription(request):
#     user_subscription_qs = Subscription.objects.filter(user_membership = get_user_membership(request))
#     if user_subscription_qs.exists():
#         user_subscription = user_subscription_qs.first()
#         return user_subscription
#     return None


@login_required
def Profile(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    Pro.objects.filter(id=request.user.profile.id).update(is_teacher=True)

    if request.method == 'POST':
        u_form = userUpdateForm(request.POST,instance=request.user)
        p_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Account Has Been Successfully Updated !!')
            return redirect('users:profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context= {
        'u_form':u_form,
        'p_form':p_form,
        'user_membership':user_membership,
        'user_subscription': user_subscription
    }
    return render(request,'profile/profile.html',context)

def Request(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('e-mail')
        Telephone_Number = request.POST.get('phone')
        prof = request.user.profile
        Approved = False
        Request = Requests(Profile=prof, Name=Name, Email=Email, Telephone_Number=Telephone_Number,Approved=Approved)
        Request.save()
        prof_id = prof.id
        if Requests.objects.get(Profile_id=prof_id).Approved == False:
            messages.info(request, f'The Request Was Sent Successfully, You Will Be Notified By Email.')
            send_mail(
                'Ukyply',
                'Someone Requested A Teacher Account. Their Info: ' + Name + ' , ' + Email + ' , ' + Telephone_Number + ' , ' + str(prof) + '.',
                'foreducation9800@gmail.com',
                ['foreducation9800@gmail.com'],
                fail_silently=False,
            )
            return redirect('courses:home')

            Pro.objects.filter(id=prof_id).update(is_teacher=True)

            message = 'Your Request For A Teacher Account Has Been Accepted! Now You Can Go Back To Ukyply And Upload Courses And Lectures, Good Job!'
            send_mail(
                'Ukyply, The Request Was Accepted',
                message,
                'foreducation9800@gmail.com',
                [Email],
                fail_silently=False,
            )
            return redirect('courses:home')
