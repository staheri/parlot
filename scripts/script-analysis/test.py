import numpy as np
#from basic_units import cm, inch
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


N = 5
menMeans = (150, 160, 146, 172, 155)
menStd = (20, 30, 32, 10, 20)

fig, ax = plt.subplots()

ind = np.arange(N)    # the x locations for the groups
width = 0.35         # the width of the bars
p1 = ax.bar(ind, menMeans, width, color='r', bottom=0, yerr=menStd)


womenMeans = (150, 160, 146, 172, 155)
womenStd = (20, 30, 32, 10, 20)
p2 = ax.bar(ind + width, womenMeans, width,
            color='y', bottom=0, yerr=womenStd)

ax.set_title('Scores by group and gender')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

ax.legend((p1[0], p2[0]), ('Men', 'Women'))

ax.autoscale_view()

#plt.show()
plt.savefig("test.png")
