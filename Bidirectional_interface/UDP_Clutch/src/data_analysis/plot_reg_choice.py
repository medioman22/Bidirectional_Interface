#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 23:16:00 2018

@author: matteomacchini
"""

res_mlp_1 = res_1[1:-9]
res_svr_1 = res_1[-9:]


m_perf_mlp_1 = mean([x['mse'] for x in res_mlp_1])

m_perf_svr_1 = mean([x['mse'] for x in res_svr_1])

m_fit_mlp_1 = mean([x['fit_time'] for x in res_mlp_1])

m_fit_svr_1 = mean([x['fit_time'] for x in res_svr_1])


res_mlp_3 = res_3[1:-9]
res_svr_3 = res_3[-9:]


m_perf_mlp_3 = mean([x['mse'] for x in res_mlp_3])

m_perf_svr_3 = mean([x['mse'] for x in res_svr_3])

m_fit_mlp_3 = mean([x['fit_time'] for x in res_mlp_3])

m_fit_svr_3 = mean([x['fit_time'] for x in res_svr_3])

res_mlp_6 = res_6[1:-9]
res_svr_6 = res_6[-9:]


m_perf_mlp_6 = mean([x['mse'] for x in res_mlp_6])

m_perf_svr_6 = mean([x['mse'] for x in res_svr_6])

m_fit_mlp_6 = mean([x['fit_time'] for x in res_mlp_6])

m_fit_svr_6 = mean([x['fit_time'] for x in res_svr_6])



matplotlib.rcParams.update({'font.size': 40})

#data = ((finals[1]), ((finals[2], finals[3])))


###

plt.figure()


plt.xlabel("")
plt.ylabel("MSE (normalized)")
plt.title("")
#plt.yscale('log')
plt.grid('on')

x = np.array([1, 2, 3])

y = [m_perf_mlp_1/m_perf_svr_1, m_perf_mlp_3/m_perf_svr_3, m_perf_mlp_6/m_perf_svr_6]
z= [m_perf_svr_1/m_perf_svr_1, m_perf_svr_3/m_perf_svr_3, m_perf_svr_6/m_perf_svr_6]

w = 0.3

ax = plt.subplot(111)
rect1 = ax.bar(x - w/2, z,width=w,color='g',align='center')
rect2 = ax.bar(x + w/2, y,width=w,color='r',align='center')

ax.legend((rect1[0], rect2[0]), ('SVR', 'MLP'))
plt.xticks((1, 2, 3), ('1 Dataset', '3 Datasets', '6 Datasets'))

plt.ylim((0, 1.5))

#def autolabel(rects):
#    for rect in rects:
#        h = rect.get_height()
#        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
#                ha='center', va='bottom')
#
#autolabel(rect1)
#autolabel(rect2)

plt.show()


###

plt.figure()

plt.xlabel("")
plt.ylabel("Fit Time [s]")
plt.title("")
#plt.yscale('log')
plt.grid('on')

x = np.array([1, 2, 3])

y = [m_fit_mlp_1, m_fit_mlp_3, m_fit_mlp_6]
z= [m_fit_svr_1, m_fit_svr_3, m_fit_svr_6]

w = 0.3

ax = plt.subplot(111)
rect1 = ax.bar(x - w/2, z,width=w,color='g',align='center')
rect2 = ax.bar(x + w/2, y,width=w,color='r',align='center')

ax.legend((rect1[0], rect2[0]), ('SVR', 'MLP'))
plt.xticks((1, 2, 3), ('1 Dataset', '3 Datasets', '6 Datasets'))

plt.ylim((1, 400))

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rect1)
autolabel(rect2)

plt.show()