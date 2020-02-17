from django.shortcuts import render
from .models import Sample_info, Tpm_list, trans_sample, Entrez_Gene_ID, annot_table
from django import forms
import pandas as pd
import numpy as np
from operator import itemgetter, attrgetter

# Create your views here.


def post_list(request):
	label_list = ['KLS 116-1','Sochung2','Kangwon sujib2-33','Kyoungbuk Kyoungsan-1997-54','Ilpumgeomjeong','IT112859','Geomeunbak','Dongsan133','KLS88066','KAS590-6','KAS210-22',
			 					'PI 227159','YB316-3','IT177388','KLS123-1','Heugcheong','PI 96983','SLSB397-1','PI 399122','Chungja','Cheongja3','SS0404-T5-76','KAS660-21','KAS505-1',
			 					'IT178024','IT104334','YN154','KAS660-12','Pureun','Milyang12','Williams 82K','Daepung','Taekwang','Heuin','Hwangkeum','Wooram','Yonpoong','Haman','Saedanbaek ',
			 					'L62-667','Daeyang','PI 88820','Pungwon','Somyung','Bangsa','Danbaek','Shinhwa','KLS86083','PI 60269-2','PI 84644']

	genename = Entrez_Gene_ID.objects.all()


# tissue select -> push cultivar_list


	ix_10 = []

	stage_10 = '10'
	stage_selected 	= Sample_info.objects.filter(stage=stage_10)
	sample_list = trans_sample.objects.all()
	trans_dic = {}
	for x in sample_list:
		trans_dic[x.SampleNo] = x.ResourceName
	cultivar_list		= [trans_dic[x.cultivar] for x in stage_selected]

	ix_10					+= [int(x.id) for x in stage_selected]

	ix_30 = []

	stage_30 			= '30'
	stage_selected 		= Sample_info.objects.filter(stage=stage_30)
	sample_list 		= trans_sample.objects.all()
	trans_dic 			= {}
	for x in sample_list:
		trans_dic[x.SampleNo] 	= x.ResourceName
	cultivar_list				= [trans_dic[x.cultivar] for x in stage_selected]



	ix_30						+= [int(x.id) for x in stage_selected]


	ix_cultivar 	= []
	cultivar_all 	= Sample_info.objects.all()
	stage_list 		= [str(x.stage) for x in cultivar_all]
	ix_cultivar		+= [int(x.id) for x in cultivar_all]






# gene select -> push tpm_output
	query 				= request.GET.get("gene")

	if str(query)		== 'None':
		query 			= '100808170'




	annot = annot_table.objects.all()
	post_data = annot_table.objects.filter(GeneID=query)




	tpm_values, tpm_set, tpm_set_fix, data, data_sort = [], [], [], [], []

	gene_selected 		= Tpm_list.objects.filter(Entrez_Gene_ID=query)
	tpm_values 			+= [x.Tpm for x in gene_selected]


	tpm_set	 			+= [np.array(x.split(','))[ix_10] for x in tpm_values]
	tpm_set_fix			+= [list(map(float,x.tolist())) for x in tpm_set]
	tpm_output			=  sum(tpm_set_fix,[])

			
# csv file 
	data				+= [[x,y] for x, y in zip(tpm_output, cultivar_list)]
	for x in label_list:
		for y in data:
			if y[1] == x:
				data_sort.append(y)
	DB_output			= [(np.array(data_sort))]
	csv_file_10			= '/static/output_10.csv'	
	np.savetxt('./blog/static/output_10.csv', np.column_stack((DB_output)), delimiter = ',', fmt = '%s', header = 'tpm,cultivar',comments="")

	tpm_set, tpm_set_fix, data, data_sort = [], [], [], []

	tpm_set				+= [np.array(x.split(','))[ix_30] for x in tpm_values]
	tpm_set_fix			+= [list(map(float,x.tolist())) for x in tpm_set]
	tpm_output			=  sum(tpm_set_fix,[])
			
# csv file 
	data				+= [[x,y] for x, y in zip(tpm_output, cultivar_list)]
	for x in label_list:
		for y in data:
			if y[1] == x:
				data_sort.append(y)
	DB_output			= [(np.array(data_sort))]
	csv_file_30			= '/static/output_30.csv'	
	np.savetxt('./blog/static/output_30.csv', np.column_stack((DB_output)), delimiter = ',', fmt = '%s', header = 'tpm,cultivar',comments="")

	tpm_values, tpm_set, tpm_set_fix, data = [], [], [], []

	gene_selected 		= Tpm_list.objects.filter(Entrez_Gene_ID=query)
	tpm_values 			+= [x.Tpm for x in gene_selected]


	tpm_set	 			+= [np.array(x.split(','))[ix_cultivar] for x in tpm_values]
	tpm_set_fix			+= [list(map(float,x.tolist())) for x in tpm_set]
	tpm_output			=  sum(tpm_set_fix,[])

			
# csv file 
	
	data				+= [[x,y] for x, y in zip(tpm_output, stage_list)]
	DB_output			= [(np.array(data))]
	csv_file_stage		= '/static/output_stage.csv'	
	np.savetxt('./blog/static/output_stage.csv', np.column_stack((DB_output)), delimiter = ',', fmt = '%s', header = 'tpm,stage',comments="")

	


	return_source 		= {'csv_file_10':csv_file_10, 'query':query, 'csv_file_30':csv_file_30, 'csv_file_stage':csv_file_stage, 'genename':genename, 'post_data':post_data}

	return render(request, 'blog/post_list.html', return_source)