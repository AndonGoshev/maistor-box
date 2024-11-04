from django.urls import path, include

from maistorbox.accounts.views import RegularUserRegistrationView, ContractorUserRegistrationView


# urlpatterns = [
#     path('regular-user/', include(
#         path('registration/', )
#     ))
# ]


urlpatterns = [
    path('regular-user/', include([
        path('registration/', RegularUserRegistrationView.as_view(), name='regular-user-registration'),
    ])),
    path('contractors/', include([
        path('registration/', ContractorUserRegistrationView.as_view(), name='contractor-registration')
    ]))
]