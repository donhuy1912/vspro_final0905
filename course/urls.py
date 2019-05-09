from django.urls import path
from . import views
from . import ajax

app_name = 'course'

urlpatterns = [
    path('mblock', views.mblock, name='mblock'),
    path('course/allcourse', views.allcourse, name='allcourse'),
    path('coursedetail/<int:id>/', views.coursedetail, name = 'coursedetail'),
    path('coursedetail/<int:id>/enroll', views.enroll, name = 'enroll'),
    path('course/<int:id>', views.coursepart, name = 'coursepart'),
    path('course/<int:id>/chapter', views.coursechapter, name = 'coursechapter'),
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>', views.courselesson, name = 'courselesson'),
    # Course activity
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/item/<int:iditem>/activity/<int:idact>', views.courseactivity, name = 'courseactivity'),
    # List course
    path('course/mycourse', views.courselist, name = 'mycourse'),
    #course created by a teacher viewed by student
    path('course/teachercourse/<str:teacheraccid>', views.teachercourse, name = 'teachercourse'),
    # teacher detail
    path('course/teacherdetail', views.teacherdetail, name= 'teacherdetail'),
    # managecourse
    path('course/managecourse',views.managecourse, name= 'managecourse'),


    # cousre overview
    path('course/courseoverview/<int:idsub>', views.courseoverview, name='courseoverview'),

    # Create, update, delete COURSE
    path('course/coursecreate', views.coursecreate, name= "coursecreate"),
    path('course/<int:idsub>/chapincourse', views.chapincourse, name= "chapincourse"),
    path('course/courseedit/<int:idsub>', views.courseedit, name= "courseedit"),

    # Create, create, delete Chapter
    path('course/<int:idsub>/chapter/create', views.chaptercreate, name="chaptercreate"),
    path('course/<int:idsub>/chapter/<int:idchap>/edit', views.chapteredit, name="chapteredit"),
    path('course/<int:idsub>/chapter/<int:idchap>', views.lessinchap, name= "lessinchap"),

    # Create, create, delete Lesson:
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/create', views.lessoncreate, name="lessoncreate"),    
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/edit', views.lessonedit, name="lessonedit"),
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/iteminles', views.iteminles, name= "iteminles"),

    # Create, create, delete Item:
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/item/create', views.itemcreate, name="itemcreate"), 
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/item/<int:iditem>/edit', views.itemedit, name="itemedit"), 
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/item/<int:iditem>/actinitem', views.actinitem, name= "actinitem"),

    # create act
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/item/<int:iditem>/activity/create', views.activitycreate, name="activitycreate"),
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/item/<int:iditem>/activity/<int:idact>/edit', views.activityedit, name="activityedit"),
    # dashboard
    path('dashboard', views.dashboard, name= 'dashboard'),
    # dashboard/course/id
    path('dashboard/course/<int:idsub>', views.dashboardcourse, name="dashboardcourse"),

	# show userforumblog của course
    path('course/<int:idsub>/userforumcourse/', views.userforumcourse, name = "userforumcourse"),
    path('course/<int:idsub>/userforumblogcourse/<int:idfor>/', views.userforumblogcourse, name = "userforumblogcourse"),
    path('course/<int:idsub>/userforumpostcourse/', views.userforumpostcourse, name = "userforumpostcourse"),

    # ajax Like
    path('ajax/ajaxunlike', ajax.ajaxUnlike, name = "ajaxUnlike"),
    path('ajax/like', ajax.ajaxLike, name = 'ajaxLike'),
    # ajax chapter
    path('ajax/chaptercontent', ajax.ajaxChapContent, name = 'chapterContent'),
    # ajax del cmt lesson
    path('ajax/lessonDelComment', ajax.ajaxDelCommentLes, name = 'lessonDelComment'),
    # ajax del cmt lesson
    path('ajax/actDelComment', ajax.ajaxDelCommentActRep, name = 'actDelComment'),
    # ajax tracking for button complete for activity
    path('ajax/trackingActivity', ajax.ajaxtrackingActivity, name = 'trackingActivity'),
    # ajax create comment actReply
    path('ajax/actCreateComment', ajax.ajaxCreateCommentActRep , name="ajaxCreateComment"),
    # ajax sort chap,les,item,act
    path('ajax/sortchap', ajax.ajaxSortChap),
    path('ajax/sortlesson', ajax.ajaxSortLes),
    path('ajax/sortitem', ajax.ajaxSortItem),
    path('ajax/sortact', ajax.ajaxSortAct),
    # ajax reload chap after sort
    path('ajax/aftersortchap', ajax.ajaxAfterSortChap),
    path('ajax/aftersortles', ajax.ajaxAfterSortLes),
    path('ajax/aftersortitem', ajax.ajaxAfterSortItem),
    path('ajax/aftersortact', ajax.ajaxAfterSortAct),
   
    # ajax check course: create, edit
    path('ajax/checktypeact', ajax.ajaxchecktypeact),
    path('ajax/checkenvir', ajax.ajaxcheckenvir),
   
   # ajax create forumreply
    path('ajax/forumshowcourse/', ajax.ajaxShowForCourse),
    # path('ajax/forumsearchcourse/', ajax.ajaxSearchForCourse),
    # path('ajax/forumreplydeletecourse/', ajax.ajaxDelCommentForCourse),
    # path('ajax/forumreplycreatecourse/', ajax.ajaxCreateCommentForCourse),
    path('ajax/forumreplyshowcourse/', ajax.ajaxShowCommentForCourse),
   
    # Views pdf
    path('pdf/<str:namePDF>', views.pdfView),

    # Moi truong: Homepage
    path('environment/<int:idcate>', views.showsubjectsbyenvironment, name="showsubjectcate"),
    path('environment/more/', views.showsubjectsbyenvironment2, name="showsubjectcate2"),

    # Delete activity, item, lesson, chap, sub
    path('activity/<int:idact>/delete/', views.deleteactivity, name='deleteactivity'),
    path('item/<int:iditem>/delete/', views.deleteitem, name = 'deleteitem'),
    path('lesson/<int:idles>/delete/', views.deletelesson, name= 'deletelesson'),
    path('chapter/<int:idchap>/delete/', views.deletechapter, name= 'deletechapter'),
    path('subject/<int:idsub>/delete/', views.deletecourse, name='deletecourse'),

    # 
    path('course/manageteach', views.managecourseteacher, name="manageteach"),
    path('course/managesubmition',views.managesubmition,name="managesubmittion"),
    path('course/reviewsubmition/<int:idsubmit>',views.reviewsubmition,name="reviewsubmition"),

    path('ajax/ajaxcheckactivityreq', ajax.ajaxcheckactivityreq),
    path('ajax/ajaxcheckactivityreqcreate', ajax.ajaxcheckactivityreqcreate),
    
    path('course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/item/<int:iditem>/activity/special/create', views.activitySPECcreate, name="activitySPECcreate"),

    # manage course
    path('ajax/ajaxmanagecourseenvir', ajax.ajaxmanagecourseenvir),
    path('ajax/ajaxmanageteachpermit', ajax.ajaxmanageteachpermit),
    path('ajax/ajaxdelteach', ajax.ajaxdelteach),
    path('ajax/ajaxdomteach',ajax.ajaxdomteach),
    path('ajax/ajaxsearchsub',ajax.ajaxsearchsub),
    path('ajax/ajaxsearchusersub',ajax.ajaxsearchusersub),
    path('ajax/ajaxgetpoint', ajax.ajaxgetpoint),

    path('ajax/lookbf', ajax.ajaxlookbf),
    path('ajax/dellookbf', ajax.ajaxdellookbf),
]