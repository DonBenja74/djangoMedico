from django.urls import path
from . import views

urlpatterns = [

    # LOGIN / LOGOUT / SIGNUP
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),

    # DASHBOARDS 
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/doctor/", views.dashboard_doctor, name="dashboard_doctor"),
    path("dashboard/paciente/", views.dashboard_user, name="dashboard_user"),

    # ADMIN 
    path("admin/doctores/", views.doctores_list, name="doctores_list"),
    path("admin/pacientes/", views.pacientes_list, name="pacientes_list"),
    path("admin/atenciones/", views.atenciones_list, name="atenciones_list"),

    # CRUD DOCTOR
    path("admin/doctores/crear/", views.doctor_form, name="doctor_create"),
    path("admin/doctores/editar/<int:id>/", views.doctor_form, name="doctor_edit"),
    path("admin/doctores/eliminar/<int:id>/", views.doctor_delete, name="doctor_delete"),

    # CRUD PACIENTE
    path("admin/pacientes/crear/", views.paciente_form, name="paciente_create"),
    path("admin/pacientes/editar/<int:id>/", views.paciente_form, name="paciente_edit"),
    path("admin/pacientes/eliminar/<int:id>/", views.paciente_delete, name="paciente_delete"),

    # CRUD ATENCIÓN
    path("admin/atenciones/crear/", views.atencion_form, name="atencion_create"),
    path("admin/atenciones/editar/<int:id>/", views.atencion_edit, name="atencion_edit"),
    path("admin/atenciones/eliminar/<int:id>/", views.atencion_delete, name="atencion_delete"),

    # DOCTOR
    path("doctor/pacientes/", views.doctor_pacientes, name="doctor_pacientes"),
    path("doctor/atenciones/", views.doctor_atenciones, name="doctor_atenciones"),

    # PACIENTE
    path("paciente/atenciones/", views.paciente_atenciones, name="paciente_atenciones"),
]
