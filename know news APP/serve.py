from flask import Flask,render_template,request,redirect,url_for,session,jsonify,make_response
# redirect 重定向
import pymysql,hashlib,math,re,os,datetime,random

# 连接数据库
db = pymysql.connect(host="localhost",user="root",password="",db="newsnews")
# 创建游标
cur = db.cursor()

app = Flask(__name__)
# 生成密钥
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# 前台
@app.route('/')
def index():
    sql = "select * from users "
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    sql1 = "select * from news order by news.id desc"
    cur.execute(sql1)
    res1 = cur.fetchall()

    arr = []
    for item in res1:
        arr.append(list(item))

    for item in arr:
        item[6] = item[6].split(",")

    sql="select * from newscategory"
    cur.execute(sql)
    res2=cur.fetchall()


    sql = "select * from news where cid=2"
    cur.execute(sql)
    res3 = cur.fetchall()
    print(res3)
    arr3 = []
    for item in res3:
        arr3.append(list(item))

    for item in arr3:
        item[6] = item[6].split(",")
    sql = "select * from news where cid=3"
    cur.execute(sql)
    res4 = cur.fetchall()
    arr4 = []
    for item in res4:
        arr4.append(list(item))

    for item in arr4:
        item[6] = item[6].split(",")
    sql = "select * from news where cid=4"
    cur.execute(sql)
    res5 = cur.fetchall()
    arr5 = []
    for item in res5:
        arr5.append(list(item))

    for item in arr5:
        item[6] = item[6].split(",")
    sql = "select * from news where cid=5"
    cur.execute(sql)
    res6 = cur.fetchall()
    arr6 = []
    for item in res6:
        arr6.append(list(item))

    for item in arr6:
        item[6] = item[6].split(",")
    sql = "select * from news where cid=6"
    cur.execute(sql)
    res7 = cur.fetchall()
    arr7 = []
    for item in res7:
        arr7.append(list(item))

    for item in arr7:
        item[6] = item[6].split(",")
    sql = "select * from news where cid=7"
    cur.execute(sql)
    res8 = cur.fetchall()
    arr8 = []
    for item in res8:
        arr8.append(list(item))

    for item in arr8:
        item[6] = item[6].split(",")
    return render_template("/news-master/index.html",data=res,data1=arr,data2=res2,data3=arr3,data4=arr4,data5=arr5,data6=arr6,data7=arr7,data8=arr8,)
@app.route("/category")
def category():
    sql="select * from news left join classify on news.id=classify.n_id left join (select c.id from newscategory) as c on classify.c_id=c.name where c.id=%s"%id
    print(sql)
    cur.execute(sql)
    res=cur.fetchall()
    print(res)
    return render_template("/news-master/index.html",data=res)
@app.route("/xq<id>")
def xq(id):
    sql="select * from news where id=%s"%id
    cur.execute(sql)
    res=cur.fetchall()

    sql="select account from users"
    cur.execute(sql)
    account=cur.fetchone()[0]

    sql = "select account,u_time,word,id from comment where n_id=%s" % id
    cur.execute(sql)
    comment=cur.fetchall()
    u_id=""
    for item in comment:
        u_id=item[3]
    print(u_id)
    # sql = "select account,u_time,word,id from comment where u_id=%s" % u_id
    # cur.execute(sql)
    # huifu = cur.fetchall()
    # print(huifu)


    # 相关新闻推荐

    sql = "select group_concat(n_keywords) from news_keywords where n_id=%s"%id
    cur.execute(sql)
    keyword = cur.fetchone()[0]
    try:
        # 不一定所有的都有关键字
        arr0 = set(keyword.split(","))
    except:
        arr0 = set()

    sql = "select n_id,group_concat(n_keywords) from news_keywords group by n_id"
    cur.execute(sql)
    # 获取所有关键字
    newskeywords = cur.fetchall()
    newskeywordsdict = {}
    for item in newskeywords:
        newskeywordsdict[item[0]] = set(item[1].split(","))

    newskeywordsdictnum = {}
    for k, v in newskeywordsdict.items():
        newskeywordsdictnum[k] = len(v & arr0)

    newid = []
    for k, v in newskeywordsdictnum.items():
        if v > 0 and k != int(id):
            newid.append(str(k))
    tuijian=[]
    if newid:
        sql2 = "select id,name,author,c_time,imgurl from news where id in (%s)" % (",".join(newid))
        cur.execute(sql2)
        tuijian1 = cur.fetchall()
        tuijian.append(tuijian1[0])
    return render_template("/news-master/xq.html",data=res,data1=tuijian,keyword=arr0,n_id=id,account=account,comment=comment,u_id=u_id)



# 增加评论
@app.route("/comment",methods=['post'])
def comment():
    if 'account' in session:
        comment = request.form['comment']
        n_id=request.form['n_id']
        account=request.form['account']
        sql="insert into comment (word,n_id,account,u_id) values ('%s',%s,%s,0)"%(comment,n_id,account)
        cur.execute(sql)
        db.commit()
        sql="select * from comment where word='%s'"%comment
        cur.execute(sql)
        res=cur.fetchall()
        resres=list(res)
        id=""
        u_time=""
        account=""
        for item in resres:
            id=item[0]
            u_time=item[4]
            account=item[1]
        rep={'info':'ok','id':id,'u_time':u_time,"account":account}
        return jsonify(rep)
    else:
        return redirect(url_for("login1"))

# 打开弹框回复
@app.route("/huifu",methods=['post'])
def huifu():
    # comment=request.form['comment1']
    # print(comment)
    u_id=request.form['u_id']
    sql = "select * from comment where id='%s'" % u_id
    print(sql)
    cur.execute(sql)
    res=cur.fetchall()
    print(res)
    rep=""
    for item in res:
        rep={'info':'ok','account':item[1],'word':item[2],'u_time':item[4]}
    print(rep)
    return jsonify(rep)
# 增加回复
@app.route("/addhuifu",methods=['post'])
def addhuifu():
    hfhf = request.form['hfhf']
    u_id = request.form['u_id']
    n_id=request.form['n_id']
    account = request.form['account']
    sql = "insert into comment (word,n_id,u_id,account) values ('%s',%s,%s,%s)" % (hfhf,n_id,u_id,account)
    print(sql)
    cur.execute(sql)
    db.commit()
    sql = "select * from comment where word='%s'" % hfhf
    cur.execute(sql)
    res = cur.fetchall()
    resres = list(res)
    id = ""
    u_time = ""
    account = ""
    for item in resres:
        id = item[0]
        u_time = item[4]
        account = item[1]
    rep = {'info': 'ok', 'id': id, 'u_time': u_time, "account": account}
    return jsonify(rep)
@app.route("/addhf3",methods=['post'])
def addhf3():
    addhf3=request.form['addhf3']
    print(addhf3)
    u_id=request.form['u_id']
    print(u_id)
    account=request.form['account']
    sql = "insert into comment (word,u_id,account) values ('%s',%s,%s)" % (addhf3,u_id,account)
    print(sql)
    cur.execute(sql)
    db.commit()
    sql = "select * from comment where word='%s'" % addhf3
    cur.execute(sql)
    res = cur.fetchall()
    resres = list(res)
    id = ""
    u_time = ""
    account = ""
    for item in resres:
        id = item[0]
        u_time = item[4]
        account = item[1]
    rep = {'info': 'ok', 'id': id, 'u_time': u_time, "account": account}
    return jsonify(rep)
# 三级回复获取数据

@app.route("/listComments",methods=['post'])
def listComments():
    n_id = request.form['n_id']
    print(n_id)
    cur = db.cursor()
    sql = "select * from comment where n_id=%s"%n_id
    cur.execute(sql)
    res = cur.fetchall()
    print(res)
    data = {}
    cj = []
    for item in res:
        fun(cj,item[0],item[6])
        data[item[0]] = {'con':item[2],'account':item[1],'u_id':item[6]}

    print(data)
    print(cj)
    return jsonify({'data':data,'cj':cj})
#  给你一个 评论id 把评论id 放在 cj层次结构里
def fun(cj,id,u_id):
    if u_id==0:
        cj.append([id,[]])
        return
    for arr in cj:
        if arr[0]==u_id:
            arr[1].append([id,[]])
        else:
            fun(arr[1],id,u_id)

# 收藏
@app.route("/collect",methods=['post'])
def collect():
    id=request.form['nid']
    print(id)
    sql = "update news set collect=1 where id=%s" % id
    print(sql)
    cur.execute(sql)
    db.commit()
    return "ok"
    # return render_template("/news-master/xq.html")
# 打开收藏页面
@app.route("/opencollect")
def opencollect():
    sql="select * from news where collect=1"
    cur.execute(sql)
    res=cur.fetchall()
    print(res)
    arr = []
    for item in res:
        arr.append(list(item))

    for item in arr:
        item[6] = item[6].split(",")
    return render_template("/news-master/mine.html",data=arr)
# 登录后页面 我的 页面
@app.route("/newslogin")
def newslogin():
    if 'account'in session:
        account1=session['account']
        sql = "select * from users where account='%s'"%account1
        print(sql)
        cur.execute(sql)
        db.commit()
        res = cur.fetchall()
        return render_template("/news-master/login.html",account=session['account'],data=res)
    else:
        return redirect(url_for("login2"))

# 打开编辑资料页面
@app.route("/openeditdata")
def openeditdata():
    account = session['account']
    sql="select * from users where account='%s'"%account
    cur.execute(sql)
    db.commit()
    res=cur.fetchall()
    return render_template("/news-master/geren.html",account=account,data=res)
# 编辑头像
@app.route("/uploadPimg",methods=['post'])
def uploadPimg():
    f=request.files['imgurl']
    account = request.form['account3']
    imgurl="static/img/touxiang/"+f.filename
    print(imgurl)
    f.save(imgurl)
    imgurl1='/'+imgurl
    sql="update users set imgurl='%s' where account='%s'"%(imgurl1,account)
    print(sql)
    cur.execute(sql)
    db.commit()
    rep={'info':'ok','imgurl':imgurl1}
    return jsonify(rep)
# 编辑昵称
@app.route("/editdata",methods=['post'])
def editdata():
    name=request.form['nicheng']
    account=request.form['account1']
    sql="update users set name='%s' where account='%s'"%(name,account)
    print(sql)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("openeditdata"))
# 编辑介绍
@app.route("/editdata1",methods=['post'])
def editdata1():
    jieshao=request.form['jieshao']
    account = request.form['account2']
    sql="update users set jieshao='%s' where account='%s'"%(jieshao,account)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("openeditdata"))
# 打开注册页面
@app.route("/openzhuce")
def openzhuce():
    return render_template("/news-master/zhuce.html")
@app.route("/zhuce",methods=['post'])
def zhuce():
    account=request.form['account']
    # 手机号码的正则验证 var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;
    ret = re.match(r"^1[35678]\d{9}$", account)
    if ret:
        sql="insert into users(account,name,jieshao,imgurl) values(%s,'修改昵称','这个人很懒，什么也没有留下','static/img/moren.png') "%account
        cur.execute(sql)
        db.commit()
        return render_template("/news-master/zhuce.html")
    else:
        return redirect(url_for("tips", state="no", href="openzhuce", time=3))

# 用户登录页面
@app.route("/login1")
def login1():
    return render_template("/news-master/login1.html")
# 检测登录，登录账号是否存在
@app.route("/checklogin1",methods=['post'])
def checklogin1():
    account=request.form['account']
    print(account)

    sql="select account from users where account='%s'"%account
    cur.execute(sql)
    account0 = ""
    res=cur.fetchone()

    if res!=None:
        account0 = res[0]
        print(account0)
    if account0==account:
        session['account']=account
        return redirect(url_for("newslogin"))
    else:
        return redirect(url_for("tips",state="no",href="openzhuce",time=3))

# 去登录
@app.route("/login2")
def login2():
    return render_template("/news-master/login2.html")
# # 退出登录
@app.route("/loginout1")
def loginout1():
    if 'account' in session:
        del session['account']
    return render_template("/news-master/login2.html")
# 后台
# 后台管理主页
@app.route("/admin")
def admin():
    if 'username' in session:
        return render_template("/blue-master/index.html",level=session['level'])
    else:
        return redirect(url_for("login"))
@app.route("/login")
def login():
    return render_template("blue-master/login.html")
@app.route("/loginout")
def loginout():
    del session['username']
    del session['level']
    return render_template("blue-master/login.html")

@app.route("/checklogin",methods=['post'])
def checklogin():
    username=request.form['username']
    password = request.form['password']
    # 加密密码
    s = hashlib.md5()
    s.update(password.encode())
    password=s.hexdigest()
    # print(password)
    sql="select password,level from admin where username = '%s'"%username
    cur.execute(sql)
    password0=""

    res=cur.fetchone()

    if res!=None:
        password0 = res[0]
    if password0 == password:
        session['username']=username
        session['level'] = res[1]
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("tips",state="no",href="login",time=3))

@app.route("/tips/<state>/<href>/<time>")
def tips(state,href,time):
    return render_template("blue-master/tips.html",state=state,href=href,time=time)
# 打开添加管理员
@app.route("/openadduser")
def openadduser():
    if 'username' in session:
        if session['level']==1:
            return render_template("/blue-master/adduser.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("tips",state="no",href="admin",time=3))
@app.route("/adduser",methods=['post'])
def adduser():
    if 'username' in session:
        if 'username' in session:
            username = request.form['username']
            newpass = request.form['newpass']
            renewpass = request.form['renewpass']
            if username != "" and newpass != "" and renewpass != "":
                if newpass == renewpass:
                    s = hashlib.md5()
                    s.update(newpass.encode())
                    password = s.hexdigest()
                    sql = "insert into admin(username,password,level) values('%s','%s',%s)" % (username, password, 2)
                    cur.execute(sql)
                    db.commit()
                    return redirect(url_for("tips", state="yes", href="openadduser", time=3))
                else:
                    return redirect(url_for("tips", state="no", href="openadduser", time=3))
            else:
                return redirect(url_for("tips", state="no", href="openadduser", time=3))
        else:
            return redirect(url_for("login"))
# 查看管理员
@app.route("/listuser<page>")
def listuser(page):
    page = int(page)
    if 'username' in session:
        sql = "select count(*) from admin"
        cur.execute(sql)
        length=cur.fetchone()[0]
        #  a,b 每一页从a 开始显示b条
        sql = "select id,username,level from admin limit %s,2" % ((page-1)*2)
        cur.execute(sql)
        res = cur.fetchall()
        pages = range(1, math.ceil(length/2)+1)
        return render_template("/blue-master/listuser.html", data=res, pages=pages, now=page)
    else:
        return redirect(url_for("login"))
# 修改
# 打开修改页面
@app.route("/openedituser<id>_<username>")
def openedituser(id,username):
    if 'username' in session and session['level']==1:
        return render_template("/blue-master/edituser.html",id=id,username=username)
@app.route("/edituser",methods=['post'])
def edituser():
    if 'username' in session and session['level'] == 1:
        id=request.form['id']
        username = request.form['username']
        mpass=request.form['mpass'] #原始密码
        newpass=request.form['newpass'] #新密码

        s = hashlib.md5()
        s.update(mpass.encode())
        mpass = s.hexdigest()
        sql="select password from admin where id=%s"%id
        cur.execute(sql)
        res=cur.fetchone()[0]

        if res==mpass:
            h = hashlib.md5()
            h.update(newpass.encode())
            newpass = h.hexdigest()
            sql="update admin set password='%s' where id=%s"%(newpass,id)
            cur.execute(sql)
            db.commit()
            return redirect(url_for("tips",state="yes",href="listuser1",time=3))
        else:
            return redirect(url_for("tips",state="no",href="openedituser%s_%s"%(id,username),time=3))
#  删除
@app.route("/deluser<name>")
def deluser(name):
    if name != "admin":#超级管理员不能删除
        try:
            sql = "delete from admin where username='%s'" % (name)
            cur.execute(sql)
            db.commit()
            return redirect(url_for("tips", state="yes", href="listuser1", time=3))
        except:
            db.rollback()#数据回滚 提交错误时 返回到提交时
            return redirect(url_for("tips",state="no",href="listuser1",time=3))
    else:
        return redirect(url_for("tips", state="no", href="listuser1", time=3))

# 头条首页数据
# 打开添加新闻分类
@app.route("/openaddnewscategory")
def openaddnewscategory():
    sql = "select id,name from newscategory  "
    cur.execute(sql)
    res = cur.fetchall()
    return render_template("/blue-master/addnewscategory.html",data=res)
# 添加产品分类
@app.route("/addnewscategory",methods=['post'])
def addnewscategory():
    name=request.form['name']
    sql="insert into newscategory (name) values ('%s')"%name
    cur.execute(sql)
    db.commit()
    sql="select id from newscategory where name='%s'"%name
    cur.execute(sql)
    id=cur.fetchone()[0]
    rep={'info':'ok','id':id}
    print(rep)
    return jsonify(rep)

# 判断添加种类不重复
@app.route("/selectnewscategory",methods=['post'])
def selectpcategory():
    name = request.form['name']
    sql="select count(*) from newscategory where name='%s'"%name
    cur.execute(sql)
    length = cur.fetchone()[0]
    print(length)
    if length>0:
        return "no"
    else:
        return "yes"
# 删除新闻分类
@app.route("/delnewscategory",methods=['post'])
def delpcategory():
    id = request.form['id']
    print(id)
    sql="delete from newscategory where id='%s'"%id
    cur.execute(sql)
    db.commit()
    return "ok"

# 打开修改页面
@app.route("/openeditnewscategory<id>_<name>")
def openeditnewscategory(id,name):
    return render_template("/blue-master/editnewscategory.html",id=id,name=name)
# 修改种类名称
@app.route("/editnewscategory",methods=['post'])
def editnewscategory():
    id=request.form['id']
    name=request.form['name']
    newname = request.form['newname']
    sql = "update newscategory set name='%s' where name='%s'" % (newname,name)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openaddnewscategory", time=3))
#  打开添加新闻页面
@app.route("/openaddnews")
def openaddnews():
    sql="select * from newscategory"
    cur.execute(sql)
    db.commit()
    res=cur.fetchall()
    sql = "select * from keywords"
    cur.execute(sql)
    db.commit()
    res1 = cur.fetchall()
    return render_template("/blue-master/addnews.html",data=res,data1=res1)

# 添加新闻 插入富文本编辑器
@app.route("/addnews",methods=['post'])
def addnews():
    name=request.form['title']
    author=request.form['author']
    comment=request.form['comment']
    cid=request.form.getlist('cid')
    keywords = request.form['keywords']
    print(cid)
    con = request.form['con']
    print(con)
    #从富文本编辑器截取图片
    img=re.findall(r'<img alt="" src="(.*?).(jpg|png|jpeg|gif)"',con)
    imgurl=",".join(img)

    list = imgurl.split(",")
    length = len(list)
    print(imgurl)
    print(length)
    sql="insert into news (name,author,comment,con,imgurl,s_id,length) values ('%s','%s',%s,'%s','%s',0,%s)"%(name,author,comment,con,imgurl,length)
    cur.execute(sql)
    db.commit()

    sql = "select id from news where name='%s'"%name
    cur.execute(sql)
    res= cur.fetchone()[0]
    # 关联分类表中插入分类
    for item in cid:
        sql = "insert into classify (n_id,c_id) values (%s,'%s')" % (res,item)
        print(sql)
        cur.execute(sql)
        db.commit()
    keywords_list=keywords.split("，")
    # 关联分类表中插入关键字
    for item1 in keywords_list:
        sql = "insert into news_keywords (n_id,n_keywords) values (%s,'%s')" % (res, item1)
        print(sql)
        cur.execute(sql)
        db.commit()
    return redirect(url_for("tips", state="yes", href="openaddnews", time=3))

#
#     str=""
#     for item in cid:
#         str+="(%s,'%s'),"%(res,item)
#         print(str)
#     sql = "insert into classify (n_id,c_id) values " +str[:-1]
#     cur.execute(sql)
#     db.commit()

# 查看新闻列表
@app.route("/listnews<page>")
def listnews(page):
    page = int(page)
    sql = "select count(*) from news"
    cur.execute(sql)
    length = cur.fetchone()[0]
    sql = "select n.id,n.name,n.con,n.author,n.c_time,c_id,n_keywords,n.s_id,n.comment from news as n left join (select c.n_id,group_concat(c.c_id) as c_id from classify as c group by c.n_id) " \
          "as c on n.id=c.n_id left join (select k.n_id,group_concat(k.n_keywords) as n_keywords from news_keywords as k group by k.n_id) as k on n.id=k.n_id order by n.id desc limit %s,10" %((page - 1) * 10)
    cur.execute(sql)
    res = cur.fetchall()
    print(sql)
    print(res)
    pages = range(1, math.ceil(length / 10) + 1)
    return render_template("/blue-master/listnews.html", data=res, pages=pages, now=page)
# 新闻发布状态
@app.route("/newssend<id>")
def newssend(id):
    sql="update news set s_id=1 where id=%s"%id
    cur.execute(sql)
    db.commit()
    return "ok"
# 新闻撤回状态
@app.route("/newsback<id>")
def newsback(id):
    sql="update news set s_id=0 where id=%s"%id
    cur.execute(sql)
    db.commit()
    return "ok"
# 删除新闻
#  删除某个产品
@app.route("/delnews<name>")
def delnews(name):
    try:
        sql="delete from news where name='%s'"%name
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()  #回滚，出现错误信息的时候回滚到出错之前
        return redirect(url_for("tips",state="no", href="listnews1", time=3))
    return redirect(url_for("tips",state="yes",href="listnews1",time=3))
# 打开修改产品详情页面
@app.route("/openeditnews<id>_<name>")
def openeditnews(id,name):
    sql = "select * from newscategory"
    cur.execute(sql)
    db.commit()
    res = cur.fetchall()
    sql = "select * from keywords"
    cur.execute(sql)
    db.commit()
    res1 = cur.fetchall()
    return render_template("/blue-master/editnews.html",id=id,name=name,data=res,data1=res1)
# 修改新闻详情页
@app.route("/editnews",methods=['post'])
def editnews():
    id = request.form['id']
    print(id)
    name = request.form['title']
    con=request.form['content']
    cid=request.form['cid']
    print(cid)
    sql = "update news set name='%s',con='%s',cid=%s where id=%s" % (name,con,cid,id)
    print(sql)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openeditnews%s_%s"%(id,name), time=3))
# 打开添加新闻关键字
@app.route("/openaddkeywords")
def openaddkeywords():
    sql = "select id,name from keywords  "
    cur.execute(sql)
    res = cur.fetchall()
    return render_template("/blue-master/addkeywords.html",data=res)
# 添加新闻关键字
@app.route("/addkeywords",methods=['post'])
def addkeywords():
    name=request.form['name']
    sql="insert into keywords (name) values ('%s')"%name
    cur.execute(sql)
    db.commit()
    sql="select id from keywords where name='%s'"%name
    cur.execute(sql)
    id=cur.fetchone()[0]
    rep={'info':'ok','id':id}
    print(rep)
    return jsonify(rep)

# 判断添加关键字不重复
@app.route("/selectkeywords",methods=['post'])
def selectkeywords():
    name = request.form['name']
    sql="select count(*) from keywords where name='%s'"%name
    cur.execute(sql)
    length = cur.fetchone()[0]
    print(length)
    if length>0:
        return "no"
    else:
        return "yes"
# 删除新闻关键字
@app.route("/delkeywords",methods=['post'])
def delkeywords():
    id = request.form['id']
    print(id)
    sql="delete from keywords where id='%s'"%id
    cur.execute(sql)
    db.commit()
    return "ok"

# 打开修改页面
@app.route("/openeditkeywords<id>_<name>")
def openeditkeywords(id,name):
    return render_template("/blue-master/editkeywords.html",id=id,name=name)
# 修改新闻关键字
@app.route("/editkeywords",methods=['post'])
def editkeywords():
    id=request.form['id']
    name=request.form['name']
    newname = request.form['newname']
    sql = "update keywords set name='%s' where name='%s'" % (newname,name)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("tips", state="yes", href="openaddkeywords", time=3))
# 注册用户列表
# @app.route("/listusers<page>")
# def listusers(page):
#     page = int(page)
#     sql = "select count(*) from users"
#     cur.execute(sql)
#     length = cur.fetchone()[0]
#     sql = "select * from users by users.id desc limit %s,2" % ((page - 1) * 2)
#     cur.execute(sql)
#     res = cur.fetchall()
#     pages = range(1, math.ceil(length / 2) + 1)
#     return render_template("/blue-master/listusers.html",data=res, pages=pages, now=page)
@app.route("/listusers")
def listusers():
    sql = "select * from users"
    cur.execute(sql)
    res = cur.fetchall()
    return render_template("/blue-master/listusers.html",data=res)





def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))
@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(app.static_folder, 'upload', rnd_name)

        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response

if __name__ == '__main__':
        app.run(debug=True)
