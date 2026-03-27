from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("select-role/", views.select_role, name="select_role"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("client/onboarding/", views.client_onboarding, name="client_onboarding"),
    path("advocate/onboarding/", views.advocate_onboarding, name="advocate_onboarding"),
    path("case/add/", views.create_case, name="create_case"),
    path("hearing/add/", views.create_hearing, name="create_hearing"),
    path("document/upload/", views.upload_document, name="upload_document"),
    path("task/add/", views.create_task, name="create_task"),
    path("case/<int:case_id>/", views.case_detail, name="case_detail"),
    path("case/<int:case_id>/edit/", views.update_case, name="update_case"),
    path("case/<int:case_id>/delete/", views.delete_case, name="delete_case"),
    path("case/<int:case_id>/download-pdf/", views.download_case_pdf, name="download_case_pdf"),
]
