import matplotlib.pyplot as plt
import numpy as np

bar_width = 0.25
opacity = 0.8

runtime_min = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
runtime_avg = [1.0031779107546512, 1.000, 1.001102576161294, 1.0, 1.0, 1.0, 1.0083403841151323]
runtime_max = [1.020, 1.0, 1.009, 1.0, 1.0, 1.0, 1.029]

n_groups = 7

index = np.arange(n_groups)

rects1 = plt.bar(index, runtime_min, bar_width,
                 alpha=opacity,
                 # edgecolor='b',
                 color='dodgerblue',
                 label='min'
                 )

rects2 = plt.bar(index + bar_width, runtime_avg, bar_width,
                 alpha=opacity,
                 # edgecolor='b',
                 color='gold',
                 label='avg'
                 )

rects3 = plt.bar(index + bar_width * 2, runtime_max, bar_width,
                 alpha=opacity,
                 # edgecolor='b',
                 color='orangered',
                 label='max'
                 )

for rect, label in zip(rects1, runtime_min):
  height = rect.get_height()
  plt.text(rect.get_x() + rect.get_width()/2., height + 0.005, "%.3f" % label, ha='center', va='bottom', rotation = 90, fontsize = 15)

for rect, label in zip(rects2, runtime_avg):
  height = rect.get_height()
  plt.text(rect.get_x() + rect.get_width()/2., height + 0.005, "%.3f" % label, ha='center', va='bottom', rotation = 90, fontsize = 15)

for rect, label in zip(rects3, runtime_max):
  height = rect.get_height()
  plt.text(rect.get_x() + rect.get_width()/2., height + 0.005, "%.3f" % label, ha='center', va='bottom', rotation = 90, fontsize = 15)

plt.xticks(index + bar_width, ('traffic', "face", "tracker", "pose", "caption", "audio", "actdet"), fontsize=24)
# plt.yticks([50, 60, 70, 80, 90, 100], ('50', '60', '70', '80', '90', '100'), fontsize=24)
plt.yticks([0.9, 0.95, 1.00, 1.05], ("0.90", "0.95", "1.00", "1.05"), fontsize=24)
plt.legend(ncol = 4, fontsize=20)

plt.ylabel("Cost of Scrooge/Optimal (%)", fontsize=24)

axes = plt.gca()
axes.set_ylim([0.9, 1.08])

plt.subplots_adjust(top=0.96, bottom=0.10, left=0.16, right=0.98, hspace=0.25, wspace=0.3)

fig = plt.gcf()
fig.set_size_inches(15, 7)

plt.show()
# plt.savefig("figure/ablation_quantify_milp.pdf")
