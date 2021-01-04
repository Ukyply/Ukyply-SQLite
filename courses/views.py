import secrets
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView,DetailView,View
from courses.models import Course,Lesson,Category
# from memberships.models import UserMembership
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CategoryForm, CourseForm, LessonForm
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['category'] = category
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'



def CourseListView(request, category):
    courses = Course.objects.filter(Category=category)
    context = {
        'courses':courses
    }
    return render(request, 'courses/course_list.html', context)



class CourseDetailView(DetailView):
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    model = Course


class LessonDetailView(View,LoginRequiredMixin):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        context = {'lesson': lesson}
        return render(request, "courses/lesson_detail.html", context)


# @login_required
def SearchView(request):
    if request.method == 'POST':
        Search = request.POST.get('search')
        results = Lesson.objects.filter(Title__contains=Search)
        context = {
            'results':results
        }
        return render(request, 'courses/search_result.html', context)


@login_required
def create_category(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Kategoriýa döretmek isleseňiz ilki mugallym bolmaly !!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = CategoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Kategoriýa üstünlikli döredildi !!')
            return redirect('courses:home')
    else:
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'courses/create_category.html', context)


@login_required
def create_course(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Kurs döretmek isleseňiz ilki mugallym bolmaly !!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            Category = form.cleaned_data['Category']
            slug = Category.id
            messages.success(request, f'Kurs üstünlikli döredildi !!')
            return redirect('/courses/' + str(slug))
    else:
        form = CourseForm(initial={'Creator':request.user.id, 'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_course.html', context)


@login_required
def create_lesson(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Sapak döretmek isleseňiz ilki mugallym bolmaly !!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = LessonForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            Course = form.cleaned_data['Course']
            slug = Course.slug
            messages.success(request, f'Sapak üstünlikli döredildi !!')
            return redirect('/Create/Lesson')
    else:
        form = LessonForm(initial={'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_lesson.html', context)


def view_404(request, exception):
    return render(request, '404.html')

def view_403(request, exception):
    return render(request, '403.html')

def view_500(request):
    return render(request, '500.html')

# def get(self,request,course_slug,lesson_slug,*args,**kwargs):
#
#     course_qs = Course.objects.filter(slug=course_slug)
#     if course_qs.exists():
#         course = course_qs.first()
#     lesson_qs = course.lessons.filter(slug=lesson_slug)
#     if lesson_qs.exists():
#         lesson = lesson_qs.first()
#     user_membership = UserMembership.objects.filter(user=request.user).first()
#     user_membership_type = user_membership.membership.membership_type
#
#     course_allowed_membership_type = course.allowed_memberships.all()
#     context = {'lessons':None}
#
#     if course_allowed_membership_type.filter(membership_type=user_membership_type).exists():
#         context = {'lesson':lesson}
#
#     return render(request,'courses/lesson_detail.html',context)
