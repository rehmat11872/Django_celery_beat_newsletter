from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import MessageBoard
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.decorators import user_passes_test
from .models import *
from .forms import *
from .tasks import *
from django.views import View
# Create your views here.

class MessageBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'board/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messageboard = get_object_or_404(MessageBoard, id=1)
        form = MessageCreateForm()
        context['messageboard'] = messageboard
        context['form'] = form
        
        return context

    def post(self, request, *args, **kwargs):
        messageboard = get_object_or_404(MessageBoard, id=1)

        if request.user not in messageboard.subscribers.all():
            messages.warning(request, 'You need to be Subscribed!')
            return redirect('messageboard')

        form = MessageCreateForm(request.POST)
        if form.is_valid():
            # Save the message, but don't commit to DB yet
            message = form.save(commit=False)
            message.author = request.user
            message.messageboard = messageboard
            message.save()
            send_email(message)
        else:
            messages.warning(request, 'Form submission is invalid')

        return redirect('messageboard')


class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        messageboard = get_object_or_404(MessageBoard, id=1)

        if request.user not in messageboard.subscribers.all():
            messageboard.subscribers.add(request.user)
        else:
            messageboard.subscribers.remove(request.user)
        return redirect('messageboard')
    





def send_email(message):
    messageboard = message.messageboard 
    subscribers = messageboard.subscribers.all()
    
    for subscriber in subscribers: 
        subject = f'New Message from {message.author.profile.name}'
        body = f'{message.author.profile.name}: {message.body}\n\nRegards from\nMy Message Board'
        
        send_email_task.delay(subject, body, subscriber.email)
        
#         email_thread = threading.Thread(target=send_email_thread, args=(subject, body, subscriber))
#         email_thread.start()

# def send_email_thread(subject, body, subscriber):        
#     email = EmailMessage(subject, body, to=[subscriber.email])
#     email.send()



def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def newsletter(request):
    return render(request, 'board/newsletter.html')



# class NewsletterView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
#     template_name = 'board/newsletter.html'
#     def test_func(self):
#         return self.request.user.is_staff

