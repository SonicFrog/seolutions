from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
               url(r'^$', views.UserLoginView.as_view(),
                   name="login"),
               url(r'^check$', views.UserLoginCheckView.as_view(),
                   name="login-check"),
               url(r'^out$', views.UserLogoutView.as_view(),
                   name='login-out'),
)
