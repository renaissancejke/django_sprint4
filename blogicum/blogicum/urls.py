from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path
from django.views.generic.edit import CreateView

# from blog.forms import CustomUserCreationForm

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
        ),
        name='registration',
    ),
]
