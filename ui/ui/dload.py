import os
from django.conf import settings
from django.http import HttpResponse

def download():
    # file_path = os.path.join(settings.MEDIA_ROOT, path)
    # file_path = os.path
    # if os.path.exists(file_path):
    # with open(file_path, 'rb') as fh:
    #     response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
    #     response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    #     return response
    # raise Http404

	response = HttpResponse(mimetype='text/plain')
	response['Content-Disposition'] = 'attachment; filename="%s.txt"' % p.uuid
	response.write(p.body)


download()