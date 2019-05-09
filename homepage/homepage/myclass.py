class SubjectMaster:
    def __init__(self, subject, avgRate, countAR, sumTime, sublike, cate):
        self.subject = subject # class Subject
        self.avgRate = avgRate
        self.countAR = countAR
        self.sumTime = sumTime
        self.sublike = sublike
        self.cate = cate

class TimeNameChapter:
    def __init__(self, name, time, time2):
        self.name = name
        self.time = time
        self.time2 = time2

class rateStarDetail:
    def __init__(self, star1, perstar1, star2, perstar2, star3, perstar3, star4, perstar4, star5, perstar5, sum, sumavg):
        self.star1 = star1
        self.perstar1 = perstar1
        self.star2 = star2
        self.perstar2 = perstar2
        self.star3 = star3
        self.perstar3 = perstar3
        self.star4 = star4
        self.perstar4 = perstar4
        self.star5 = star5
        self.perstar5 = perstar5
        self.sum = sum
        self.sumavg = sumavg

class newestComment:
    def __init__(self, avatar, rate, username, date, content):
        self.avatar= avatar
        self.rate =rate
        self.username =username
        self.date= date
        self.content=content

class TeacherDetails:
    def __init__(self, name, avatar, account):
        self.name = name
        self.avatar = avatar
        self.account=account

class SubPartDetail:
    def __init__(self, avgRate, countAR, sumTime, sublikes):
        self.avgRate = avgRate
        self.countAR = countAR
        self.sumTime = sumTime
        self.sublikes = sublikes

class ChapAndLess:
    def __init__(self, chapterid, chapter, listlesson, numChapid,checkpass):
        self.chapterid = chapterid
        self.chapter = chapter
        self.listlesson = listlesson
        self.numChapid = numChapid
        self.checkpass=checkpass
    
class ItemAndActivity:
    def __init__(self, item, listactivity):
        self.item =item
        self.listactivity=listactivity

class LessonReplyAccount:
    def __init__(self, lessonreply, account):
        self.lessonreply = lessonreply
        self.account = account

class ActivityReplyAccount:
    def __init__(self, activityreply, account):
        self.activityreply = activityreply
        self.account = account

class ChapterProcess:
    def __init__(self, order, chapter, iscomplete):
        self.order = order
        self.chapter = chapter
        self.iscomplete = iscomplete

class ActivityProcess:
    def __init__(self, order, activity, iscomplete):
        self.order = order
        self.activity = activity
        self.iscomplete = iscomplete

class ClassDashBoard:
    def __init__(self, subject, countAllAct, countACT, percent):
        self.subject = subject
        self.countAllAct = countAllAct
        self.countACT = countACT
        self.percent = percent

class ChapDashBoard:
    def __init__(self, chapter, percent, lesson, orderchap, showpercent):
        self.chapter = chapter
        self.percent = percent
        self.lesson = lesson
        self.orderchap = orderchap
        self.showpercent = showpercent

class LessonDashBoard:
    def __init__(self, lesson, classacts, devidepercent, sumpercent, orderlesson):
        self.lesson = lesson
        self.classacts = classacts
        self.devidepercent = devidepercent
        self.sumpercent = sumpercent
        self.orderlesson = orderlesson

class ActDashBoard:
    def __init__(self, activity, checkpass, order):
        self.activity = activity
        self.checkpass = checkpass
        self.order = order
 
class Level:
    def __init__(self, level, sumexp, expperleft):
        self.level = level
        self.sumexp = sumexp
        self.expperleft = expperleft
		
class Rank:
    def __init__(self,avatar, name):
        self.avatar = avatar
        self.name = name
       

class ChapAndLessSimple:
    def __init__(self, chapter, classlessons, count):
        self.chapter = chapter
        self.classlessons = classlessons
        self.count = count

class LessAndItemSimple:
    def __init__(self, lesson, items, count):
        self.lesson = lesson
        self.items = items
        self.count = count

class ItemAndActSimple:
    def __init__(self, item, activities, count):
        self.item = item
        self.activities = activities
        self.count = count

class ClassCompetition:
    def __init__(self, competition, star, person):
        self.competition = competition
        self.star = star
        self.person = person


class RankCompetition:
    def __init__(self, comsubmit, comsublike):
        self.comsubmit = comsubmit
        self.comsublike = comsublike

class RankName:
    def __init__(self, classrankcom, rankorder):
        self.classrankcom = classrankcom
        self.rankorder = rankorder

class ProShare:
    def __init__(self, projectshare, countlike):
        self.projectshare = projectshare
        self.countlike = countlike
		
# hàm load userdetail dựa vào forum.accountid
class ForumUserdetail:
    def __init__(self, forum, userdetail):
        self.forum = forum
        self.userdetail = userdetail

# hàm load userdetail dựa vào forumreply.accountid
class ForumReplyUserdetail:
    def __init__(self, forumreply, userdetail):
        self.forumreply = forumreply
        self.userdetail = userdetail

# hàm load userdetail dựa vào news.accountid
class NewsUserdetail:
    def __init__(self, news, userdetail):
        self.news = news
        self.userdetail = userdetail

# hàm load userdetail dựa vào newsreply.accountid
class NewsReplyUserdetail:
    def __init__(self, newsreply, userdetail):
        self.newsreply = newsreply
        self.userdetail = userdetail

# thanh vien tich cuc
class UserDetailActivityRep:
    def __init__(self, account, name, numrep, numenroll):
        self.account = account
        self.name = name
        self.numrep = numrep
        self.numenroll = numenroll


class GameAndRate:
    def __init__(self, game, rate, view, date):
        self.game = game
        self.rate = rate
        self.view = view
        self.date = date

class GamePopNew:
    def __init__(self, populargame, newgame):
        self.populargame = populargame
        self.newgame = newgame


class AccountUserdetail:
    def __init__(self, account, userdetail):
        self.account = account
        self.userdetail = userdetail

