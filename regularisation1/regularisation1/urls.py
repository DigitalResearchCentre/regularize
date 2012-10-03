from django.conf.urls import patterns, include, url

#from input.views import regularization, change, show_original
# from birmingham.views import pickText
# from sampleJSON.views import collate, regularize, getWitnesses, getTokens
# from jsRegularize.views import getBaseWitnesses, getBaseTokens, loadInterface
# from jsRegularize.views import saveRules, getRules, recollate, saveRegWitnesses
# from jsRegularize.views import loadViewReg, getRegWitnesses, loadInformationWindow
# from jsRegularize.views import saveInformationWindow, getInformationWindow, changeRule
# from jsRegularize.views import deleteRule, getNextEntity, getPreviousEntity
# from jsRegularize.views import getEntityApi


from jsRegularize.views import regularization, postSelectedWitnesses, chooseRuleSetsInterface
from jsRegularize.views import postSelectedRuleSets, loadRegularizationInterface
from jsRegularize.views import postNewRule, postEntireReg, viewEntireReg
from jsRegularize.views import reloadRegularizationInterface


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
    url(r'^regularization/postEntireReg/$', postEntireReg),
    url(r'^regularization/viewEntireReg/$', viewEntireReg),
    url(r'^regularization/reloadRegularizationInterface/$', reloadRegularizationInterface),


    
    # url(r'^regularization/interface/getBaseWitnesses/$', getBaseWitnesses),
    # url(r'^regularization/interface/getBaseTokens/$', getBaseTokens),
    # url(r'^regularization/interface/$', loadInterface),

    # url(r'^regularization/interface/saveRules/$', saveRules),
    # url(r'^regularization/interface/getRules/$', getRules),
    # url(r'^regularization/interface/recollate/$', recollate),
    # url(r'^regularization/interface/saveRegWitnesses/$', saveRegWitnesses),
    # url(r'^regularization/interface/view/$', loadViewReg),
    # url(r'^regularization/interface/getRegWitnesses/$', getRegWitnesses),
    # url(r'^regularization/interface/informationWindow/$', loadInformationWindow),
    # url(r'^regularization/interface/saveInformationWindow/$', saveInformationWindow),
    # url(r'^regularization/interface/getInformationWindow/$', getInformationWindow),
    # url(r'^regularization/interface/changeRule/$', changeRule),
    # url(r'^regularization/interface/deleteRule/$', deleteRule),
    # url(r'^regularization/interface/getNextEntity/$', getNextEntity),
    # url(r'^regularization/interface/getPreviousEntity/$', getPreviousEntity),

    # #testing urls
    # url(r'^regularization/interface/getEntityApi/$', getEntityApi),
)

# if settings.DEBUG:
#     urlpatterns += patterns('',
#                             #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/media'}),
#         (r'', include('staticfiles.urls')),
#     )
