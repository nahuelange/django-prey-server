# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.base import ContentFile
from preylog.models import Device, API_User, Report, ReportFile
import hashlib
import uuid
import base64


@csrf_exempt
def log(request):
    print "log"
    print request.POST
    print request.GET
    print request.FILES
    return HttpResponse()


@csrf_exempt
def devices(request):
    print "devicess"

    user = authenticate(request)

    try:
        device, new = Device.objects.get_or_create(
                                        title=request.POST['device[title]'],
                                        os_version=request.POST['device[os_version]'],
                                        os=request.POST['device[os]'],
                                        genre=request.POST['device[device_type]'],
                                        user=user,
                                        )
        if new:
            device.key = uuid.uuid4()
            device.save()
    except Exception, e:
        print e
    reponse = '<devices type="array"><device><key>9xy9ne</key><state>ok</state>'\
              + '<title>yaya</title></device></devices>'
    r = HttpResponse('<key>%s</key>' % device.key)
    r.status_code = 201
    return r


@csrf_exempt
def device(request, key):
    print "device"

    user = authenticate(request)

    try:
        device = Device.objects.get(key=key)

        if request.method == "PUT":
            report_data = request.read()
            report = Report(device=device, data=report_data)
            report.save()
            return HttpResponse()

        if device.lost == True:
            response = "<device>\n<status>\n<missing>%s</missing>\n</status>" % device.lost \
                        + "<configuration>\n<current_release>0.5.3</current_release>\n" \
                        + "<post_url>http://localhost/report/%s.xml</post_url>\n" % device.key \
                        + "<delay>20</delay>\n<auto_update>true</auto_update>\n</configuration>\n" \
                        + "<modules>\n" + '<module type="action" active="true" name="system" version="1.5"/>' + "\n" \
                        + '<module type="action" active="true" name="webcam" version="1.5"/>\n</modules>' \
                        + "\n</device>"

            return HttpResponseNotFound(response)
        else:
            response = '<device><status><missing>%s</missing></status>' % device.lost \
                        + '<configuration><current_release>0.5.3</current_release>' \
                        + '<delay>20</delay><auto_update>true</auto_update></configuration>' \
                        + '<modules><module type="action" active="true" name="system" version="1.5"/>' \
                        + '<module type="action" active="true" name="webcam" version="1.5"/></modules></device>'
            return HttpResponse(response)
    except Exception, e:
        print e

    return HttpResponse()


@csrf_exempt
def report(request, key):
    print "report"

    user = authenticate(request)

    try:
        device = Device.objects.get(key=key)
        report = Report(device=device, data=request.POST)
        report.save()
        print request.FILES
        for report_file, data_file in request.FILES.items():
            new_file = ReportFile(report=report)
            new_file.save()
            new_file.filename.save(key + "-" + data_file, ContentFile(request.FILES[report_file].read()))
    except Exception, e:
        print e

    return HttpResponse()


def authenticate(request):
    try:
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            username, passwd = base64.b64decode(auth[1]).split(':')
            user = API_User.objects.get(username=str(username))
            return user

    except Exception, e:
        print e
