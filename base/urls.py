from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('medicines', MedicineList.as_view(), name='medicines'),
    path('add-medicine/', MedicineCreate.as_view(), name='medicines-add'),
    path('edit-medicine/<int:pk>/', MedicineEdit.as_view(), name='medicines-edit'),
    path('delete-medicine/<int:pk>/', MedicineDelete.as_view(), name='medicines-delete'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('medicine/<int:pk>/', MedicineDetail.as_view(), name='medicine'),
    path('medicinesDatabases', MedicineDatabaseList.as_view(), name='medicinesDatabase'),
    path('medicineDatabases/<int:pk>/', MedicineDatabaseDetail.as_view(), name='medicineDatabase'),

]
