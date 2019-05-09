from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


# Create your models here.
class AccountType(models.Model):
    accounttypeid = models.AutoField(db_column='AccountTypeID', primary_key=True)  # Field name made lowercase.
    accounttypename = models.CharField(db_column='AccountTypeName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'accounttype'



# Create your models here.
class Account(models.Model):
    accountid = models.AutoField(db_column='AccountID', primary_key=True)  # Field name made lowercase.
    # userdetailid = models.ForeignKey(UserDetail, models.DO_NOTHING, db_column='UserDetailID', blank=True, null=True)  # Field name made lowercase.
    accounttypeid = models.ForeignKey(AccountType, models.DO_NOTHING, db_column='AccountTypeID', blank=True, null=True)  # Field name made lowercase.
    #accounttypeid = models.IntegerField(db_column='AccountTypeID', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=250, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    resetcode = models.CharField(db_column='ResetCode', max_length=250, blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'account'



# Create your models here.
class UserDetail(models.Model):
    userdetailid = models.AutoField(db_column='UserDetailID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)
    firstname = models.CharField(db_column='FirstName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    birthday = models.DateField(db_column='Birthday', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=250, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber',  max_length=250, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=250, blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'userdetail'



# Create your models here.
class EnviromentCate(models.Model):
    enviromentcateid = models.AutoField(db_column='EnviromentCateID', primary_key=True)  # Field name made lowercase.
    enviromentcatename = models.CharField(db_column='EnviromentCateName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'enviromentcate'



# Create your models here.
class Subject(models.Model):
    subjectid = models.AutoField(db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    enviromentcateid = models.ForeignKey(EnviromentCate, models.DO_NOTHING, db_column='EnviromentCateID', blank=True, null=True)  # Field name made lowercase.
    subjectname = models.CharField(db_column='SubjectName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    introvideo = models.CharField(db_column='IntroVideo', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', max_length=250, blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'subject'



# Create your models here.
class SubjectPart(models.Model):
    subjectpartid = models.AutoField(db_column='SubjectPartID', primary_key=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    subjectpartname = models.CharField(db_column='SubjectPartName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'subjectpart'



class SubjectLike(models.Model):
    subjectlikeid = models.AutoField(db_column='SubjectLikeID', primary_key=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'subjectlike'



# Create your models here.
class Enrollment(models.Model):
    enrollmentid = models.AutoField(db_column='EnrollmentID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'enrollment'



# Create your models here.
class SubjectTeacher(models.Model):
    subjectteacherid = models.AutoField(db_column='SubjectTeacherID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'subjectteacher'



# Create your models here.   
class Chapter(models.Model):
    chapterid = models.AutoField(db_column='ChapterID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    chaptername = models.CharField(db_column='ChapterName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'chapter'



# Create your models here.
class Lesson(models.Model):
    lessonid = models.AutoField(db_column='LessonID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='ChapterID', blank=True, null=True)  # Field name made lowercase.
    lessonname = models.CharField(db_column='LessonName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'lesson'



# Create your models here.
class LessonReply(models.Model):
    lessonreplyid = models.AutoField(db_column='LessonReplyID', primary_key=True)  # Field name made lowercase.
    enrollmentid = models.ForeignKey(Enrollment, models.DO_NOTHING, db_column='EnrollmentID', blank=True, null=True)  # Field name made lowercase.
    lessonid = models.ForeignKey(Lesson, models.DO_NOTHING, db_column='LessonID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'lessonreply'



# Create your models here.
class Item(models.Model):
    itemid = models.AutoField(db_column='ItemID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    lessonid = models.ForeignKey(Lesson, models.DO_NOTHING, db_column='LessonID', blank=True, null=True)  # Field name made lowercase.
    itemname = models.CharField(db_column='ItemName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'item'



# Create your models here.
class ActivityType(models.Model):
    activitytypeid = models.  AutoField(db_column='ActivityTypeID', primary_key=True)  # Field name made lowercase.
    activitytypename = models.CharField(db_column='ActivityTypeName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'activitytype'



# Create your models here.      
class Activity(models.Model):
    activityid = models.AutoField(db_column='ActivityID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    requiredactivityid = models.ForeignKey('self', models.DO_NOTHING, db_column='RequiredActivityID', blank=True, null=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemID', blank=True, null=True)  # Field name made lowercase.
    activitytypeid = models.ForeignKey(ActivityType, models.DO_NOTHING, db_column='ActivityTypeID', blank=True, null=True)  # Field name made lowercase.
    # activitytype = models.TextField(db_column='ActivityType', blank=True, null=True)  # Field name made lowercase.
    activityname = models.CharField(db_column='ActivityName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    time = models.IntegerField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    description = RichTextUploadingField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'activity'



class ActivityReply(models.Model):
    activityreplyid = models.AutoField(db_column='ActivityReplyID', primary_key=True)  # Field name made lowercase.
    enrollmentid = models.ForeignKey(Enrollment, models.DO_NOTHING, db_column='EnrollmentID', blank=True, null=True)  # Field name made lowercase.
    activityid = models.ForeignKey(Activity, models.DO_NOTHING, db_column='ActivityID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    rate = models.IntegerField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'activityreply'



# Create your models here.
class ActivitySubmittion(models.Model):
    activitysubmittionid = models.AutoField(db_column='ActivitySubmittionID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    activityid = models.ForeignKey(Activity, models.DO_NOTHING, db_column='ActivityID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=199, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'activitysubmittion'



# Create your models here.
class ActivitySubmittionReply(models.Model):
    activitysubmittionreplyid = models.AutoField(db_column='ActivitySubmittionReplyID', primary_key=True)  # Field name made lowercase.
    enrollmentid = models.ForeignKey(Enrollment, models.DO_NOTHING, db_column='EnrollmentID', blank=True, null=True)  # Field name made lowercase.
    activitysubmittionid = models.ForeignKey(ActivitySubmittion, models.DO_NOTHING, db_column='ActivitySubmittionID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'activitysubmittionreply'



# Create your models here.
class Tracking(models.Model):
    trackingid = models.AutoField(db_column='TrackingID', primary_key=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    subjectpartid = models.ForeignKey(SubjectPart, models.DO_NOTHING, db_column='SubjectPartID', blank=True, null=True)  # Field name made lowercase.
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='ChapterID', blank=True, null=True)  # Field name made lowercase.
    lessonid = models.ForeignKey(Lesson, models.DO_NOTHING, db_column='LessonID', blank=True, null=True)  # Field name made lowercase.
    #lessonid = models.ForeignKey(db_column='LessonID', blank=True, null=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemID', blank=True, null=True)  # Field name made lowercase.
    activityid = models.ForeignKey(Activity, models.DO_NOTHING, db_column='ActivityID', blank=True, null=True)  # Field name made lowercase.
    enrollmentid = models.ForeignKey(Enrollment, models.DO_NOTHING, db_column='EnrollmentID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tracking'


# Create your models here.
class UserRank(models.Model):
    userrankid = models.AutoField(db_column='UserRankID', primary_key=True)  # Field name made lowercase.
    enviromentcateid = models.ForeignKey(EnviromentCate, models.DO_NOTHING, db_column='EnviromentCateID', blank=True, null=True)  # Field name made lowercase.
    userrankname = models.CharField(db_column='UserRankName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(db_column='Icon', max_length=250, blank=True, null=True)  # Field name made lowercase.
    requiredlevel = models.IntegerField(db_column='RequiredLevel', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'userrank'


# Create your models here.
class Contact(models.Model):
    contactid = models.AutoField(db_column='ContactID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'contact'


# Create your models here.
class Forum(models.Model):
    forumtopicid = models.AutoField(db_column='ForumTopicID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    enviromentcateid = models.ForeignKey('Enviromentcate', models.DO_NOTHING, db_column='EnviromentCateID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    forumtopicname = models.CharField(db_column='ForumTopicName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    likecount = models.IntegerField(db_column='LikeCount', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'forum'



# Create your models here.
class ForumLike(models.Model):
    forumlikeid = models.AutoField(db_column='ForumLikeID', primary_key=True)  # Field name made lowercase.
    forumtopicid = models.ForeignKey(Forum, models.DO_NOTHING, db_column='ForumTopicID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'forumlike'



# Create your models here.
class ForumReply(models.Model):
    forumreplyid = models.AutoField(db_column='ForumReplyID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    forumtopicid = models.ForeignKey(Forum, models.DO_NOTHING, db_column='ForumTopicID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'forumreply'



# Create your models here.
class ProjectShare(models.Model):
    projectsharetopicid = models.AutoField(db_column='ProjectShareTopicID', primary_key=True)  # Field name made lowercase.
    enviromentcateid = models.ForeignKey(EnviromentCate, models.DO_NOTHING, db_column='EnviromentCateID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    projectsharetopicname = models.CharField(db_column='ProjectShareTopicName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    likecount = models.IntegerField(db_column='LikeCount', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'projectshare'



# Create your models here.
class ProjectShareLike(models.Model):
    projectsharelikeid = models.AutoField(db_column='ProjectShareLikeID', primary_key=True)  # Field name made lowercase.
    projectsharetopicid = models.ForeignKey(ProjectShare, models.DO_NOTHING, db_column='ProjectShareTopicID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'projectsharelike'



# Create your models here.
class ProjectShareReply(models.Model):
    projectsharereplyid = models.AutoField(db_column='ProjectShareReplyID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    projectsharetopicid = models.ForeignKey(ProjectShare, models.DO_NOTHING, db_column='ProjectShareTopicID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'projectsharereply'



# Create your models here.
class News(models.Model):
    newsid = models.AutoField(db_column='NewsID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    enviromentcateid = models.ForeignKey(EnviromentCate, models.DO_NOTHING, db_column='EnviromentCateID', blank=True, null=True)  # Field name made lowercase.
    newsname = models.CharField(db_column='NewsName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'news'



# Create your models here.
class NewsReply(models.Model):
    newsreplyid = models.AutoField(db_column='NewsReplyID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    newsid = models.ForeignKey(News, models.DO_NOTHING, db_column='NewsID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'newsreply'



# Create your models here.
class Competition(models.Model):
    competitionid = models.AutoField(db_column='CompetitionID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    enviromentcateid = models.ForeignKey(EnviromentCate, models.DO_NOTHING, db_column='EnviromentCateID', blank=True, null=True)  # Field name made lowercase.
    competitionname = models.CharField(db_column='CompetitionName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    opendate = models.DateTimeField(db_column='OpenDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    likecount = models.IntegerField(db_column='LikeCount', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'competition'



# Create your models here.
class CompetitionSubmittion(models.Model):
    competitionsubmittionid = models.AutoField(db_column='CompetitionSubmittionID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    competitionid = models.ForeignKey(Competition, models.DO_NOTHING, db_column='CompetitionID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'competitionsubmittion'



# Create your models here.
class CompetitionSubmittionLike(models.Model):
    competitionsubmittionlikeid = models.AutoField(db_column='CompetitionSubmittionLikeID', primary_key=True)  # Field name made lowercase.
    competitionsubmittionid = models.ForeignKey(CompetitionSubmittion, models.DO_NOTHING, db_column='CompetitionSubmittionID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'competitionsubmittionlike'



# Create your models here.
class CompetitionSubmittionReply(models.Model):
    competitionsubmittionreplyid = models.AutoField(db_column='CompetitionSubmittionReplyID', primary_key=True)  # Field name made lowercase.
    competitionsubmittionid = models.ForeignKey(CompetitionSubmittion, models.DO_NOTHING, db_column='CompetitionSubmittionID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content')  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate')  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'competitionsubmittionreply'



# Create your models here.
class FastChat(models.Model):
    fastchatid = models.AutoField(db_column='FastChatID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'fastchat'


# Create your models here.
class Introduction(models.Model):
    introductionid = models.AutoField(db_column='IntroductionID', primary_key=True)  # Field name made lowercase.
    introductionname = models.CharField(db_column='IntroductionName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=250, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'introduction'   


    
# Create your models here.
class Home(models.Model):
    homeid = models.AutoField(db_column='HomeID', primary_key=True)  # Field name made lowercase.
    homename = models.CharField(db_column='HomeName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=250, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'home'



# Create your models here.
class Header(models.Model):
    headerid = models.AutoField(db_column='HeaderID', primary_key=True)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    headername = models.CharField(db_column='HeaderName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=250, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'header'



# Create your models here.
class Footer(models.Model):
    footerid = models.AutoField(db_column='FooterID', primary_key=True)  # Field name made lowercase.
    footername = models.CharField(db_column='FooterName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=250, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'footer'



# Create your models here.
class SlideRunBar(models.Model):
    sliderunbarid = models.AutoField(db_column='SlideRunBarID', primary_key=True)  # Field name made lowercase.
    sliderunbarname = models.CharField(db_column='SlideRunBarName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    isenable = models.IntegerField(db_column='IsEnable', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=250, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'sliderunbar'



class GameType(models.Model):
    gametypeid = models.AutoField(db_column='GameTypeID', primary_key=True)  # Field name made lowercase.
    gametypename = models.CharField(db_column='GameTypeName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'gametype'

class Game(models.Model):
    gameid = models.AutoField(db_column='GameID', primary_key=True)  # Field name made lowercase.
    gametypeid = models.ForeignKey(GameType, models.DO_NOTHING, db_column='GameTypeID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID', blank=True, null=True)  # Field name made lowercase.
    gamename = models.CharField(db_column='GameName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.
    content = RichTextUploadingField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=250, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'game'

class GameRate(models.Model):
    gamerateid = models.AutoField(db_column='GameRateID', primary_key=True)  # Field name made lowercase.
    gameid = models.ForeignKey(Game, models.DO_NOTHING, db_column='GameID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    rate = models.IntegerField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'gamerate'


class Online(models.Model):
    onlineid = models.AutoField(db_column='OnlineID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    isonline = models.IntegerField(db_column='Isonline', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'online'

class ChatRoom(models.Model):
    chatroomid = models.AutoField(db_column='ChatRoomID', primary_key=True)  # Field name made lowercase.
    supportid = models.ForeignKey(Online, models.DO_NOTHING, db_column='OnlineID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    
    class Meta: 
        managed = True
        db_table = 'chatroom'

class Chat(models.Model):
    chatid = models.AutoField(db_column='ChatID', primary_key=True)  # Field name made lowercase.
    chatroomid = models.ForeignKey(ChatRoom, models.DO_NOTHING, db_column='ChatRoomID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=250, blank=True, null=True)  # Field name made lowercase.
   
    class Meta:
        managed = True
        db_table = 'chat'

