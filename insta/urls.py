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
    url(r'^follow/(\w+)$',views.handle_follow,name='follow'),
    url(r'^unfollow/(\w+)$', views.handle_unfollow,name='unfollow'),
    url(r'^like/(\d+)$',views.handle_like,name='like'),
    url(r'^unlike/(\d+)$',views.handle_unlike,name='unlike'),
    url(r'^edit/profile/$',views.edit_profile,name='edit_profile'), 
    url(r'^search/$',views.search,name='search'),
    url(r'^view/pic/(\d+)$',views.comment_image,name='comment'),
    url(r'^update/image/caption/(\d+)$',views.update_bio,name='update_bio'),
    url(r'^image/delete/(\d+)$', views.image_delete, name="delete_image"),
    url(r'^like/comment/(\d+)$',views.handle_like_comment,name='like_comment'),
    url(r'^unlike/comment/(\d+)$', views.handle_unlike_comment, name='unlike_comment'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)