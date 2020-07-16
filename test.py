import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["zhangfen"]
# Docs=mydb['userzhifu'].find().limit(10000)
# t=0
# tt=0
# allnum=0
# for doc in Docs:
#     flag=0
#     for zhifudata in doc['zhifudata']:
#         zhifudata['total_fee']=int(zhifudata['total_fee'])
#         if zhifudata['total_fee']>100:
#             print('                             ')
#             print(zhifudata)
#             allnum+=zhifudata['total_fee']
#             tt+=1
#             flag=1
#     if flag==1:
#         t+=1
# print(t)
# print(tt)
# print(allnum)