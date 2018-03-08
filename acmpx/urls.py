from django.urls import path
from .views import home, admin

app_name = 'acmpx'
urlpatterns = [
	path('', home.index, name='index'),
	path('certificate/', home.certificate_inquiry, name='certificate_inquiry'),
	path('certificate/<int:certificate_id>/render/', home.certificate_render, name='certificate_render'),
	path('training/<int:training_id>/certificate/render_all/', home.training_certificate_render_all,
		 name='training_certificate_render_all'),
	path('certificate/<int:certificate_id>/show/', home.certificate_show, name='certificate_show'),

	path('admin/', admin.admin_index, name='admin_index'),
	path('admin/login/', admin.admin_login, name='admin_login'),
	path('admin/logout/', admin.admin_logout, name='admin_logout'),
	path('admin/permission_denied/', admin.admin_permission_denied, name='admin_permission_denied'),
	path('admin/training/', admin.admin_training_list, name='admin_training_list'),
	path('admin/training/add/', admin.admin_training_add, name='admin_training_add'),
	path('admin/training/<int:training_id>/edit/', admin.admin_training_edit, name='admin_training_edit'),
	path('admin/training/<int:training_id>/certificate/', admin.admin_certificate_list, name='admin_certificate_list'),
	path('admin/training/<int:training_id>/upload/certificate/', admin.admin_training_upload_certificate,
		 name='admin_training_upload_certificate'),
	path('admin/training/<int:training_id>/download_certificate_set/', admin.admin_training_download_certificate_set,
		 name='admin_training_download_certificate_set'),
	path('admin/training/<int:training_id>/clear_certificate_cache/', admin.admin_training_clear_certificate_cache,
		 name='admin_training_clear_certificate_cache'),
]
