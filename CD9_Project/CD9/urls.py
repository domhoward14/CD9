from django.conf.urls import patterns, url
import rest_framework.authtoken
import views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^api/userprofiles/$', views.UserProfiles.as_view()),
        url(r'^api/get_ids/$', views.GetIds.as_view()),
        url(r'^api/update_profile/(?P<pk>\d+)/$', views.UpdateUserProfile.as_view()),
        url(r'^api/add_another_teen/(?P<pk>\d+)/$', views.AddAnotherTeen.as_view()),
        url(r'^api/texts/$', views.Texts_View.as_view()),
        url(r'^api/apps/$', views.Apps.as_view()),
        url(r'^api/phone_calls/$', views.PhoneCall.as_view()),
        url(r'^api/web_history/$', views.WebHistory.as_view()),
        url(r'^api/add_parent/$', views.AddParent.as_view()),
        url(r'^api/new_user/$', views.CreateNewUser),
        url(r'^api/verify/$', views.TokenUpdater),
        url(r'^api/extend/$', views.TokenExtender),
        url(r'^api/userlist/$', views.UserList.as_view()),
        url(r'^api/update_token/$', views.TokenUpdater),
        url(r'^api/test/$', views.test),
        url(r'^api/processData/$', views.processAllData),
        url(r'^api/ping/$', views.ping.as_view()),
        url(r'^api/ping_checker/$', views.ping_checker),
        url(r'^logout/$', views.user_logout),
        url(r'^login/$', views.loginUser),
        url(r'^daniel/$', views.daniel),
        url(r'^settings/$', views.settings),
        url(r'^daniel2/$', views.daniel2),
        url(r'^test/$', views.test),
    )
