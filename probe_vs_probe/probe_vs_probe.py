import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates
import scipy.ndimage as ndim
import pandas as pd

title = 'Air temperature compare'  # Атмосферное давление Температура окружающего воздуха Относительная влажность воздуха
label_x = 'Date, dd.mm'
label_y = 'Temperature, ℃'  # Температура, ℃ Давление, мм.рт.ст. Влажность, %ОВ
legend_pos = 'upper left'  # lower left upper right
legend_1 = 'Cold subtropics (№3)'
legend_2 = 'Warm subtropics (№4)'
legend_3 = 'Succulents (№7)'
legend_4 = 'notfound'
filename_png = 'temp_bmp(3)_vs_temp_bmp(4)_vstemp_bmp(7)'  # temp_bmp(14)_vs_RP5 press_bmp(14)_vs_RP5
filename_csv_1 = 'probe3.csv'
filename_csv_2 = 'probe4.csv'
filename_csv_3 = 'probe7.csv'
filename_csv_4 = 'notfound.csv'
sensor_name = 'temp_bmp'  # temp_bmp press_bmp hum_htu
sensor_name_1 = sensor_name  # temp_bmp press_bmp hum_htu
up_limit = 30
down_limit = -30
up_x_axis_limit = 19097  # кол-во дней с 01.01.1970
down_x_axis_limit = 18949
up_y_axis_limit = 30
down_y_axis_limit = 0
gauss_sigma = 5

temp_bmp_14 = []
temp_bmp_7 = []
temp_bmp_filtered = []
temp_bmp_4 = []
time_probe_bmp_4 = []
temp_htu = []
temp_rtc = []
temp_ds = []
time_probe = []
time_probe_bmp_14 = []
time_probe_bmp_7 = []
time_probe_bmp_filtered = []
time_probebmp_rp5 = []
temp_rp5 = []
temp_rp5_filtered = []
time_rp5 = []
time_rp5_filtered = []
temp_bmp_11 = []
time_probe_bmp_11 = []
time_probe_ds_14 = []
time_probe_rtc_14 = []
time_probe_htu_14 = []


# зонд 1
probe_data_14 = pd.read_csv(filename_csv_1, sep='\t', decimal=',')
data_bmp_14 = probe_data_14.loc[(probe_data_14[sensor_name] < up_limit) & (probe_data_14[sensor_name] > down_limit)]
data_bmp_14.reset_index(drop=True)
data_bmp_14.to_excel('data_filtered.xlsx', sheet_name=sensor_name, index=False)
data_bmp_14 = pd.read_excel('data_filtered.xlsx')

for i in range(data_bmp_14.shape[0] - 1):
    temp_bmp_14.append(0)
    time_probe_bmp_14.append(0)
    temp_bmp_14[i] = data_bmp_14[sensor_name][i]  # записываем температуру
    time_probe_bmp_14[i] = datetime.datetime.strptime(str(data_bmp_14['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S')

# зонд 2
probe_data_11 = pd.read_csv(filename_csv_2, sep='\t', decimal=',')
data_bmp_filtered_11 = probe_data_11.loc[(probe_data_11[sensor_name_1] < up_limit) & (probe_data_11[sensor_name_1] > down_limit)]
data_bmp_filtered_11.reset_index(drop=True)
data_bmp_filtered_11.to_excel('data_filtered_11.xlsx', sheet_name=sensor_name_1, index=False)
data_bmp_filtered_11 = pd.read_excel('data_filtered_11.xlsx')

for i in range(data_bmp_filtered_11.shape[0] - 1):
    temp_bmp_11.append(0)
    time_probe_bmp_11.append(0)
    temp_bmp_11[i] = data_bmp_filtered_11[sensor_name_1][i]  # записываем температуру
    time_probe_bmp_11[i] = datetime.datetime.strptime(str(data_bmp_filtered_11['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S')

# зонд 3
probe_data_7 = pd.read_csv(filename_csv_3, sep='\t', decimal=',')
data_bmp_filtered_7 = probe_data_7.loc[(probe_data_7[sensor_name_1] < up_limit) & (probe_data_7[sensor_name_1] > down_limit)]
data_bmp_filtered_7.reset_index(drop=True)
data_bmp_filtered_7.to_excel('data_filtered_7.xlsx', sheet_name=sensor_name_1, index=False)
data_bmp_filtered_7 = pd.read_excel('data_filtered_7.xlsx')

for i in range(data_bmp_filtered_7.shape[0] - 1):
    temp_bmp_7.append(0)
    time_probe_bmp_7.append(0)
    temp_bmp_7[i] = data_bmp_filtered_7[sensor_name_1][i]  # записываем температуру
    time_probe_bmp_7[i] = datetime.datetime.strptime(str(data_bmp_filtered_7['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S')

# # зонд 4
# probe_data_4 = pd.read_csv(filename_csv_4, sep='\t', decimal=',')
# data_bmp_filtered_4 = probe_data_4.loc[(probe_data_4[sensor_name_1] < up_limit) & (probe_data_4[sensor_name_1] > down_limit)]
# data_bmp_filtered_4.reset_index(drop=True)
# data_bmp_filtered_4.to_excel('data_filtered_4.xlsx', sheet_name=sensor_name_1, index=False)
# data_bmp_filtered_4 = pd.read_excel('data_filtered_4.xlsx')
#
# for i in range(data_bmp_filtered_4.shape[0] - 1):
#     temp_bmp_4.append(0)
#     time_probe_bmp_4.append(0)
#     temp_bmp_4[i] = data_bmp_filtered_4[sensor_name_1][i]  # записываем температуру
#     time_probe_bmp_4[i] = datetime.datetime.strptime(str(data_bmp_filtered_4['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S')

# рисунок поверх графика на котором отрисовываются прочие элементы
fig = plt.figure()
ax = fig.add_subplot(111)

#подись заголовка и осей
plt.title(title, {'fontname':'Times New Roman'}, fontsize=18, pad=12.0)
plt.xlabel(label_x, {'fontname':'Times New Roman'}, fontsize=16, labelpad=10)
plt.ylabel(label_y, {'fontname':'Times New Roman'}, fontsize=16, labelpad=5)
plt.grid(True)

#гауссовый фильтр + построение первого графика
X = ndim.gaussian_filter(temp_bmp_14, sigma=gauss_sigma, order=0)
plt.plot_date(time_probe_bmp_14, X, 'b-', xdate=True)

#гауссовый фильтр + построение второго графика
X = ndim.gaussian_filter(temp_bmp_11, sigma=gauss_sigma, order=0)
plt.plot_date(time_probe_bmp_11, X, 'r-')
#
#гауссовый фильтр + построение третьего графика
X = ndim.gaussian_filter(temp_bmp_7, sigma=gauss_sigma, order=0)
plt.plot_date(time_probe_bmp_7, X, 'g-')
#
# #гауссовый фильтр + построение третьего графика
# X = ndim.gaussian_filter(temp_bmp_4, sigma=gauss_sigma, order=0)
# plt.plot_date(time_probe_bmp_4, X, 'y-')

#задаем границы осей
plt.axis([down_x_axis_limit, up_x_axis_limit, down_y_axis_limit, up_y_axis_limit])
plt.rc('font', family='Times New Roman')  # шрифт легенды
legend = plt.legend([legend_1, legend_2, legend_3], loc=legend_pos, fontsize=12)  # отображение легенды

# установка формата отображения даты и времени
plt.gcf().autofmt_xdate()
myFmt = matplotlib.dates.DateFormatter('%d.%m')
plt.gca().xaxis.set_major_formatter(myFmt)

# подписи оси Х устанавливаем по центру делений, угол поворота надписей = 0 град, установка шрифта и размера
xticks = ax.get_xticks()
ax.set_xticklabels(xticks, ha='center')
myFmt = matplotlib.dates.DateFormatter('%d.%m')
plt.gca().xaxis.set_major_formatter(myFmt)
plt.tick_params('x', labelrotation=45.0)
for tick in ax.get_xticklabels():
    tick.set_fontname("Times New Roman")
    tick.set_fontsize(14)
for tick in ax.get_yticklabels():
    tick.set_fontname("Times New Roman")
    tick.set_fontsize(14)

# сохраняем график и отображаем его
plt.savefig(filename_png, bbox_inches='tight')
plt.show()

