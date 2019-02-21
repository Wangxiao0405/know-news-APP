# 数据处理为字典
res={
#     id：{con:sss,author:sa}


}
obj={}
for item in res :
    obj[item[0]]={'con':item[1]}

cj=[
    {1:[
        {3:[
            {4:[]}
        ]}
    ]},
    {2:[]}

]
res=(
    # id u_id
    (1,0),
    (2,0),
        (3,1),
    (4,3)

)

cj=[]
def fun(cj,id,u_id):
    if u_id==0:
        cj.append([id,[]])
        return
    for arr in cj:
        if arr[0]==u_id:
            arr[1].append([id,[]])
        else:
            fun(arr[1],id,u_id)

for id,u_id in res:
    fun(cj,id,u_id)

print(cj)