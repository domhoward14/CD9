from CD9.views import *
from CD9.models import *
#for text in Texts.objects.all():
#	print text.emo_score
data_set = App_list.objects.all()
dict = {'data_set':data_set} 
dict["data_type"] = 1 
fetchAndProcess(dict)
for app in App_list.objects.all():
	print app.description
