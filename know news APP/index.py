from flask import Blueprint,render_template,request,jsonify
import pymysql
db = pymysql.connect("localhost","root","","news")
cur = db.cursor()

app1 = Blueprint("app1",__name__,template_folder="")

@app1.route("/")
def index():
    sql1 = "select * from category"
    cur.execute(sql1)
    category = cur.fetchall()
    sql2 = "select * from newcon"
    cur.execute(sql2)
    cons = cur.fetchall()
    arr1 = []
    # [[],[],[]]
    for new in cons:
        arr2 = []
        for i in range(8):
            if i!=6:
                arr2.append(new[i])
            else:
                arr2.append(new[i].split(","))

        arr2.append(len(arr2[6]))
        arr1.append(arr2)

    return render_template("templates/index/index.html",category=category,cons=arr1)

@app1.route("/xq<id>")
def xq(id):
    sql1 = "select * from newcon where id=%s"%id
    cur.execute(sql1)
    res = cur.fetchone()

    sql = "select group_concat(k_title) from news_keywords where n_id=%s"%id
    cur.execute(sql)

    # 不一定所有都有关键字
    arr0 = set(cur.fetchone()[0].split(","))

    sql = "select n_id,group_concat(k_title) from news_keywords group by n_id"
    cur.execute(sql)
    newskeywords = cur.fetchall()

    newskeywordsdict = {}

    for item in newskeywords:
        newskeywordsdict[item[0]] = set(item[1].split(","))
    print(newskeywordsdict)
    newskeywordsdictnum = {}
    for k,v in newskeywordsdict.items():
        newskeywordsdictnum[k] = len(v&arr0)

    newid = []

    for k,v in newskeywordsdictnum.items():
        if v>0 and k != int(id):
            newid.append(str(k))

    tuijian = ""
    if newid:
        sql2 = "select id,n_title from newcon where id in (%s)"%(",".join(newid))
        cur.execute(sql2)
        tuijian = cur.fetchall()

    return render_template("templates/index/xq.html",data = res,tuijian=tuijian,n_id=id)

@app1.route("/addComments",methods=['post'])
def addComments():
    con = request.form['con']
    n_id = request.form['n_id']
    u_id = request.form['u_id']

    sql = "insert into comments (con,n_id,u_id,u_name) values ('%s',%s,%s,'%s')"%(con,n_id,u_id,"horns")

    cur.execute(sql)
    db.commit()
    return "ok"

@app1.route("/listComments",methods=['post'])
def listComments():
    n_id = request.form['n_id']
    cur = db.cursor()
    sql = "select * from comments where n_id=%s"%n_id
    cur.execute(sql)
    res = cur.fetchall()
    data = {}
    cj = []
    for item in res:
        fun(cj,item[0],item[4])
        data[item[0]] = {'con':item[1],'u_name':item[3],'u_id':item[4]}

    # print(data)
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
