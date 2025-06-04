from django.urls import path
from .views import   add_announcement, add_meeting, add_or_update_practice_session, add_transaction, create_intern_from_application, delete_announcement, delete_meeting, delete_practice_session , delete_transaction, download_document, edit_meeting, edit_transaction, get_ai_data, get_application_data, get_details, interns_performance, manage_shedule, search_candidates, send_mail,download_csv, helper, login_view, logout_view, search_applications, send_notification, send_offer_letter, single, sorted_applications, transaction_list, update_performance, update_single_performance, upload_excel,home, upload_performance,user_list, user_performance_list
# from .views import update_timestamp

urlpatterns = [
    path('', home, name='home'),

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),


    path('upload/', upload_excel, name='upload_excel'),
    path('search/', search_applications, name='search_applications'),
    path("sorted-applications/", sorted_applications, name="sorted_applications"),

    
    path('performance/', user_performance_list, name='user_performance'),
    path('get-application-data/', get_application_data, name='get_application_data'),
    path('update-performance/<int:user_id>/', update_performance, name='update_performance'),
    path("update-single-performance/", update_single_performance, name="update_single_performance"),

    # path('filter-performance/', filter_performance, name='filter_performance'),
    path('user-list/', user_list, name='user_list'),
    path('get-details/<int:user_id>/', get_details, name='get_details'),

    path("download-csv/", download_csv, name="download_csv"),
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/add/',add_transaction, name='add_transaction'),
    path('transactions/edit/<uuid:transaction_id>/',edit_transaction, name='edit_transaction'),
    path('transactions/delete/<uuid:transaction_id>/', delete_transaction, name='delete_transaction'),
    path('transactions/download/<uuid:transaction_id>/', download_document, name='download_document'),

    path('interns-performance/', interns_performance, name='interns_performance'),
    path('send-notification/', send_notification, name='send_notification'),
    path('add-meeting/', add_meeting, name='add_meeting'),
    path("add-practice-session/", add_or_update_practice_session, name="add_practice_session"),
    path("edit-practice-session/<int:session_id>/", add_or_update_practice_session, name="edit_practice_session"),
    path("add-announcement/", add_announcement, name="add_announcement"),
    path("manage-schedule/", manage_shedule, name="manage_schedule"),
    path('edit-meeting/<int:id>/', edit_meeting, name='edit_meeting'),
    path('delete-meeting/<int:id>/', delete_meeting, name='delete_meeting'),
    path('delete-announcement/<int:id>/', delete_announcement, name='delete_announcement'),
    path('delete-practice-session/<int:session_id>/', delete_practice_session, name='delete_practice_session'),



    path('create-intern/', create_intern_from_application, name='create_intern'),






    # path('update-timestamp/', update_timestamp, name='update_timestamp'),
    path("upload-performance/", upload_performance, name="upload_performance"),

    path('send-email/',send_mail,name='send-email'),
    path('single-email/',single,name='single-email'),
    path('help/',helper,name='help'),


    path("internship/", search_candidates, name="internship"),
    path("send-offer/<int:candidate_id>/", send_offer_letter, name="send_offer_letter"),
    path("get-ai-data/", get_ai_data, name="get_ai_data"),


    
]
