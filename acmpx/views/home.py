from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..forms import SearchCertificateForm
from ..models import Training, Certificate
from django.conf import settings
from ..modules.CertificateHandler import CertificateHandler


# 首页
def index(request):
	return render(request, 'acmpx/index.html')


# 证书查询
def certificate_inquiry(request):
	form = SearchCertificateForm(request.GET)
	certificate_set = None
	if form.is_valid() and form.cleaned_data['query'] != '':
		if form.cleaned_data['type'] == 'student_no':
			certificate_set = Certificate.objects.all().filter(student_no=form.cleaned_data['query'])
		if form.cleaned_data['type'] == 'certificate_no':
			certificate_set = Certificate.objects.all().filter(pk=form.cleaned_data['query'])
	return render(request, 'acmpx/certificate_inquiry.html', {
		'item': 'certificate_inquiry', 'form': form, 'certificate_set': certificate_set
	})


# 证书渲染
def certificate_render(request, certificate_id):
	certificate = get_object_or_404(Certificate, pk=certificate_id)
	return render(request, 'acmpx/certificate_render_a4.html',
				  {'certificate': certificate, 'base_url': settings.BASE_URL})


# 全部证书渲染
def training_certificate_render_all(request, training_id):
	training = get_object_or_404(Training, pk=training_id)
	return render(request, 'acmpx/certificate_render_all_a4.html',
				  {'training': training, 'base_url': settings.BASE_URL})


# 证书查看
def certificate_show(request, certificate_id):
	certificate = get_object_or_404(Certificate, pk=certificate_id)
	# 懒加载，第一次访问时生成证书
	certificate_handler = CertificateHandler(certificate.training_id, certificate_id)
	url_list = [settings.BASE_URL + reverse('acmpx:certificate_render', args=(certificate.id,))]
	certificate_handler.load_certificate(url_list)
	return HttpResponseRedirect(certificate_handler.get_certificate_url())
