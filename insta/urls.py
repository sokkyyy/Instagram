from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register,name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$',views.logout_user,name='logout'),
    url(r'^profile/(\w+)$', views.user_profile, name='profile'),
    url(r'^new/post/$', views.post_pic,name='new_post'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)