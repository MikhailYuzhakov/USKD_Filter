import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates
import scipy.ndimage as ndim
import pandas as pd

title = 'Air humidity'  # Атмосферное давление Температура окружающего воздуха Относительная влажность воздуха Температура окружающего воздуха
label_x = 'Date, dd.mm.yy'
label_y = 'Relative humidity, %RH'  # Температура, ℃ Давление, мм.рт.ст. Влажность, %ОВ
legend_pos = 'lower right'  #
legend_1 = 'Probe №14'
legend_2 = 'Weather service RP5'
filename_png = 'hum_htu(14)_vs_RP5'  # temp_bmp(14)_vs_RP5 press_bmp(14)_vs_RP5
filename_csv = 'probe14.csv'
filename_xlsx = 'RP5_3.xlsx'
sensor_name = 'hum_htu'  # temp_bmp press_bmp
rp5_sensor_name = 'U'  # P U T
up_limit = 100
down_limit = 0
up_x_axis_limit = 19011  # кол-во дней с 01.01.1970
down_x_axis_limit = 18897
up_y_axis_limit = 100
down_y_axis_limit = 30
gauss_sigma = 4

temp_bmp = []
temp_bmp_filtered = []
temp_htu = []
temp_rtc = []
time_probe = []
time_probe_bmp = []
time_probe_bmp_filtered = []
time_probebmp_rp5 = []
temp_rp5 = []
temp_rp5_filtered = []
time_rp5 = []
time_rp5_filtered = []

probe_data = pd.read_csv(filename_csv, sep='\t', decimal=',')
data_bmp_filtred = probe_data.loc[(probe_data[sensor_name] < up_limit) & (probe_data[sensor_name] > down_limit)]
data_bmp_filtred.reset_index(drop=True)
data_bmp_filtred.to_excel('data_filtered.xlsx', sheet_name=sensor_name, index=False)
data_bmp_filtred = pd.read_excel('data_filtered.xlsx')

for i in range(data_bmp_filtred.shape[0] - 1):
    temp_bmp.append(0)
    time_probe_bmp.append(0)
    temp_bmp[i] = data_bmp_filtred[sensor_name][i]  # записываем температуру
    time_probe_bmp[i] = datetime.datetime.strptime(str(data_bmp_filtred['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S')

# for i in range(probe_data.shape[0]):
# temp_htu.append(0)
# temp_rtc.append(0)
# time_probe.append('0')
# temp_htu[i] = float(probe_data['temp_htu'][i])  # записываем температуру
# temp_rtc[i] = float(probe_data['temp_rtc'][i])  # записываем температуру
# time_probe[i] = datetime.datetime.strptime(str(probe_data['probe_timestamp'][i]), '%Y-%m-%d %H:%M:%S') #записываем дату

###############################Сервис погоды РП-5######################################################

weather_RP5 = pd.read_excel(filename_xlsx)
# print(weather_RP5)
# print(weather_RP5.dtypes) #тип данных в таблице
# print(weather_RP5.columns) #Нзвание столбцов
# print(weather_RP5.shape) #сколько строк и столбцов
# print(weather_RP5.describe()) #выводит статистику (макс, мин, ср)
# print(weather_RP5['T'][0]) #Т - столбик с температурой, 0 - индекс строки

for i in range(weather_RP5.shape[0]):
    temp_rp5.append(0)
    time_rp5.append('0')
    temp_rp5[i] = weather_RP5[rp5_sensor_name][weather_RP5.shape[0] - i - 1]  # записываем температуру по возврастанию даты
    time_rp5[i] = datetime.datetime.strptime(str(weather_RP5['Местное время в Томске'][i]),
                                             '%d.%m.%Y %H:%M')  # записываем дату
j = 0

time_rp5.sort()  # сортируем дату и время по возрастанию

# for i in range(len(time_probe_bmp)):
#     time_probe_bmp[i] = time_probe_bmp[i] - datetime.timedelta(hours=7)

#строим сравнительный график только по тем точкам время которых совпадает
k = 0
for i in range(len(time_rp5)):
    for j in range(len(time_probe_bmp)):
        if time_rp5[i].date() == time_probe_bmp[j].date() and time_rp5[i].hour == time_probe_bmp[j].hour:
            time_probe_bmp_filtered.append(0)
            time_rp5_filtered.append(0)
            temp_bmp_filtered.append(0)
            temp_rp5_filtered.append(0)
            time_probe_bmp_filtered[k] = time_probe_bmp[j]
            temp_bmp_filtered[k] = temp_bmp[j]
            temp_rp5_filtered[k] = temp_rp5[i]
            k += 1
            break
#рисунок поверх графика на котором отрисовываются прочие элементы
fig = plt.figure()
ax = fig.add_subplot(111)

#подись заголовка и осей
plt.title(title, {'fontname':'Times New Roman'}, fontsize=18, pad=12.0)
plt.xlabel(label_x, {'fontname':'Times New Roman'}, fontsize=16, labelpad=10)
plt.ylabel(label_y, {'fontname':'Times New Roman'}, fontsize=16, labelpad=5)
plt.grid(True)

#гауссовый фильтр + построение первого графика
X = ndim.gaussian_filter(temp_bmp_filtered, sigma=gauss_sigma, order=0)
plt.plot_date(time_probe_bmp_filtered, X, 'b-', xdate=True)

#гауссовый фильтр + построение второго графика
X = ndim.gaussian_filter(temp_rp5_filtered, sigma=gauss_sigma, order=0)
plt.plot_date(time_probe_bmp_filtered, X, 'r-')

#задаем границы осей
plt.axis([down_x_axis_limit, up_x_axis_limit, down_y_axis_limit, up_y_axis_limit])
plt.rc('font', family='Times New Roman')  # шрифт легенды
legend = plt.legend([legend_1, legend_2], loc=legend_pos, fontsize=14)  # отображение легенды

# установка формата отображения даты и времени
plt.gcf().autofmt_xdate()
myFmt = matplotlib.dates.DateFormatter('%d.%m.%y')
plt.gca().xaxis.set_major_formatter(myFmt)

# подписи оси Х устанавливаем по центру делений, угол поворота надписей = 0 град, установка шрифта и размера
xticks = ax.get_xticks()
ax.set_xticklabels(xticks, ha='center')
myFmt = matplotlib.dates.DateFormatter('%d.%m.%y')
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