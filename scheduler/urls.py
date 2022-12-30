from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views


urlpatterns = [
    path('', views.indexView, name="index_view"),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='redirect'),
    path('createclass', views.StudentClassCreateView.as_view(), name='create_student_class'),
    path('listclasses/', views.StudentClassListView.as_view(), name = 'list_student_classes'),
    path('joinclass/', views.joinclassView, name = 'join_student_classes'),
    path('listclasses/removeclass/<int:pk>/', views.remove_class, name = 'delete_student_class'),
    path('joinclass/allclasses', views.JoinClassListView.as_view(), name= 'all_classes'),
    path('todo/', views.todoAppView, name='todo'),
    path('addTodoItem/', views.addTodoView),
    path('deleteTodoItem/<int:i>/', views.deleteTodoView),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<int:event_id>/', views.event, name='event_edit'),
    path('class/<int:pk>/', views.ClassView.as_view(), name="class_detail"),
    path('j_class/<int:pk>/', views.JoinClassView.as_view(), name="join_class_detail"),
    path('j_class/', views.ClassSearch, name="class_search"),
    path('j_class/search/<str:instructor>', views.JoinClassFilterView.as_view(), name="filtered_classes"),
    path('j_class/<int:pk>/addjoin/', views.add_join_class, name="add_join"),
    path('class/<int:pk>/addnote/', views.AddNote, name = 'class_add_note'),
    path('class/<int:pk>/deletenote/<int:id>', views.DeleteNote, name = 'class_delete_note'),
    path('rooms', views.all_rooms, name="all_rooms"),
    url(r'token$', views.token, name="token"),
    url(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)