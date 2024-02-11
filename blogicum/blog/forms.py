from django import forms
from django.core.mail import send_mail

from .models import Comment, Post, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }

    def message(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        send_mail(
            subject='Another Beatles member',
            message=f'{first_name} {last_name} пытался опубликовать запись!',
            from_email='birthday_form@blogicum.not',
            recipient_list=['admin@blogicum.not'],
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
