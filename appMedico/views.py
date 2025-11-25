from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from appMedico.models import Usuario, Doctor, Paciente, Atencion

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # REDIRECCIÓN SEGÚN EL ROL
            if user.rol == "admin":
                return redirect("dashboard_admin")
            elif user.rol == "doctor":
                return redirect("dashboard_doctor")
            else:
                return redirect("dashboard_user")

        return render(request, "auth/login.html", {"error": "Credenciales inválidas"})

    return render(request, "auth/login.html")



def logout_view(request):
    logout(request)
    return redirect("login")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        rol = request.POST["rol"]

        user = Usuario.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            rol=rol
        )

        # Crear perfiles según rol
        if rol == "doctor":
            Doctor.objects.create(usuario=user, especialidad="", telefono="")
        elif rol == "paciente":
            Paciente.objects.create(usuario=user, fecha_nacimiento="2000-01-01", direccion="")

        return redirect("login")

    return render(request, "auth/signup.html")



@login_required
def dashboard_admin(request):
    if request.user.rol != "admin":
        return redirect("login")
    return render(request, "admin/dashboardAdmin.html")


@login_required
def dashboard_doctor(request):
    if request.user.rol != "doctor":
        return redirect("login")
    return render(request, "doctor/dashboardDoctor.html")


@login_required
def dashboard_user(request):
    if request.user.rol != "paciente":
        return redirect("login")
    return render(request, "paciente/dashboardUser.html")



@login_required
def doctores_list(request):
    if request.user.rol != "admin":
        return redirect("login")
    doctores = Doctor.objects.all()
    return render(request, "admin/doctores_list.html", {"object_list": doctores})


@login_required
def pacientes_list(request):
    if request.user.rol != "admin":
        return redirect("login")
    pacientes = Paciente.objects.all()
    return render(request, "admin/pacientes_list.html", {"object_list": pacientes})


@login_required
def atenciones_list(request):
    if request.user.rol != "admin":
        return redirect("login")
    atenciones = Atencion.objects.all()
    return render(request, "admin/atenciones_list.html", {"object_list": atenciones})



@login_required
def doctor_form(request, id=None):
    if request.user.rol != "admin":
        return redirect("login")

    doctor = Doctor.objects.filter(id=id).first()

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        especialidad = request.POST["especialidad"]
        telefono = request.POST["telefono"]

        if doctor:  # EDITAR
            u = doctor.usuario
            u.first_name = first_name
            u.last_name = last_name
            u.email = email
            u.save()

            doctor.especialidad = especialidad
            doctor.telefono = telefono
            doctor.save()

        else:  # CREAR
            password = request.POST["password"]

            u = Usuario.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                rol="doctor"
            )

            doctor = Doctor.objects.create(
                usuario=u,
                especialidad=especialidad,
                telefono=telefono
            )

        return redirect("doctores_list")

    return render(request, "admin/doctor_form.html", {"doctor": doctor})


@login_required
def doctor_delete(request, id):
    if request.user.rol != "admin":
        return redirect("login")

    doctor = get_object_or_404(Doctor, id=id)

    if request.method == "POST":
        doctor.usuario.delete()
        doctor.delete()
        return redirect("doctores_list")

    return render(request, "common/delete_confirm.html", {"objeto": doctor})



@login_required
def paciente_form(request, id=None):
    if request.user.rol != "admin":
        return redirect("login")

    paciente = Paciente.objects.filter(id=id).first()

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        direccion = request.POST["direccion"]

        if paciente:
            u = paciente.usuario
            u.first_name = first_name
            u.last_name = last_name
            u.email = email
            u.save()

            paciente.fecha_nacimiento = fecha_nacimiento
            paciente.direccion = direccion
            paciente.save()

        else:
            password = request.POST["password"]

            u = Usuario.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                rol="paciente"
            )

            paciente = Paciente.objects.create(
                usuario=u,
                fecha_nacimiento=fecha_nacimiento,
                direccion=direccion
            )

        return redirect("pacientes_list")

    return render(request, "admin/paciente_form.html", {"paciente": paciente})


@login_required
def paciente_delete(request, id):
    if request.user.rol != "admin":
        return redirect("login")

    paciente = get_object_or_404(Paciente, id=id)

    if request.method == "POST":
        paciente.usuario.delete()
        paciente.delete()
        return redirect("pacientes_list")

    return render(request, "common/delete_confirm.html", {"objeto": paciente})



@login_required
def atencion_form(request):
    if request.user.rol != "admin":
        return redirect("login")

    doctores = Doctor.objects.all()
    pacientes = Paciente.objects.all()

    if request.method == "POST":
        doctor_id = request.POST["doctor"]
        paciente_id = request.POST["paciente"]
        fecha = request.POST["fecha"]
        descripcion = request.POST["descripcion"]
        diagnostico = request.POST["diagnostico"]

        Atencion.objects.create(
            doctor_id=doctor_id,
            paciente_id=paciente_id,
            fecha=fecha,
            descripcion=descripcion,
            diagnostico=diagnostico
        )
        return redirect("atenciones_list")

    return render(request, "admin/atencion_form.html", {
        "doctores": doctores,
        "pacientes": pacientes
    })


@login_required
def atencion_edit(request, id):
    if request.user.rol != "admin":
        return redirect("login")

    atencion = get_object_or_404(Atencion, id=id)
    doctores = Doctor.objects.all()
    pacientes = Paciente.objects.all()

    if request.method == "POST":
        atencion.doctor_id = request.POST["doctor"]
        atencion.paciente_id = request.POST["paciente"]
        atencion.fecha = request.POST["fecha"]
        atencion.descripcion = request.POST["descripcion"]
        atencion.diagnostico = request.POST["diagnostico"]
        atencion.save()

        return redirect("atenciones_list")

    return render(request, "admin/atencion_edit.html", {
        "atencion": atencion,
        "doctores": doctores,
        "pacientes": pacientes
    })


@login_required
def atencion_delete(request, id):
    if request.user.rol != "admin":
        return redirect("login")

    atencion = get_object_or_404(Atencion, id=id)

    if request.method == "POST":
        atencion.delete()
        return redirect("atenciones_list")

    return render(request, "common/delete_confirm.html", {"objeto": atencion})



@login_required
def doctor_pacientes(request):
    if request.user.rol != "doctor":
        return redirect("login")

    doctor = request.user.doctor
    pacientes = Paciente.objects.filter(atencion__doctor=doctor).distinct()

    return render(request, "doctor/doctor_pacientes.html", {"pacientes": pacientes})


@login_required
def doctor_atenciones(request):
    if request.user.rol != "doctor":
        return redirect("login")

    doctor = request.user.doctor
    atenciones = Atencion.objects.filter(doctor=doctor)

    return render(request, "doctor/doctor_atenciones.html", {"atenciones": atenciones})



@login_required
def paciente_atenciones(request):
    if request.user.rol != "paciente":
        return redirect("login")

    paciente = request.user.paciente
    atenciones = Atencion.objects.filter(paciente=paciente)

    return render(request, "paciente/paciente_atenciones.html", {"atenciones": atenciones})
