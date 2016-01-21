from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^api/userprofiles/$', views.UserProfileList.as_view()),
        url(r'^api/update_profile/(?P<pk>\d+)/$', views.UpdateUserProfile.as_view()),
        url(r'^api/texts/$', views.Texts.as_view()),
        url(r'^api/update_text/(?P<pk>\d+)/$', views.TextsUpdate.as_view()),
        url(r'^api/new_user/$', views.CreateNewUser),

    )

