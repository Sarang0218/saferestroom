from .models import RestroomVisitData, Restroom, PrivateRestroom, Building
from django.forms import ModelForm

class RestroomVisitDataForm(ModelForm):
  def __init__(self,user,*args,**kwargs):
        super (RestroomVisitDataForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['p_restroom'].queryset = PrivateRestroom.objects.none()
        buildings = Building.objects.filter(user=user)
        for building in buildings:
          restrooms = Restroom.objects.filter(building=building)
          for restroom in restrooms:
              self.fields['p_restroom'].queryset = self.fields['p_restroom'].queryset | PrivateRestroom.objects.filter(restroom=restroom, owner=user)
            
        
      
        


 
  class Meta:
    model = RestroomVisitData
    fields = ['telephone', 'gender', 'p_restroom']
    labels = {
        "telephone": "핸드폰 번호",
        "gender" : "성",
        "p_restroom":"화장실"
    }


