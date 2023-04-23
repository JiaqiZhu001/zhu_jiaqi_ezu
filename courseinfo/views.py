from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from courseinfo.forms import InstructorForm, SectionForm, CourseForm, SemesterForm, StudentForm, RegistrationForm
from courseinfo.models import Instructor, Section, Course, Semester, Student, Registration
from courseinfo.utils import ObjectCreateMixin, PageLinksMixin


# Create your views here.


# class InstructorList(View):
#
#     def get(self, request):
#         return render(request, 'courseinfo/instructor_list.html', {'instructor_list': Instructor.objects.all()})

# class InstructorList(View):
#     page_kwarg = 'page'
#     paginate_by = 25;  # 25 instructors per page
#     template_name = 'courseinfo/instructor_list.html'
#
#     def get(self, request):
#         instructors = Instructor.objects.all()
#         paginator = Paginator(
#             instructors,
#             self.paginate_by
#         )
#         page_number = request.GET.get(
#             self.page_kwarg
#         )
#         try:
#             page = paginator.page(page_number)
#         except PageNotAnInteger:
#             page = paginator.page(1)
#         except EmptyPage:
#             page = paginator.page(
#                 paginator.num_pages)
#         if page.has_previous():
#             prev_url = "?{pkw}={n}".format(
#                 pkw=self.page_kwarg,
#                 n=page.previous_page_number())
#         else:
#             prev_url = None
#         if page.has_next():
#             next_url = "?{pkw}={n}".format(
#                 pkw=self.page_kwarg,
#                 n=page.next_page_number())
#         else:
#             next_url = None
#         context = {
#             'is_paginated':
#                 page.has_other_pages(),
#             'next_page_url': next_url,
#             'paginator': paginator,
#             'previous_page_url': prev_url,
#             'instructor_list': page,
#         }
#         return render(
#             request, self.template_name, context)

class InstructorList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Instructor

    permission_required = 'courseinfo.view_instructor'


class InstructorDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Instructor
    permission_required = 'courseinfo.view_instructor'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        instructor = self.get_object()
        section_list = instructor.sections.all()
        context['section_list'] = section_list
        return context


class InstructorCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    form_class = InstructorForm
    model = Instructor
    permission_required = 'courseinfo.add_instructor'


# class InstructorUpdate(View):
#     form_class = InstructorForm
#     model = Instructor
#     template_name = 'courseinfo/instructor_form_update.html'
#
#     def get_object(self, pk):
#         return get_object_or_404(self.model, pk=pk)
#
#     def get(self, request, pk):
#         instructor = self.get_object(pk)
#         context = {
#             'form': self.form_class(instance=instructor),
#             'instructor': instructor
#         }
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         instructor = self.get_object(pk)
#         bound_form = self.form_class(request.POST, instance=instructor)
#         if bound_form.is_valid():
#             new_instructor = bound_form.save()
#             return redirect(new_instructor)
#         else:
#             context = {
#                 'form': bound_form,
#                 'instructor': instructor
#             }
#             return render(request, self.template_name, context)

class InstructorUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    form_class = InstructorForm
    model = Instructor
    permission_required = 'courseinfo.change_instructor'
    template_name = 'courseinfo/instructor_form_update.html'


class InstructorDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Registration
    success_url = reverse_lazy('courseinfo_registration_list_urlpattern')
    permission_required = 'courseinfo.delete_instructor'

    def get(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        sections = instructor.sections.all()

        if sections.count() > 0:
            return render(
                request,
                'courseinfo/instructor_refuse_delete.html',
                {'instructor': instructor,
                 'sections': sections,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/instructor_confirm_delete.html',
                {'instructor': instructor}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Instructor,
            pk=pk)

    def post(self, request, pk):
        instructor = self.get_object(pk)
        instructor.delete()
        return redirect('courseinfo_instructor_list_urlpattern')


class SectionList(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Section
    permission_required = 'courseinfo.view_section'


class SectionDetail(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    model = Section
    permission_required = 'courseinfo.view_section'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        section = self.get_object()
        semester = section.semester
        course = section.course
        instructor = section.instructor
        registration_list = section.registrations.all()
        context['semester'] = semester
        context['course'] = course
        context['instructor'] = instructor
        context['registration_list'] = registration_list
        return context

    # def get(self, request, pk):
    #     section = get_object_or_404(Section, pk=pk)
    #     semester = section.semester
    #     course = section.course
    #     instructor = section.instructor
    #     registration_list = section.registrations.all()
    #     return render(request, 'courseinfo/section_detail.html',
    #                   {'section': section, 'semester': semester, 'course': course, 'instructor': instructor,
    #                    'registration_list': registration_list})


class SectionCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    form_class = SectionForm
    model = Section
    permission_required = 'courseinfo.add_section'


# class SectionUpdate(View):
#     form_class = SectionForm
#     model = Section
#     template_name = 'courseinfo/section_form_update.html'
#
#     def get_object(self, pk):
#         return get_object_or_404(self.model, pk=pk)
#
#     def get(self, request, pk):
#         section = self.get_object(pk)
#         context = {
#             'form': self.form_class(instance=section),
#             'section': section
#         }
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         section = self.get_object(pk)
#         bound_form = self.form_class(request.POST, instance=section)
#         if bound_form.is_valid():
#             new_section = bound_form.save()
#             return redirect(new_section)
#         else:
#             context = {
#                 'form': bound_form,
#                 'section': section
#             }
#             return render(request, self.template_name, context)

class SectionUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    form_class = SectionForm
    model = Section
    permission_required = 'courseinfo.change_section'
    template_name = 'courseinfo/section_form_update.html'


class SectionDelete(DeleteView):
    permission_required = 'courseinfo.delete_section'

    def get(self, request, pk):
        section = get_object_or_404(Section, pk=pk)
        registrations = section.registrations.all()
        if registrations.count() > 0:
            return render(
                request,
                'courseinfo/section_refuse_delete.html',
                {'section': section,
                 'registrations': registrations,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/section_confirm_delete.html',
                {'section': section}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Section,
            pk=pk)

    def post(self, request, pk):
        section = self.get_object(pk)
        section.delete()
        return redirect('courseinfo_section_list_urlpattern')


class CourseList(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Course
    permission_required = 'courseinfo.view_course'


class CourseDetail(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    model = Course
    permission_required = 'courseinfo.view_course'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        return context


class CourseCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    form_class = CourseForm
    model = Course
    permission_required = 'courseinfo.add_course'


# class CourseUpdate(View):
#     form_class = CourseForm
#     model = Course
#     template_name = 'courseinfo/course_form_update.html'
#
#     def get_object(self, pk):
#         return get_object_or_404(self.model, pk=pk)
#
#     def get(self, request, pk):
#         course = self.get_object(pk)
#         context = {
#             'form': self.form_class(instance=course),
#             'course': course
#         }
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         course = self.get_object(pk)
#         bound_form = self.form_class(request.POST, instance=course)
#         if bound_form.is_valid():
#             new_course = bound_form.save()
#             return redirect(new_course)
#         else:
#             context = {
#                 'form': bound_form,
#                 'course': course
#             }
#             return render(request, self.template_name, context)

class CourseUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    form_class = CourseForm
    model = Course
    permission_required = 'courseinfo.change_course'

    template_name = 'courseinfo/course_form_update.html'


class CourseDelete(DeleteView):
    permission_required = 'courseinfo.delete_course'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        sections = course.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseinfo/course_refuse_delete.html',
                {'course': course,
                 'sections': sections,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/course_confirm_delete.html',
                {'course': course}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Course,
            pk=pk)

    def post(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return redirect('courseinfo_course_list_urlpattern')


class SemesterList(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Semester
    permission_required = 'courseinfo.view_semester'


class SemesterDetail(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    model = Semester
    permission_required = 'courseinfo.view_semester'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        semester = self.get_object()
        section_list = semester.sections.all()
        context['section_list'] = section_list
        return context

    #
    # def get(self, request, pk):
    #     semester = get_object_or_404(Semester, pk=pk)
    #     section_list = semester.sections.all()
    #     return render(request, 'courseinfo/semester_detail.html', {'semester': semester, 'section_list': section_list})


class SemesterCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    form_class = SemesterForm
    model = Semester
    permission_required = 'courseinfo.add_semester'


# class SemesterUpdate(View):
#     form_class = SemesterForm
#     model = Semester
#     template_name = 'courseinfo/semester_form_update.html'
#
#     def get_object(self, pk):
#         return get_object_or_404(self.model, pk=pk)
#
#     def get(self, request, pk):
#         semester = self.get_object(pk)
#         context = {
#             'form': self.form_class(instance=semester),
#             'semester': semester
#         }
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         semester = self.get_object(pk)
#         bound_form = self.form_class(request.POST, instance=semester)
#         if bound_form.is_valid():
#             new_course = bound_form.save()
#             return redirect(new_course)
#         else:
#             context = {
#                 'form': bound_form,
#                 'semester': semester
#             }
#             return render(request, self.template_name, context)


class SemesterUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    form_class = SemesterForm
    model = Semester
    permission_required = 'courseinfo.change_semester'
    template_name = 'courseinfo/section_form_update.html'


class SemesterDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = 'courseinfo.delete_semester'
    def get(self, request, pk):
        semester = get_object_or_404(Semester, pk=pk)
        sections = semester.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseinfo/semester_refuse_delete.html',
                {'semester': semester,
                 'sections': sections,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/semester_confirm_delete.html',
                {'semester': semester}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Semester,
            pk=pk)

    def post(self, request, pk):
        semester = self.get_object(pk)
        semester.delete()
        return redirect('courseinfo_semester_list_urlpattern')


# class StudentList(View):
#     page_kwarg = 'page'
#     paginate_by = 25;  # 25 instructors per page
#     template_name = 'courseinfo/student_list.html'
#
#     def get(self, request):
#         students = Student.objects.all()
#         paginator = Paginator(
#             students,
#             self.paginate_by
#         )
#         page_number = request.GET.get(
#             self.page_kwarg
#         )
#         try:
#             page = paginator.page(page_number)
#         except PageNotAnInteger:
#             page = paginator.page(1)
#         except EmptyPage:
#             page = paginator.page(
#                 paginator.num_pages)
#         if page.has_previous():
#             prev_url = "?{pkw}={n}".format(
#                 pkw=self.page_kwarg,
#                 n=page.previous_page_number())
#         else:
#             prev_url = None
#         if page.has_next():
#             next_url = "?{pkw}={n}".format(
#                 pkw=self.page_kwarg,
#                 n=page.next_page_number())
#         else:
#             next_url = None
#         context = {
#             'is_paginated':
#                 page.has_other_pages(),
#             'next_page_url': next_url,
#             'paginator': paginator,
#             'previous_page_url': prev_url,
#             'student_list': page,
#         }
#         return render(
#             request, self.template_name, context)

class StudentList(LoginRequiredMixin, PermissionRequiredMixin,PageLinksMixin, ListView):
    paginate_by = 25
    model = Student
    permission_required = 'courseinfo.view_student'


class StudentDetail(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    model = Student
    permission_required = 'courseinfo.view_student'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        student = self.get_object()
        registration_list = student.registrations.all()
        context['registration_list'] = registration_list
        return context


class StudentCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    form_class = StudentForm
    model = Student
    permission_required = 'courseinfo.add_student'


# class StudentUpdate(View):
#     form_class = StudentForm
#     model = Student
#     template_name = 'courseinfo/student_form_update.html'
#
#     def get_object(self, pk):
#         return get_object_or_404(self.model, pk=pk)
#
#     def get(self, request, pk):
#         student = self.get_object(pk)
#         context = {
#             'form': self.form_class(instance=student),
#             'student': student
#         }
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         student = self.get_object(pk)
#         bound_form = self.form_class(request.POST, instance=student)
#         if bound_form.is_valid():
#             new_student = bound_form.save()
#             return redirect(new_student)
#         else:
#             context = {
#                 'form': bound_form,
#                 'student': student
#             }
#             return render(request, self.template_name, context)


class StudentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = StudentForm
    model = Student
    template_name = 'courseinfo/student_form_update.html'
    permission_required = 'courseinfo.change_student'


class StudentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'courseinfo.delete_student'

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        registrations = student.registrations.all()
        if registrations.count() > 0:
            return render(
                request,
                'courseinfo/student_refuse_delete.html',
                {'student': student,
                 'registrations': registrations,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/student_confirm_delete.html',
                {'instructor': student}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Student,
            pk=pk)

    def post(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return redirect('courseinfo_student_list_urlpattern')


class RegistrationList(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Registration
    permission_required = 'courseinfo.view_registration'


class RegistrationDetail(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    permission_required = 'courseinfo.view_registration'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        registration = self.get_object()
        return context

    def get(self, request, pk):
        registration = get_object_or_404(Registration, pk=pk)
        return render(request, 'courseinfo/registration_detail.html', {'registration': registration})


class RegistrationCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    form_class = RegistrationForm
    model = Registration
    permission_required = 'courseinfo.add_registration'


# class RegistrationUpdate(View):
#     form_class = RegistrationForm
#     model = Registration
#     template_name = 'courseinfo/registration_form_update.html'
#
#     def get_object(self, pk):
#         return get_object_or_404(self.model, pk=pk)
#
#     def get(self, request, pk):
#         registration = self.get_object(pk)
#         context = {
#             'form': self.form_class(instance=registration),
#             'registration': registration
#         }
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         registration = self.get_object(pk)
#         bound_form = self.form_class(request.POST, instance=registration)
#         if bound_form.is_valid():
#             new_registration = bound_form.save()
#             return redirect(new_registration)
#         else:
#             context = {
#                 'form': bound_form,
#                 'registration': registration
#             }
#             return render(request, self.template_name, context)

class RegistrationUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    form_class = RegistrationForm
    model = RegistrationForm
    template_name = 'courseinfo/registration_form_update.html'
    permission_required = 'courseinfo.change_registration'


# class RegistrationDelete(View):
#
#     def get(self, request, pk):
#         registration = self.get_object(pk)
#         return render(
#             request,
#             'courseinfo/registration_confirm_delete.html',
#             {'registration': registration}
#         )
#
#     def get_object(self, pk):
#         registration = get_object_or_404(
#             Registration,
#             pk=pk
#         )
#         return registration
#
#     def post(self, request, pk):
#         registration = self.get_object(pk)
#         registration.delete()
#         return redirect('courseinfo_registration_list_urlpattern')


class RegistrationDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Registration
    success_url = reverse_lazy('courseinfo_registration_list_urlpattern')
    permission_required = 'courseinfo.delete_registration'
