from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views as auth_view
from .forms import LogInForm,MyPasswordChangeForm,MySetPassword



urlpatterns = [

    path('',ProductView.as_view(),name='home'),
    # path('product-detail/', product_detail, name='product-detail'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(),name='product-detail'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/',show_cart,name='showcart'),
    path('pluscart/',plus_cart,),
    path('minuscart/',minus_cart),
    path('removecart/',remove_cart),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', address, name='address'),
    path('editadd/<int:id>',update_adress,name='update-add'),
    path('deleteadd/<int:id>',delete_adress,name='delete-add'),
    path('orders/', orders, name='orders'),
    path('laptop/',laptop_all,name='laptop'),
    path('laptop/<slug:data>',laptop_all,name='laptopdata'),
    path('topwear/',topwear_view,name='topwear'),
    path('bottomwear/',bottomwear_view,name='bottomwear'),
    path('mobile/',mobile,name='mobile'),
    path('mobile/<slug:data>', mobile, name='mobiledata'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LogInForm), name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPassword),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/', Registration.as_view(), name='customerregistration'),
    path('checkout/', checkout, name='checkout'),
    path('paymentdone/',payment_done, name='paymentdone'),

    path('addproducts/',add_products,name='add-products'),
    path('viewproducts/',view_product,name='view-products'),
    path('updateproducts/<int:id>',update_products,name='update-products'),
    path('deleteproducts/<int:id>',delete_products,name='delete-products'),

    path('users/',user_data,name='users'),
    path('addusers/',add_users,name='add-users'),
    path('updateusers/<int:id>',update_user,name='update-user'),
    path('deleteuser/<int:id>',delete_user,name='delete-user'),

    path('carts-data/',cart_data,name='carts-data'),

    path('orders-data/',orders_data,name='orders-data'),
    path('update-orders/<int:id>',update_orders,name='update-orders'),
    path('delete-orders/<int:id>',delete_orders,name='delete-orders')
   
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   # for display image in web page 
