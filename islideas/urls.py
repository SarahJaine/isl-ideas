from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(),
        name='home'),
    url(r'^new/$', NewIdeaList.as_view(),
        name='new'),
    url(r'^tags/$', TagList.as_view(),
        name='tag_list'),
    url(r'^ideas/(?P<slug>[-\w]+)$',
        IdeaDetail.as_view(),
        name='idea_detail'),
    url(r'^add/$', IdeaCreate.as_view(),
        name='idea_form'),
    url(r'^ideas/(?P<slug>[-\w]+)/edit/$',
        IdeaUpdate.as_view(),
        name='idea_edit'),
    url(r'^ideas/(?P<slug>[-\w]+)/delete/$',
        IdeaDelete.as_view(),
        name='idea_confirm_delete'),
    url(r'^ideas/(?P<idea_slug>[-\w]+)/commentedit/(?P<pk>[-\w]+)/$',
        CommentUpdate.as_view(),
        name='comment_edit'),
    url(r'^ideas/(?P<idea_slug>[-\w]+)/commentdelete/(?P<pk>[-\w]+)/$',
        CommentDelete.as_view(),
        name='comment_confirm_delete'),
    url(r'^tags/(?P<slug>[-\w]+)$',
        TagDetail.as_view(),
        name='tag'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/rq/', include('django_rq.urls')),
    url(r'^logout/$', logout_then_login, name='logout'),
    url('', include('pythonisl.urls')),
    # url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^ideas/$', RedirectView.as_view(
        pattern_name='home', permanent=True)),
]
