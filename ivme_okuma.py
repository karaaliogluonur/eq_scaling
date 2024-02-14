import os
import matplotlib.pyplot as plt
import numpy as np
import eqsig

from scipy.integrate import cumtrapz


# %%
os_path_dirname = os.path.dirname(__file__)

class GroundMotion:
    
    def __init__(self, filename):
        self.filename = filename
        
    def open_file(self, custom_file_path=None):
        if custom_file_path is None:
            self.fname = os.path.join(os_path_dirname, self.filename)
        else:
            self.fname = os.path.join(custom_file_path, self.filename)
        # Load the AT2 timeseries
        
        with open(self.fname) as fp:
            for _ in range(3):
                next(fp)
            line = next(fp)
            self.dt = float(line[17:25])
            self.accels = np.array([p for l in fp for p in l.split()]).astype(float)
            
        self.time = np.around(np.arange(0,len(self.accels))*self.dt,3)
        
        self.eq_info = open(self.fname,'r').readlines()[1]
        
        self.record = eqsig.single.AccSignal(self.accels*9.80665,self.dt)
            
        
        return self.fname, self.dt, self.accels, self.time, self.eq_info, self.record
    
    
    def get_accels(self):
        return self.accels
    
    def get_timeseries(self):
        return self.time
    
    def get_eqinfo(self):
        return self.eq_info
    
    def PGA(self):
        self.PGA_ = max(abs(min(self.accels)),max(self.accels))
        return self.PGA_
    
    def PGV(self):
        self.PGV_ = self.record.pgv
        return self.PGV_
    
    def PGD(self):
        self.PGD_ = self.record.pgd
        return self.PGD_
    
    def velocity(self):
        self.velocity_ = cumtrapz(self.accels*9.80665, dx=self.dt, initial=0)
        return self.velocity_
    
    def displacement(self):    
        self.displacement_ = cumtrapz(self.velocity_, dx=self.dt, initial=0)
        return self.displacement_
    
    def plt_accels(self):
        plt.figure(figsize=(8,2))
        plt.plot(self.time, self.accels,"k")
        plt.grid(color="silver", axis="y")
        plt.xlabel('Time(s)')
        plt.ylabel('Acceleration(g)')
        plt.title(f'{self.eq_info}PGA : {round(self.PGA(),3)}g')
        plt.xlim(left=0, right=self.time[-1])
        plt.show()
        
    def plt_velocity(self):
        plt.figure(figsize=(8,2))
        plt.plot(self.time, self.velocity(),"k")
        plt.grid(color="silver", axis="y")
        plt.xlabel('Time(s)')
        plt.ylabel('Velocity(m/s)')
        plt.title(f'{self.eq_info}PGV : {round(self.PGV(),3)} m/s')
        plt.xlim(left=0, right=self.time[-1])
        plt.show()
    
    def plt_displacement(self):
        plt.figure(figsize=(8,2))
        plt.plot(self.time, self.displacement(),"k")
        plt.grid(color="silver", axis="y")
        plt.xlabel('Time(s)')
        plt.ylabel('Displacement(m)')
        plt.title(f'{self.eq_info}PGD : {round(self.PGD(),3)} m')
        plt.xlim(left=0, right=self.time[-1])
        plt.show()
    
    def gm_SA(self):
        # list of sdof's periods
        self.periods = np.arange(0.1,8.01,0.01).tolist()
        # generate response spectrum
        self.spectra = self.record.generate_response_spectrum(response_times=self.periods)
        # m/s^2 to g
        self.SA = (self.record.s_a/9.80665).tolist()
        
        # insert; time=0 --> Sa=PGA
        self.periods.insert(0,0)
        self.periods = (np.around(self.periods,2)).tolist()
        self.SA.insert(0,self.PGA()/9.80665)
        
        return self.periods, self.SA
    
    def plt_spectra(self):
        # Plot response spectrum
        plt.plot(self.gm_SA()[0], self.gm_SA()[1])
        plt.grid(color="silver", axis="y")
        plt.xlabel('Period(s)')
        plt.ylabel('Spectral Acceleration(g)')
        plt.title(f'{self.eq_info} Response Spectrum')
        plt.xlim(left=0,right=8)
        plt.ylim(bottom=0, top=3)
        
def create_eqdic(eq_list, eq_number):
    eq_dic = {}
    sayac=0
    for i in range(1,eq_number+1):
        for j in range(1,3):
            eq_dic[f'eq_{i}_{j}'] = GroundMotion(eq_list[sayac])
            sayac += 1
    return eq_dic
        
# %%
    
# example.plt_accels()
# example.plt_velocity()
# example.plt_displacement()

klasor_yolu = r"D:\insaat\2- GTU\TEZ\TEZ_nlth\olcekleme\depremler"
eq_list = os.listdir(klasor_yolu)

# if eq_list is not None:
#     for deprem in eq_list:
#         print(deprem)
#     print(len(eq_list))


# eq_number = 11

# plt.figure(figsize=(10,6))

# eq_dic = create_eqdic(eq_list, eq_number)
# for i in range(1, eq_number+1):
#     for j in range(1,3):
#         eq_dic[f'eq_{i}_{j}'].open_file()
#         eq_dic[f'eq_{i}_{j}'].plt_spectra()
    

# Ss = 1.68
# S1 = 0.63
# site_class = "ZB"
# r=1

# tbdy_1 = tbdy_spektrum.Tbdy_spektrum(Ss, S1, site_class, r)

# tbdy_1.plot()