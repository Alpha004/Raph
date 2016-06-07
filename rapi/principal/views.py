from cStringIO import StringIO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from reportlab.lib import colors
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib.pagesizes import A4, cm
from reportlab.platypus import Paragraph, Table, TableStyle
from models import Atencion , Personal, Puesto, Edicion, Area, Cama, Paciente
from django.core import  serializers
from principal.forms import Login, CreateUser
from rapi import settings
from rapi.settings import BASE_DIR


@login_required
def visualizarListaAtenciones(request):

    ObjAtenciones = Atencion.objects.all()
    return render(request, "rapi/rapi_listatencion.html",locals())

def reporteGen(request):
    fecha_actual = datetime.date.today()
    USUARIO_ = request.user
    ATENCIONES = Atencion.objects.filter(TiempoA__day=fecha_actual.day)

    if(request.POST):
        seleccion = request.POST.get('sele1',0)

        if(seleccion == "1"):
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=Reportedia-'+'.pdf'

            temp = BytesIO()
            # Create the PDF object, using the StringIO object as its "file."
            p = canvas.Canvas(temp,pagesize=A4)
            ancho,alto = A4
            print ancho,alto
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'RAPH')

            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Registro de Atencion de Pacientes Hospitalizados')
            url_imagen_logo = BASE_DIR + '/principal/static/imagenes/logo_essalud.jpg'
            p.drawImage( url_imagen_logo,440,690,width=110,height=110)

            p.line(30,710,560,710)
            p.drawString(255,685,'REPORTE DEL DIA')
            p.drawString(30,660,'Nombre de Usuario:')
            p.drawString(30,630,'Fecha de Emision:')
            p.drawString(30,600,'Cantidad de Atenciones:')
            p.drawString(420,660,USUARIO_.username)
            p.drawString(420,630,str(fecha_actual))
            p.drawString(420,600,str(ATENCIONES.count()))
            p.setStrokeColor(black)
            p.setFont('Helvetica-Bold',16)
            p.drawString(30,570,"Tabla de Atenciones")
            p.setFont('Helvetica',14)
            p.drawString(30,530,"Atendidos = A")
            p.drawString(30,515,"No Atendidos = N")

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.line(30, 65,560,65)
            p.drawString(30,50,"Reporte del Dia: " + str(format(fecha_actual,"%d-%m-%y"))+" - Registro de Atencion de Pacientes Hospitalizados")

            styles = getSampleStyleSheet()
            styleBH = styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 10

            numero_rapi = Paragraph('''Nro''', styleBH)
            cama_rapi = Paragraph('''Cama''', styleBH)
            hora_rapi = Paragraph('''Hora''', styleBH)
            perso_rapi = Paragraph('''Personal''', styleBH)
            descr_rapi = Paragraph('''Descripcion''', styleBH)
            edit_rapi = Paragraph('''Ediciones''', styleBH)
            esta_rapi = Paragraph('''Estado''', styleBH)

            data = []

            data.append([numero_rapi, cama_rapi, hora_rapi, perso_rapi, descr_rapi, edit_rapi, esta_rapi])

            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7

            high = 480
            this_atencion = None
            for Natencion in ATENCIONES:
                # try:
                #     personal_seleccionado = Personal.objects.get(id=Natencion.ID_P)
                # except Exception as e:
                #     personal_seleccionado ="No se asigno un profesional a la atencion"
                estado = None
                if Natencion.Estado==True:
                    estado = "A"
                else:
                    estado = "N"
                this_atencion = [Natencion.id,Natencion.NroCamaA,format(Natencion.TiempoA.time(),"%H:%M:%S"),
                                 Natencion.ID_P.NombreS + ", " + Natencion.ID_P.ApellidoS,Natencion.DescripcionA,
                                 Natencion.NroEdiciones,estado]
                    # try:
                    #     this_atencion = [Natencion.id,Natencion.NroCamaA,Natencion.TiempoA.hour,
                    #              personal_seleccionado.NombreS + ", " + personal_seleccionado.ApellidoS,Natencion.DescripcionA,
                    #              Natencion.NroEdiciones,estado]
                    # except Exception as e:
                    #     this_atencion = [Natencion.id,Natencion.NroCamaA,Natencion.TiempoA.hour,
                    #              "No se registro nadie","Esta campo se considera no registrado tambien",
                    #              Natencion.NroEdiciones,estado]
                data.append(this_atencion)
                high = high -25


            print(data[0][0],data[1][0])
            table = Table(data, colWidths=[1*cm,1.4*cm,2*cm,4.5*cm, 7*cm, 1.7 *cm, 1.6 * cm])
            table.setStyle(TableStyle([('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0),(-1,-1), 0.25, colors.black), ]))
            table.wrapOn(p,ancho,alto)
            table.drawOn(p,30,high)

            p.showPage()
            p.save()
            newpdf=temp.getvalue()
            temp.close()
            # Get the value of the StringIO buffer and write it to the response.
            response.write(newpdf)
            print "termino"
            return response

        if(seleccion == "2"):
            pass
        if(seleccion == "3"):
            pass
        else:
            return render(request, "rapi/rapi_reportes.html")

    return render(request, "rapi/rapi_reportes.html")

@login_required
def visualizarPrincipal(request):
    return render(request, "rapi/rapi_principal.html")


def visualizarLogin(request):
    # next = request.GET.get('next', '/index/')
    if(request.method=='POST'):
        usuario = request.POST['username']
        contra = request.POST['password']
        #form = Login(request.POST)
        # if form.is_valid():
        #     usuario = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        acceso = authenticate(username=usuario,password=contra)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return HttpResponseRedirect('/index')
            else:
                return HttpResponse('usuario inactivo.')
                    # ("rapi/rapi_login.html", context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    # else:
    #     form = Login
    return render(request,"rapi/rapi_login.html")

def Logout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)

@login_required
def visualizarAlertas(request):
    personal = Personal.objects.all()
    alertas = Atencion.objects.filter(Estado=False,ID_P=None, NroEdiciones=0)
    return render(request, "rapi/rapi_ALERTAS.html",locals())

@login_required
def visualizarReporte(request):
   return render(request, "rapi/rapi_reportes.html")


def visualizarAlertasAjax(request):
    datos =""
    if(request.GET):
        id_personal = request.GET['id']
        persona = Personal.objects.values(id_personal)
        datos = serializers.serialize('json',persona,fields=('NombreS','ApellidoS'))
    return HttpResponse(datos,content_type="application/json")


def editaralertas1(request, pk):
    atencion = Atencion.objects.get(pk=pk)
    personal = Personal.objects.all()
    # if request.POST:
    #     if request.POST['atendido']:
    atencion.Nombre_U = request.user
    atencion.Estado = True
    edition_created= Edicion.objects.create(TiempoE=timezone.now(),TotalE=1)
    edition_created.IdUsuarios.add(request.user)
    atencion.NroEdiciones=edition_created
    atencion.save()
    return redirect(reverse('alertas2',kwargs={'pk':pk}))
    # else:
    #         return redirect(reverse('alertas'))
    # return render(request, 'rapi/rapi_ALERTAS.html')


def editaralertas2(request, pk):
    atencion = Atencion.objects.get(pk=pk)
    personal = Personal.objects.all()
    # if request.POST:
    #     if request.POST['atendido']:
    atencion.Nombre_U = request.user
    edition_created= Edicion.objects.create(TiempoE=timezone.now(),TotalE=1)
    edition_created.IdUsuarios.add(request.user)
    atencion.NroEdiciones=edition_created
    atencion.save()
    return redirect(reverse('alertas2',kwargs={'pk':pk}))

@login_required
def editarAlertas(request, pk):
    atencion = Atencion.objects.get(pk=pk)
    personal = Personal.objects.all()
    if request.POST:
        id_personal = int(request.POST.get('ListaPersonal',None))
        if(id_personal>0):
            personal_atendio = Personal.objects.get(id=id_personal)
            atencion.ID_P = personal_atendio
        atencion.DescripcionA = request.POST.get('descripcion-atencion',None)
        atencion.save()
        return redirect(reverse('alertas'))
    else:
        return render(request, "rapi/rapi_editalertas.html",locals())


def reporteAjax(request):
    if(request.method == 'POST'):
        fecha_actual = datetime.datetime.now()
        inicio_semana = timezone.now() - datetime.timedelta(days=7)
        fin_semana= timezone.now()
        opcion = request.POST['seleccion']
        print opcion
        atencionesD=0
        atencionesS=0
        atencionesM=0
        dato1=None

        if(opcion=="1"):
            atencionesD = Atencion.objects.filter(TiempoA__day=fecha_actual.day)
            dato1 = serializers.serialize('json',atencionesD)
        if(opcion=="2"):
            atencionesS = Atencion.objects.filter(TiempoA__range=[inicio_semana,fin_semana])
            dato1 = serializers.serialize('json',atencionesS)
        if(opcion=="3"):
            atencionesM = Atencion.objects.filter(TiempoA__month=fecha_actual.month)
            dato1 = serializers.serialize('json',atencionesM)
        # atenciones1 = Atencion.objects.filter(TiempoA__lte=datetime.date.today())
        return HttpResponse(dato1,content_type='application/json')

def AdministradorView(request):
    return render(request,'rapi/rapi_admin.html')


def CrearUsuarioView(request):
    if(request.POST):
        createuserform = CreateUser(request.POST)
        if(createuserform.is_valid()):
            createuserform.save()
            mensaje = "Usuario creado con exito"
            return render(request,'rapi/rapi_admin.html',locals())
        else:
            return render(request,'rapi/rapi_admin.html',locals())
    else:
        createuserform = CreateUser()
    return render(request,'rapi/rapi_crearuser.html',locals())

def busquedaView(request):
    return render(request,'rapi/rapi_busquedaA.html',locals())

def BusquedaAjax(request):
    pass
    #return HttpResponse(,content_type='application/json')
def cambiarpswView(request):
    users = User.objects.all()
    return render(request,'rapi/rapi_psw.html',locals())


def informacionUserView(request):
    users = User.objects.all()
    return render(request,'rapi/rapi_infouser.html',locals())


def ImprimirInformacion(request):
    pass


def cambiarpswViewAjax(request):
    pass


def informacionUserViewAjax(request):
    pass