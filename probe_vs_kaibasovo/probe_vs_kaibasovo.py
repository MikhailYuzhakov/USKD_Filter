import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates
import scipy.ndimage as ndim
import pandas as pd

filename_csv_kaibasovo = 'kaibasovo1.csv'
filename_csv_probe_2 = 'probe2.csv'
filename_csv_probe_10 = 'probe10.csv'

sensor_name_kaibasovo = 'Snow profile, 500 mm (°C)'  # Snow profile, 500 mm (°C) Temperature probe, 0.0 m (°C) Atmospheric pressure (mmHg) Temperature probe, -0.7 m (°C)
sensor_name_probe_2 = 'temp_bmp'  # 10cm temp_bmp
sensor_name_probe_10 = 'temp_bmp'

title = 'Air temperature'  # Атмосферное давление Температура окружающего воздуха
label_x = 'Date, dd.mm'
label_y = 'Temperature, ℃'  # Температура, ℃ Давление, мм.рт.ст. Влажность, %ОВ
filename_png = 'temp_bmp(2)_vs_kaibasovo'
legend_pos = 'upper left'  # upper right
legend_1 = 'Probe №2'
legend_2 = 'Kaibasovo weather station'
legend_3 = 'Агрозонд №10'

up_limit = 30
down_limit = -30
gauss_sigma = 4
up_x_axis_limit = 19043  # кол-во дней с 01.01.1970 18939
down_x_axis_limit = 18951
up_y_axis_limit = 20
down_y_axis_limit = -30
factor = 1  # для перевода гПа в мм.рт.ст. 0.750062

time_kaibasovo = []
time_probe_2 = []
time_probe_10 = []
value_kaibasovo = []
value_probe_2 = []
value_probe_10 = []
time_match_probe_2 = []
time_match_probe_10 = []
value_probe_2_filtered = []
value_probe_10_filtered = []
value_kaibasovo_filtered = []
delta = []

# метеостанция в Кайбасово
data_kaibasovo = pd.read_csv(filename_csv_kaibasovo, sep=',', decimal='.')
data_target = data_kaibasovo.loc[(data_kaibasovo[sensor_name_kaibasovo] < up_limit) & (data_kaibasovo[sensor_name_kaibasovo] > down_limit)]
data_target.reset_index(drop=True)
data_target.to_excel('data_kaibasovo.xlsx', sheet_name='data', index=False)
data_target = pd.read_excel('data_kaibasovo.xlsx')

for i in range(data_target.shape[0] - 1):
    value_kaibasovo.append(0)
    time_kaibasovo.append(0)
    value_kaibasovo[i] = data_target[sensor_name_kaibasovo][i] * factor  # записываем данные из таблицы
    time_kaibasovo[i] = datetime.datetime.strptime(str(data_target['UTC'][i]), '%Y-%m-%d %H:%M:%S')

# Агрозонд №2
data_probe_2 = pd.read_csv(filename_csv_probe_2, sep='\t', decimal=',')
data_target_probe_2 = data_probe_2.loc[(data_probe_2[sensor_name_probe_2] < up_limit) & (data_probe_2[sensor_name_probe_2] > down_limit)]
data_target_probe_2.reset_index(drop=True)
data_target_probe_2.to_excel('data_filtered_p2.xlsx', sheet_name=sensor_name_probe_2, index=False)
data_target_probe_2 = pd.read_excel('data_filtered_p2.xlsx')

for i in range(data_target_probe_2.shape[0] - 1):
    value_probe_2.append(0)
    time_probe_2.append(0)
    value_probe_2[i] = data_target_probe_2[sensor_name_probe_2][i]  # записываем температуру
    time_probe_2[i] = datetime.datetime.strptime(str(data_target_probe_2['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S')

# Агрозонд №10
# data_probe_10 = pd.read_csv(filename_csv_probe_10, sep='\t', decimal=',')
# data_target_probe_10 = data_probe_10.loc[(data_probe_10[sensor_name_probe_10] < up_limit) & (data_probe_10[sensor_name_probe_10] > down_limit)]
# data_target_probe_10.reset_index(drop=True)
# data_target_probe_10.to_excel('data_filtered_p10.xlsx', sheet_name=sensor_name_probe_10, index=False)
# data_target_probe_10 = pd.read_excel('data_filtered_p10.xlsx')

# for i in range(data_target_probe_10.shape[0] - 1):
#     value_probe_10.append(0)
#     time_probe_10.append(0)
#     value_probe_10[i] = data_target_probe_10[sensor_name_probe_10][i]  # записываем температуру
#     time_probe_10[i] = datetime.datetime.strptime(str(data_target_probe_10['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S')

# строим сравнительный график только по тем точкам время в которых совпадает по дате и часам для №2
k = 0
for i in range(len(time_kaibasovo)):
    for j in range(len(time_probe_2)):
        if time_kaibasovo[i].date() == time_probe_2[j].date() and time_kaibasovo[i].hour == time_probe_2[j].hour:
            time_match_probe_2.append(0)
            value_probe_2_filtered.append(0)
            time_match_probe_2[k] = time_probe_2[j]
            value_probe_2_filtered[k] = value_probe_2[j]
            k += 1
            break

# строим сравнительный график только по тем точкам время в которых совпадает по дате и часам для №10
# k = 0
# for i in range(len(time_kaibasovo)):
#     for j in range(len(time_probe_10)):
#         if time_kaibasovo[i].date() == time_probe_10[j].date() and time_kaibasovo[i].hour == time_probe_10[j].hour:
#             time_match_probe_10.append(0)
#             value_probe_10_filtered.append(0)
#             value_kaibasovo_filtered.append(0)
#             time_match_probe_10[k] = time_probe_10[j]
#             value_probe_10_filtered[k] = value_probe_10[j]
#             value_kaibasovo_filtered[k] = value_kaibasovo[i]
#             k += 1
#             break

# находим максимальный элемент
# max_value = -1000
# for value in value_probe_10_filtered:
#     if value > max_value:
#         max_value = value

# нормируем
# for i in range(len(value_probe_10_filtered)):
#     value_probe_10_filtered[i] = value_probe_10_filtered[i] / max_value

# находим максимальный элемент
# min_value = 1000
# for value in value_kaibasovo_filtered:
#     if value < min_value:
#         min_value = value

# нормируем
# for i in range(len(value_kaibasovo_filtered)):
#     value_kaibasovo_filtered[i] = value_kaibasovo_filtered[i] / min_value

# считаем разность температур
# for i in range(len(value_kaibasovo_filtered)):
#     delta.append(0)
#     delta[i] = value_kaibasovo_filtered[i] - value_probe_10_filtered[i]

# рисунок поверх графика на котором отрисовываются прочие элементы
fig = plt.figure()
ax = fig.add_subplot(111)

# подись заголовка и осей
plt.title(title, {'fontname':'Times New Roman'}, fontsize=18, pad=12.0)
plt.xlabel(label_x, {'fontname':'Times New Roman'}, fontsize=16, labelpad=10)
plt.ylabel(label_y, {'fontname':'Times New Roman'}, fontsize=16, labelpad=5)
plt.grid(True)

# гауссовый фильтр + построение первого графика Кайбасово
X = ndim.gaussian_filter(value_kaibasovo, sigma=gauss_sigma, order=0)
plt.plot_date(time_kaibasovo, X, 'b-', xdate=True)

# гауссовый фильтр + построение второго графика зонд №2
X = ndim.gaussian_filter(value_probe_2_filtered, sigma=gauss_sigma, order=0)
plt.plot_date(time_match_probe_2, X, 'r-')

# гауссовый фильтр + построение второго графика зонд №10
# X = ndim.gaussian_filter(value_probe_10_filtered, sigma=gauss_sigma, order=0)
# plt.plot_date(time_match_probe_10, X, 'g-')

# разница температур
# X = ndim.gaussian_filter(delta, sigma=gauss_sigma, order=0)
# plt.plot_date(time_match_probe_10, X, 'k-')

# нормированные vacc и солнечная радиация
# X = ndim.gaussian_filter(value_probe_10_filtered, sigma=0, order=0)
# plt.plot_date(time_match_probe_10, X, 'b-')

# X = ndim.gaussian_filter(value_kaibasovo_filtered, sigma=2, order=0)
# plt.plot_date(time_match_probe_10, X, 'r-')

# задаем границы осей
plt.axis([down_x_axis_limit, up_x_axis_limit, down_y_axis_limit, up_y_axis_limit])
plt.rc('font', family='Times New Roman')  # шрифт легенды
legend = plt.legend([legend_2, legend_1], loc=legend_pos, fontsize=14)  # отображение легенды

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
plt.savefig(filename_png)
plt.show()
