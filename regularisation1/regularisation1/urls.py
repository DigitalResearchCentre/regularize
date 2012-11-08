from django.conf.urls import patterns, include, url
from jsRegularize.views import regularization, postSelectedWitnesses, chooseRuleSetsInterface
from jsRegularize.views import postSelectedRuleSets, loadRegularizationInterface
from jsRegularize.views import postNewRule, changeRules, postRecollate
from jsRegularize.views import sendRecollate, getBaseTokens, postEntity, sendEntity

from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'regularisation1.views.home', name='home'),
    # url(r'^regularisation1/', include('regularisation1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^regularization/$', regularization),
    url(r'^regularization/postSelectedWitnesses/$', postSelectedWitnesses),
    url(r'^regularization/chooseRuleSetsInterface/$', chooseRuleSetsInterface),
    url(r'^regularization/postSelectedRuleSets/$', postSelectedRuleSets),
    url(r'^regularization/loadRegularizationInterface/$', loadRegularizationInterface),
    url(r'^regularization/postNewRule/$', postNewRule),
    url(r'^regularization/changeRules/$', changeRules),
    url(r'^regularization/postRecollate/$', postRecollate),
    url(r'^regularization/sendRecollate/$', sendRecollate),
    url(r'^regularization/getBaseTokens/$', getBaseTokens),
    url(r'^regularization/postEntity/$', postEntity),
    url(r'^regularization/sendEntity/$', sendEntity),
)

# if settings.DEBUG:
#     urlpatterns += patterns('',
#                             #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/media'}),
#         (r'', include('staticfiles.urls')),
#     )
