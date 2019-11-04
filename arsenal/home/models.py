from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

class knowledge_base(models.Model):
	kb_category = (('tr','Trainings'),('rp','Research Portals'))
	category = models.CharField(max_length=2, choices=kb_category) 
	title = models.CharField(max_length=20,unique=True)
	link = models.CharField(max_length=200,unique=True)
	hits = models.IntegerField(default=0,editable=False)
	
	def __str__(self):
		return self.title

class knowledge_base_admin(admin.ModelAdmin):
	list_display=('title','category','link','hits')


class user_extension(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE) #if user deleted in User(django table) delete the user in this
	description = models.CharField(max_length=25, blank=True)
	extension = models.CharField(max_length=20,unique=True,blank=True, null=True)
	mobile = models.CharField(max_length=10,blank=True,unique=True,null=True,validators=[RegexValidator(r'\d{10}')])
	
	schoice=((1,'Frist Shift'),(2,'Second Shift'))
	shift = models.IntegerField(choices=schoice, null=True, blank=True)
	
	suchoice=(('a','A'),('b','B'))
	subshift = models.CharField(max_length=1, choices=suchoice, blank=True)
	
	def __str__(self):
		return str(self.user)

class user_extension_admin(admin.ModelAdmin):
	list_display=('user','description','mobile','extension','shift','subshift')



class repository(models.Model):
	rep_category=(('cucm','CUCM'),('trace','Traces'),('software','Softwares'),('integrations','Integrations'),('daytoday','D2D'),('collaboration','Collaboration/Apps'))
	category = models.CharField(max_length=15,choices=rep_category)
	name = models.CharField(max_length=20, unique=True)
	link = models.CharField(max_length=500, unique=True)
	hits = models.IntegerField(default=0, editable=False)
	
	def __str__(self):
		return str(self.name)


class repository_admin(admin.ModelAdmin):
	list_display=('name','category','link')



class trendingidea(models.Model):
	iname = models.CharField(unique=True, max_length=15)
	idea = models.TextField(unique=True)
	submittedon = models.DateField(auto_now=True)
	support = models.ManyToManyField(User)
	hits = models.PositiveSmallIntegerField(default=1,editable=False)
	readbyadmin = models.BooleanField(default=0)
	feasibilitycheck = models.NullBooleanField(null=True)
	submittedby = models.ForeignKey(User,related_name="submitted_by")
	assignedto = models.ForeignKey(User, blank=True, null=True, related_name="assignedto")

	def __str__(self):
		return str(self.iname)

class trendingidea_admin(admin.ModelAdmin):
	list_display = ('submittedby','iname','idea','submittedon','readbyadmin','feasibilitycheck','hits')



class inventory(models.Model):
	inven_category=(('cucm','CUCM'),('router','Router'),('ipphone','IPPhone'),('kem','Expansion Module'),('esxi','ESXi'),('cimc','CIMC'))	
	identifier=models.CharField(primary_key=True,max_length=15)
	category=models.CharField(max_length=7,choices=inven_category)

	model_category=(('3951','3951'),('3905','3905'),('6901','6901'),('6921','6921'),('6941','6941'),('6945','6945'),('6961','6961'),('7821','7821'),('7841','7841'),('7861','7861'),('7811','7811'),('7832','7832'),('7925','7925'),('7931','7931'),('7940','7940'),('7942','7942'),('7945','7945'),('7960','7960'),('7962','7962'),('7965','7965'),('7970','7970'),('7975','7975'),('7916','7916'),('7961','7961'),('7912','7912'),('8865','8865'),('8861','8861'),('8800','8800'),('8811','8811'),('8821','8821'),('8821EX','8821EX'),('8831','8831'),('8832','8832'),('8841','8841'),('8845','8845'),('8851','8851'),('8941','8941'),('8945','8945'),('8961','8961'),('9951','9951'),('9971','9971'),('DX650','DX650'),('ATA187','ATA187'),('ATA190','ATA190'),('ATA191','ATA191'),('ATA192','ATA192'),('8.X','8.X'),('9.X','9.X'),('10.X','10.X'),('11.X','11.X'),('12.X','12.X'),('4.0','4.0'),('5.0','5.0'),('5.5','5.5'),('6.0','6.0'),('6.5','6.5'))

	modelorversion=models.CharField(choices=model_category,max_length=7)
	checkedoutdate=models.DateTimeField(auto_now=True)
	checkedoutby=models.ManyToManyField(User,null=True, blank=True)
	comment=models.CharField(max_length=50,blank=True,null=True)
	team_category=(('indcucm','IND-CUCM'),('indcuc','IND-CUC'),('indms','IND-MS'),('indipcc','IND-IPCC'),('indev','IND-EV'))
	team=models.CharField(max_length=7,default='indcucm',blank=True,choices=team_category)	

	def __str__(self):
		return str(self.category)+': '+str(self.identifier)

	
class inventory_admin(admin.ModelAdmin):
	list_display=('team','category','modelorversion','identifier','checkedoutdate','comment')
	
