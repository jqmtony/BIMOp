from django.db import models

from portal.models import *

class BIMComponent(models.Model):
	project = models.ForeignKey(Project, null = True, on_delete=models.CASCADE);
	guid = models.CharField(max_length=200)
	name = models.CharField(max_length=200, null = True)
	connectedFrom = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank = True)
	content = models.CharField(max_length=200, null=True) # Such as water, air, steam

	def __str__(self):
		return str(self.project) + '_' + self.name;

class Sensor(models.Model):
	measuredTarget = models.ForeignKey(BIMComponent, on_delete=models.CASCADE);
	sensorType = models.CharField(max_length=200, null = True) # Such as temperature, massFlowRate
	unit = models.CharField(max_length=200, null = True) # Such as C, F, m3/s
	isDataFromBAS = models.BooleanField(); # True if the data is obtained from BAS, False is data is derived by BIM components physical relationships
	basAddress = models.CharField(max_length=200, null = True, blank = True) # This field should be filled if isDataFromBAS is True
	derivedSensor = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank = True) # This field should be filled if isDataFromBAS is False

	def __str__(self):
		return str(self.measuredTarget) + '_' + self.sensorType + '_' + 'sensor';

class SensorDataHist(models.Model):
	recordedTime = models.DateTimeField();
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE);
	value = models.CharField(max_length=200, null = True);
	isGood = models.BooleanField();
	isBadNotes = models.CharField(max_length=200, null = True, blank = True);

	def __str__(self):
		return str(self.sensor) + '_' + 'SensorDataHist' + '_' + str(self.recordedTime);

