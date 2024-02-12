from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Comment, Post, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                            attrs={'type': 'datetime-local'})
        }

    def message(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        send_mail(
            subject='Another Beatles member',
            message=f'{first_name} {last_name} пытался опубликовать запись!',
            from_email='birthday_form@blogicum.not',
            recipient_list=[settings.RECIPIENT_EMAIL],
            fail_silently=True,
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
