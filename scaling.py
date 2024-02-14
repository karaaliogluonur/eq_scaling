import os
import tbdy_spektrum
import ivme_okuma
import matplotlib.pyplot as plt
import numpy as np

class Scaling():
    
    
    def eq_srss(eq_x_SA, eq_y_SA):
        eq_resultant = (np.sqrt(np.square(eq_x_SA) + np.square(eq_y_SA))).tolist()
        return eq_resultant
    
    # def mean_srss():
        
        
    def plt_srss(periods, eq_srss_SA):
        # Plot response spectrum
        plt.plot(periods, eq_srss_SA)
        plt.grid(color="silver", axis="x")
        plt.xlabel('Period(s)')
        plt.ylabel('Spectral Acceleration(g)')
        #plt.title('Response Spectrum')
        plt.xlim(left=0,right=8)
        plt.ylim(bottom=0)
        
    def plt_srss_mean(periods, eq_mean):
        # Plot response spectrum
        plt.plot(periods, eq_mean,label="Mean SRSS", linewidth = 3, color = "red", ls="--")
        plt.grid(color="silver", axis="x")
        plt.xlabel('Period(s)')
        plt.ylabel('Spectral Acceleration(g)')
        #plt.title('Response Spectrums')
        plt.xlim(left=0,right=8)
        plt.ylim(bottom=0)
    
    def plt_srss_mean_scaled(periods, eq_mean, scale_f):
        # Plot response spectrum
        plt.plot(periods, scale_f*np.array(eq_mean),label="Scaled SRSS", linewidth = 5, color = "k", ls="-")
        plt.grid(color="silver", axis="x")
        plt.xlabel('Period(s)')
        plt.ylabel('Spectral Acceleration(g)')
        #plt.title('Response Spectrum')
        plt.xlim(left=0,right=8)
        plt.ylim(bottom=0)
    
    def scale_factor(periods, Sr, St, Tp):
        SF=0.5
        for t in periods:
            if ((t >= 0.2*Tp) and t <= 1.5*Tp):
                    while (SF*Sr[periods.index(t)]) <= St[periods.index(t)]:
                        SF += 0.01
        return SF


eq_list = ivme_okuma.eq_list

eq_number = 11

plt.figure(figsize=(10,6))

klasor_yolu = r"D:\insaat\2- GTU\TEZ\TEZ_nlth\olcekleme\depremler"
eq_dic = ivme_okuma.create_eqdic(eq_list, eq_number)
for i in range(1, eq_number+1):
    for j in range(1,3):
        eq_dic[f'eq_{i}_{j}'].open_file(klasor_yolu)

Ss = 1.151
S1 = 0.395
site_class = "ZC"
r = 1.3 # 1.3*Sae
Tp = 2.479

tbdy_1 = tbdy_spektrum.Tbdy_spektrum(Ss, S1, site_class, r)



eq_resultant_dic = {}
for i in range(1, eq_number+1):
    eq_resultant_dic[f'eq_{i}_SA'] = Scaling.eq_srss(eq_dic[f'eq_{i}_1'].gm_SA()[1], eq_dic[f'eq_{i}_2'].gm_SA()[1])
    #Scaling.plt_srss(eq_dic[f'eq_{i}_1'].gm_SA()[0], eq_resultant_dic[f'eq_{i}_SA'])

eq_mean = []

for index in range(len(eq_resultant_dic['eq_1_SA'])):
    sa_toplam = 0
    for j in range(1, eq_number+1):
        sa_toplam += eq_resultant_dic[f'eq_{j}_SA'][index]
    sa_mean = sa_toplam / eq_number
    eq_mean.append(sa_mean)

#Scaling.plt_srss_mean(eq_dic['eq_1_1'].gm_SA()[0], eq_mean)


# BURASI HER DEPREM İÇİN AYRI BULUR
for i in range(1, eq_number+1):
    plt.figure(figsize=(10,6))
    eq_info = eq_dic[f"eq_{i}_1"].eq_info.split(",")
    # scale_f = Scaling.scale_factor(eq_dic[f'eq_{i}_1'].gm_SA()[0], eq_resultant_dic[f'eq_{i}_SA'], tbdy_1.Sae_()[1], Tp)
    # print(f"eq_{i} Scale Factor: {scale_f}")
    plt.plot(eq_dic[f'eq_{i}_1'].gm_SA()[0], eq_dic[f'eq_{i}_1'].gm_SA()[1], label="direction-1",color="green")
    plt.plot(eq_dic[f'eq_{i}_1'].gm_SA()[0], eq_dic[f'eq_{i}_2'].gm_SA()[1], label="direction-2",color="brown")
    plt.plot(eq_dic[f'eq_{i}_1'].gm_SA()[0], np.array(eq_resultant_dic[f'eq_{i}_SA']), label="SRSS",color="blue")
    # plt.plot(eq_dic[f'eq_{i}_1'].gm_SA()[0], scale_f*np.array(eq_resultant_dic[f'eq_{i}_SA']),label="Scaled SRSS",color="orange")
    # plt.title(eq_info[0] + ", " + eq_info[1] + ", " + eq_info[2] + f"\nSF = {round(scale_f,2)}", fontsize = 15)
    plt.title(eq_info[0] + ", " + eq_info[1] + ", " + eq_info[2], fontsize = 12)
    # plt.plot([0.2*Tp,0.2*Tp],[0,4], color="blue", ls="--", linewidth = 3)
    # plt.plot([1.5*Tp,1.5*Tp],[0,4], color="blue", ls="--", linewidth = 3)
    plt.grid()
    plt.xlabel("Periyot(s)")
    plt.ylabel("Sa(g)")
    plt.xlim(left=0, right=8)
    plt.ylim(bottom=0, top=(max(np.array(eq_resultant_dic[f'eq_{i}_SA']))+0.1))
    plt.legend()
    # tbdy_1.plot()
    plt.show()
    

# #BU KISIM TÜM DEPREMLER İÇİN TEK BULUR
# scale_f = Scaling.scale_factor(eq_dic['eq_1_1'].gm_SA()[0], eq_mean, tbdy_1.Sae_()[1], Tp)
# print(f"Scale Factor: {scale_f}")

# for i in range(1, eq_number+1):
#     eq_info = eq_dic[f"eq_{i}_1"].eq_info.split(",")
#     plt.plot(eq_dic[f'eq_{i}_1'].gm_SA()[0], np.array(eq_resultant_dic[f'eq_{i}_SA']), label=eq_info[2])
    
# Scaling.plt_srss_mean(eq_dic['eq_1_1'].gm_SA()[0], eq_mean)
# Scaling.plt_srss_mean_scaled(eq_dic['eq_1_1'].gm_SA()[0], eq_mean, scale_f)

# plt.plot([0.2*Tp,0.2*Tp],[0,4], color="blue", ls="--", linewidth = 3)
# plt.plot([1.5*Tp,1.5*Tp],[0,4], color="blue", ls="--", linewidth = 3)
# plt.title(f"Response Spectrums SF={round(scale_f,2)}, Tp={Tp}s")

# tbdy_1.plot()
plt.show()























