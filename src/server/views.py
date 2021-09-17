from django.shortcuts import render
import qrcode
import qrcode.image.svg
from io import BytesIO
from .models import RestroomVisitData, Restroom, PrivateRestroom
import hashlib
import datetime
import re
from django.http import JsonResponse
from django.utils import timezone
# Create your views here.
def qrgen(request, code):
    context = {}
    if request.method == "GET":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(code, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()

    return render(request, "qrview.html", context=context)

def error_404_view(request):
  return render(request, "sad404.html")

def qr_scan(request, code):
  try:
    data = code.split("_")
    restroom_visit = RestroomVisitData.objects.get(
      active=True,
      telephone=data[-1],
    )
    telephone = restroom_visit.telephone
    p_restroom = restroom_visit.p_restroom
    key = p_restroom.restroom.key
    hash = hashlib.sha256((telephone+"_"+key).encode()).hexdigest()
    timestamp = data[0]
    timestamp = timestamp.split("+")[0]
    print(timestamp)
    date_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    elapsed_time = datetime.datetime.now() - date_timestamp
    
    total_minutes = abs(int(elapsed_time.total_seconds() / 60))
    print(total_minutes)
    """----Check----"""
    hash_QR = data[1]
    restroom_visit.active = False
    restroom_visit.qr_scan_time = timezone.now()
    restroom_visit.save()

    if total_minutes <= p_restroom.time_left:
      if hash_QR == hash:

        return JsonResponse({"result":"success"}, json_dumps_params={'indent': 4})

      else:
      
        return JsonResponse({"result":"fail", "reason":"The hashed data doesn't match the following query."}, json_dumps_params={'indent': 4})
    else:
      return JsonResponse({"result":"fail", "reason":"The time limit has been exceeded."}, json_dumps_params={'indent': 4})
  except RestroomVisitData.DoesNotExist:
    return JsonResponse({"result":"fail", "reason":"The QR code does not exist. The QR Code may have been tampered with."}, json_dumps_params={'indent': 4})

  




                      
