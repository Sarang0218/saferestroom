from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from server.models import RestroomVisitData, PrivateRestroom, Restroom, Building, Review
# Create your views here.
from server.forms import RestroomVisitDataForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import qrcode
from io import BytesIO
import random
import string
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
import hashlib
import os
from twilio.rest import Client
date_format = '%Y-%m-%d %H:%M:%S'
from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return redirect('home')
@csrf_exempt
def loginuser(request):

    if request.method == 'GET':
        return render(request, 'login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form':AuthenticationForm(), 'error':'비밀번호나 유저이름이 맞지 않습니다.'})
        else:
            login(request, user)
            return redirect('restroom_sign_in_view')

@csrf_exempt
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form':UserCreationForm()})
    else:

        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                # 나중에 추가!!
                return redirect('settings')

            except IntegrityError:
                return render(request, 'signup.html', {'form':UserCreationForm(), 'error':'그 이름은 벌써 사용중입니다.'})
            
            except ValueError:
                return render(request, 'signup.html', {'form':UserCreationForm(), 'error':'이름을 입력해야합니다.'})
        else:
            return render(request, 'signup.html', {'form':UserCreationForm(), 'error':'비밀번호와 비밀번호(확인) 의 값이 같아야합니다!'})


def generate_key():
	S = 32
	random_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))  
	return str(random_key)

def settings_view(request):
  return render(request, "dev.html")


def restroom_sign_in_view(request):
  context = {}
  ratings = []
  titles = []
  template_name = 'form.html'
  form = RestroomVisitDataForm(request.user,request.POST or None)
  buildings = Building.objects.filter(user=request.user)
 
  for h in buildings:
    a = Restroom.objects.filter(building=h)
    for k in a:
      
      try:
        restp = PrivateRestroom.objects.get(restroom=k, owner=request.user)
        titles.append([f"{restp.restroom.building.title}의 {restp.restroom.title}", restp.restroom.key])
        ratings.append(restp.restroom.reviews.all())
       
      except:
        pass     


      


  unioned_rating = Review.objects.none()
  for r_rating in ratings:
    unioned_rating = unioned_rating | r_rating
  contexted_rating = []
  for item in unioned_rating:
    contexted_rating.append([list(range(item.score)), item.text])

  context["restrooms"] = titles
  context["reviews"] = contexted_rating
  if form.is_valid():
    obj = form.save(commit=False)
    data = form.cleaned_data
    try:
      a = RestroomVisitData.objects.filter(telephone=data["telephone"])
      for i in a:
        i.active = False
        i.save()

    except:
      pass

    pwd = str(data["p_restroom"].restroom.key)
    key_ = data["telephone"] + "_" + pwd
    hash = hashlib.sha256(key_.encode()).hexdigest()
    time_stamp = str(timezone.now()).split("+")[0]

    fin_qr_code = time_stamp + "_" + hash + "_" + data["telephone"]
    
    obj.qr = fin_qr_code
    fin_qr_code_a = fin_qr_code.replace(" ", "%20")
    
    obj.save()
    message = f"안녕하세요! {obj.p_restroom.restroom.building.title} {obj.p_restroom.restroom.title}에서 보내는 메세지 입니다. QR코드 링크는: https://ansimhwajangsil.compilingcoder.repl.co/link/{fin_qr_code_a} 이고 유효 시간이 {obj.p_restroom.time_left}분입니다. 의견을 남겨주세요! https://ansimhwajangsil.compilingcoder.repl.co/review/{obj.p_restroom.restroom.key}"
    print(message)

    """obj.p_restroom.restroom.key로 /review/<key>"""
    
    
    
    account_sid = os.environ['account_sid']
    auth_token = os.environ['auth_token']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=message,
                        from_='+14805681135',
                        to=data["telephone"]
                    )


    print(message.sid)
  
    obj.link_recieved_time = timezone.now()

    form = RestroomVisitDataForm(request.user)
    
  context['form']=form
  
  print(context)
  return render(request, template_name, context)
"""
def qr_scan(request, mode, slug):
  try:
    scan = RestroomVisitData.objects.get(qr=slug)
  except ObjectDoesNotExist:

    return render(request, "sad404.html")
  if mode == "open":
    scan.qr_open_time = timezone.now()
    context = {}
    if request.method == "GET":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(slug, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()
        scan.save()
        return render(request, "qrview.html", context)
  elif mode == "scan":
    scan.qr_scan_time = timezone.now()
    scan.save()
    return render(request, "info_view.html", {"scan":"success"})
  
  scan.save()

"""

@csrf_exempt
def private_restroom_form(request):
    selections = []
    buildings = Building.objects.filter(user=request.user)
    for h in buildings:
      a = Restroom.objects.filter(building=h)
      
      for object_ in a:
        selections.append([f"{object_.title}", object_.key])
    if request.method == 'GET':

        return render(request, 'restroomcreate.html', {"selections":selections})
    else:
        restroom_key = request.POST["restroom"]
        
        try:
          restroom = Restroom.objects.get(
            key=restroom_key
          )
          
          
        except:
          return render(request, 'restroomcreate.html', {'error':'이 화장실 아이디는 존재하지 않습니다.', "selections":selections})
        try:
          
          PrivateRestroom.objects.create(restroom=restroom, time_left=request.POST["time"], owner=request.user)
          
        except:
          return render(request, 'restroomcreate.html', {'error':'설문지를 다시 확인해주세요.', "selections":selections})
        return redirect("restroom_sign_in_view")

@csrf_exempt
def private_restroom_form_manage(request, key):
    selections = []
    
    rest = Restroom.objects.get(key=key)
    selections.append([rest.title,key])
    restroom = Restroom.objects.get(
        key=key
    )
    p_restroom = PrivateRestroom.objects.get(
      owner=request.user,
      restroom=restroom
    )
    
    if request.method == 'GET':

        return render(request, 'restroommanage.html', {'restroom':key, "name":p_restroom.restroom.title, "loc":p_restroom.restroom.location_information, "time":p_restroom.time_left, "selections":selections})
    else:
        print(request.POST)
        restroom_key = key
        try:
          restroom = Restroom.objects.get(
            key=restroom_key
          )
          
        except:
          return render(request, 'restroommanage.html', {'error':'이 화장실 아이디는 존재하지 않습니다.', "selections":selections})
        try:
          
          p_restroom.restroom, p_restroom.time_left = restroom,  request.POST["time"]

          p_restroom.save()
        except:
          return render(request, 'restroommanage.html', {'error':'설문지를 다시 확인해주세요.', "selections":selections})
        return render(request, 'restroommanage.html', {'restroom':key, "time":p_restroom.time_left, "selections":selections})

def viewer_home(request):
  splash_text = ["오늘 날씨가 좋은가요?", "안전과 위생, 어떤것이 더 중요할까요? 답은: 둘다!", "개발자님이 똑똑해요 ㅋㅋㅋ", "안심과 안전, 차이점은?", "좋은 하루!", "오호 확률이 낮은 문구가 나왔네요!"]
  return render(request, "home.html", {"splash":random.choice(splash_text)})


def qrgen(request, code):
    context = {}
    if request.method == "GET":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(code, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()

    return render(request, "qrview.html", context=context)

@csrf_exempt
def review(request, code):
  
  context = {}
  
  try:
    restroom = Restroom.objects.get(
      key=code
    )
  except:
    context["response"] = "실패."
    return render(request, "user_response.html", context=context)
  
  if request.method == 'GET':
    return render(request, "review.html", context=context)    
  else:

    context["response"] = "소중한 의견 감사합니다!"
    rating = request.POST["rate"]
    review = request.POST["review"]
    review = Review.objects.create(score=rating, text=review)
    restroom.reviews.add(review)
    return render(request, "user_response.html", context=context)


        