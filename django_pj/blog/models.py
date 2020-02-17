from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Sample_info(models.Model):
	class Meta:
		db_table = 'sample_info'
	id = models.AutoField(primary_key=True)

	cultivar			= models.CharField(max_length=200 ,blank=True)
	stage				= models.CharField(max_length=200 ,blank=True)
	repeat				= models.CharField(max_length=200 ,blank=True)

class Tpm_list(models.Model):
	class Meta:
		db_table = 'tpm_list'
	id = models.AutoField(primary_key=True)

	Entrez_Gene_ID		= models.CharField(max_length=200 ,blank=True)
	Tpm					= models.CharField(max_length=200 ,blank=True)

class trans_sample(models.Model):
	class Meta:
		db_table = 'trans_sample'
	id = models.AutoField(primary_key=True)

	SampleNo		= models.CharField(max_length=200 ,blank=True)
	ResourceName	= models.CharField(max_length=200 ,blank=True)

class Entrez_Gene_ID(models.Model):
	class Meta:
		db_table = 'Entrez_Gene_ID'
	id = models.AutoField(primary_key=True)

	Entrez_Gene_ID	= models.CharField(max_length=200 ,blank=True)


class annot_table(models.Model):
	class Meta:
		db_table = 'annot_table'
	id = models.AutoField(primary_key=True)

	GeneID			= models.CharField(max_length=200 ,blank=True)
	Locus			= models.CharField(max_length=200 ,blank=True)
	Proteinproduct	= models.CharField(max_length=200 ,blank=True)
	Length			= models.CharField(max_length=200 ,blank=True)
	Proteinname		= models.CharField(max_length=200 ,blank=True)

