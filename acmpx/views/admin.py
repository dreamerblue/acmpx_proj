from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..forms import AdminLoginForm, TrainingForm, AdminUploadCertificateForm
from ..models import Training, Certificate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import time
import random
import string
import os
from ..modules.XlHandler import XlHandler
from ..modules.CertificateHandler import CertificateHandler


# 后台
@login_required(login_url=settings.ADMIN_LOGIN_URL)
def admin_index(request):
	return render(request, 'acmpx/admin/index.html', {
		'training_count': Training.objects.count(),
		'certificate_count': Certificate.objects.count(),
		'participant_count': Certificate.objects.all().aggregate(Count('student_no', distinct=True))['student_no__count'],
	})


# 后台登录
def admin_login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('acmpx:admin_index'))
	error = None
	if request.method == 'POST':
		form = AdminLoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None and user.is_active:
				login(request, user)
				if request.POST['next']:
					return HttpResponseRedirect(request.POST['next'])
				else:
					return HttpResponseRedirect(reverse('acmpx:admin_index'))
			else:
				error = '用户名或密码错误'
		else:
			error = '请填写用户名和密码'
	else:
		form = AdminLoginForm()
	return render(request, 'acmpx/admin/login.html', {'form': form, 'error': error})


# 后台登出
def admin_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('acmpx:admin_login'))


# 后台-权限拒绝
@login_required(login_url=settings.ADMIN_LOGIN_URL)
def admin_permission_denied(request):
	return render(request, 'acmpx/admin/permission_denied.html')


# 后台-培训管理
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@permission_required(
	perm=['acmpx.add_training', 'acmpx.change_training', 'acmpx.delete_training'],
	login_url=settings.ADMIN_PERMISSION_DENIED_URL,
)
def admin_training_list(request):
	training_list = Training.objects.all().order_by('id').reverse()
	paginator = Paginator(training_list, 20)
	page = request.GET.get('page')
	try:
		trainings = paginator.page(page)
	except PageNotAnInteger:
		trainings = paginator.page(1)
	except EmptyPage:
		trainings = paginator.page(paginator.num_pages)
	return render(request, 'acmpx/admin/training_list.html', {'item': 'admin_training', 'training_list': trainings})


# 后台-添加培训
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@permission_required(
	perm=['acmpx.add_training'],
	login_url=settings.ADMIN_PERMISSION_DENIED_URL,
)
def admin_training_add(request):
	training_form = TrainingForm()
	errors = list()
	if request.method == 'POST':
		training_form = TrainingForm(request.POST)
		if training_form.is_valid():
			if training_form.cleaned_data['started_at'] > training_form.cleaned_data['ended_at']:
				errors.append('培训开始日期不能晚于培训结束日期')
			else:
				new_training = training_form.save()
				make_training_dir(new_training.id)
				messages.success(request, '添加成功')
				return HttpResponseRedirect(reverse('acmpx:admin_training_list'))
		else:
			for field in training_form:
				for error in field.errors:
					errors.append('{}: {}'.format(field.label, error))
	return render(request, 'acmpx/admin/training_add.html', {
		'item': 'admin_training',
		'form': training_form,
		'errors': errors,
	})


# 后台-添加培训 -> 创建培训相关资源目录
def make_training_dir(training_id):
	training_base_path = settings.MEDIA_ROOT + 'training/' + str(training_id) + '/'
	if not os.path.exists(training_base_path):
		os.makedirs(training_base_path)
	CertificateHandler(training_id).create_certificate_directory()


# 后台-编辑培训
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@permission_required(
	perm=['acmpx.change_training', 'acmpx.delete_training'],
	login_url=settings.ADMIN_PERMISSION_DENIED_URL,
)
def admin_training_edit(request, training_id):
	training = get_object_or_404(Training, pk=training_id)
	training_form = TrainingForm()
	errors = list()
	if request.method == 'GET':
		training_form = TrainingForm(instance=training)
	if request.method == 'POST':
		training_form = TrainingForm(request.POST, instance=training)
		if training_form.is_valid():
			if training_form.cleaned_data['started_at'] > training_form.cleaned_data['ended_at']:
				errors.append('培训开始日期不能晚于培训结束日期')
			else:
				training_form.save()
				messages.success(request, '保存成功 <a href="%s" class="alert-link text-left-gap">点此返回</a>' % reverse(
					'acmpx:admin_training_list'))
				return HttpResponseRedirect(reverse('acmpx:admin_training_edit', args=(training.id,)))
		else:
			for field in training_form:
				for error in field.errors:
					errors.append(field.label + '：' + error)
	return render(request, 'acmpx/admin/training_edit.html', {
		'item': 'admin_training',
		'form': training_form,
		'errors': errors,
		'training_id': training.id,
	})


# 后台-证书管理
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@permission_required(
	perm=['acmpx.add_certificate', 'acmpx.change_certificate', 'acmpx.delete_certificate'],
	login_url=settings.ADMIN_PERMISSION_DENIED_URL,
)
def admin_certificate_list(request, training_id):
	training = get_object_or_404(Training, pk=training_id)
	certificates_list = training.certificate_set.order_by('idx')
	paginator = Paginator(certificates_list, 20)
	page = request.GET.get('page')
	try:
		certificates = paginator.page(page)
	except PageNotAnInteger:
		certificates = paginator.page(1)
	except EmptyPage:
		certificates = paginator.page(paginator.num_pages)
	return render(request, 'acmpx/admin/certificate_list.html', {
		'item': 'admin_training',
		'certificate_list': certificates,
		'training': training,
	})


# 后台-上传证书数据
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@permission_required(
	perm=['acmpx.change_training', 'acmpx.add_certificate', 'acmpx.change_certificate', 'acmpx.delete_certificate'],
	login_url=settings.ADMIN_PERMISSION_DENIED_URL,
)
def admin_training_upload_certificate(request, training_id):
	training = get_object_or_404(Training, pk=training_id)
	if request.method == 'POST':
		form = AdminUploadCertificateForm(request.POST, request.FILES)
		if form.is_valid():
			certificate_data_list = handle_uploaded_certificate(request.FILES['file'])
			if certificate_data_list.has_error:
				messages.error(request, '解析文件时出现严重错误，请检查文件并重新上传')
			else:
				# 上传的表格文件有效，先删除此培训下的所有证书数据，再重新插入数据
				training.certificate_set.all().delete()
				certificate_no_prefix = training.ended_at.strftime('%Y%m%d') + '%04d' % training.id
				for certificate_data in certificate_data_list.info_list:
					Certificate(
						id=certificate_no_prefix + '%04d' % certificate_data.idx,
						student_no=certificate_data.student_no,
						student_class=certificate_data.student_class,
						student_name=certificate_data.student_name,
						score=certificate_data.score,
						rank=certificate_data.rank,
						idx=certificate_data.idx,
						training_id=training.id,
					).save()
				# 更新参与人数
				training.number_of_participants = certificate_data_list.num
				training.save()
				# 删除证书资源文件夹并重建
				CertificateHandler(training.id).delete_all_certificates()
				messages.success(request, '成功导入了 {} 条数据'.format(certificate_data_list.num))
				return HttpResponseRedirect(reverse('acmpx:admin_certificate_list', args=(training.id,)))
		else:
			messages.error(request, '请上传有效的文件')
		return HttpResponseRedirect(reverse('acmpx:admin_training_upload_certificate', args=(training.id,)))
	else:
		form = AdminUploadCertificateForm()
	return render(request, 'acmpx/admin/upload_certificate.html', {'form': form, 'training': training})


# 生成随机字符串
def random_time_based_str():
	return (str(time.time()) + ''.join(random.sample(string.ascii_letters + string.digits, 16))).replace('.', '')


# 后台-上传证书数据 -> 处理上传文件并返回处理好的信息列表
def handle_uploaded_certificate(f):
	random_file_name = random_time_based_str()
	upload_path = settings.MEDIA_ROOT + settings.UPLOAD_TMP_PATH
	if not os.path.exists(upload_path):
		os.makedirs(upload_path)
	file_path = upload_path + random_file_name
	with open(file_path, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	xl = XlHandler(file_path)
	xl.handle_data()
	os.remove(file_path)
	return xl


# 后台-下载全部证书
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@permission_required(
	perm=['acmpx.add_certificate', 'acmpx.change_certificate', 'acmpx.delete_certificate'],
	login_url=settings.ADMIN_PERMISSION_DENIED_URL,
)
def admin_training_download_certificate_set(request, training_id):
	training = get_object_or_404(Training, pk=training_id)
	# 懒加载，第一次访问时生成证书
	certificate_handler = CertificateHandler(training_id)
	url_list = [settings.BASE_URL + reverse('acmpx:training_certificate_render_all', args=(training.id,))]
	certificate_handler.load_certificate(url_list)
	return HttpResponseRedirect(certificate_handler.get_certificate_url())


# 后台-清除证书缓存
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@permission_required(
	perm=['acmpx.add_certificate', 'acmpx.change_certificate', 'acmpx.delete_certificate'],
	login_url=settings.ADMIN_PERMISSION_DENIED_URL,
)
def admin_training_clear_certificate_cache(request, training_id):
	training = get_object_or_404(Training, pk=training_id)
	CertificateHandler(training_id).delete_all_certificates()
	messages.success(request, '清除证书缓存成功')
	return HttpResponseRedirect(reverse('acmpx:admin_certificate_list', args=(training.id,)))
