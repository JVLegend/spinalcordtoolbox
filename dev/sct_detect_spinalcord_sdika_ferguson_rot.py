import os
import time
import pickle

####################################################################################################################
#   User Case

path_ferguson_work = '/home/neuropoly/code/spine-ms-tmi/'
path_config = path_ferguson_work + 'ferguson_config.pkl'
with open(path_config) as outfile:    
	config = pickle.load(outfile)
	outfile.close()
contrast = config['contrast']
nb_image_train = config['nb_image_train']
rot_bool = config['rot']
valid_subj = config['valid_subj']
path_ferguson_input_img = path_ferguson_work + 'input_img/' + contrast + '/'
path_ferguson_train = path_ferguson_work + contrast + '_'+ str(nb_image_train) + '/'
if config['svm_hog_alone']:
	cmd_line_test = './spine_detect -ctype=maxslice -lambda=1 '
else:
	cmd_line_test = './spine_detect -ctype=dpdt -lambda=1 '

if rot_bool:
	cmd_line_train = './spine_train_svm -hogsg -incr=20 --addRot='
	rot2test = ['0:360:0', '6:60:60', '12:60:60', '36:360:60', '72:360:60']

	path_sub_train = path_ferguson_train

	txt_name = [f for f in os.listdir(path_sub_train) if f.endswith('.txt') and not '_ctr' in f]
	for zz,tt in enumerate(txt_name):
		path_txt = path_sub_train + tt
		path_txt_ctr = path_sub_train + tt.split('.')[0] + '_ctr.txt'

		for rot in rot2test:
			path_ferguson_res_img = path_ferguson_work + 'output_img_' + contrast + '_'+ '_'.join(rot.split(':')) + '/'
			
			if not os.path.exists(path_ferguson_res_img):
				os.makedirs(path_ferguson_res_img)

			os.system(cmd_line_train + rot + ' ' + tt.split('.')[0] + ' ' + path_txt + ' ' + path_txt_ctr + ' --list True')
			os.system('mv ' + tt.split('.')[0] + '.yml ' + path_sub_train + tt.split('.')[0] + '.yml')

			id_train_subj = [line.rstrip('\n').split('/')[-1] for line in open(path_txt)]

			path_res_cur = path_ferguson_res_img +tt.split('.')[0]+ '/'

			if not os.path.exists(path_res_cur):
				os.makedirs(path_res_cur)

			for ss_test in valid_subj:
				if not ss_test in id_train_subj:
					os.system(cmd_line_test + path_sub_train + tt.split('.')[0] + ' ' + path_ferguson_input_img + ss_test + ' ' + path_res_cur + ss_test)
					if os.path.isfile(path_res_cur + ss_test + '_ctr.txt'):
						os.remove(path_res_cur + ss_test + '_ctr.txt')
					if os.path.isfile(path_res_cur + ss_test + '_svm.hdr'):
						os.remove(path_res_cur + ss_test + '_svm.hdr')
					if os.path.isfile(path_res_cur + ss_test + '_svm.img'):
						os.remove(path_res_cur + ss_test + '_svm.img')
			if os.path.isfile(path_sub_train + tt.split('.')[0] + '.yml'):
				os.remove(path_sub_train + tt.split('.')[0] + '.yml')