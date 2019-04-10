from math import *

mu_e_bohr_magneton = 9.274009994E-24  # J/T https://en.wikipedia.org/wiki/Bohr_magneton
mu_e_bohr_magneton_AU = 3.6E-3
h_plank_constant = 6.626070040E-34  # J.s
hbar = h_plank_constant / (2 * pi)  # J.s/rad
c_light_speed = 299792458
kB_boltzmann_constant = 1.3806488E-23  # J/K
mu_0_vacuum_permeability = 4 * pi * 1e-7  # T^2·m^3/J (H/m):vacuum permeability/magnetic constant N/A^2
mu_0_by_4pi = 1e-7
ge_neg = -2.00231930436182
ge = 2.00231930436182
a0_bohr_radius = 0.529177249E-10
mu_n_nuclear_magneton = 5.050783699E-27  # J/T https://en.wikipedia.org/wiki/Nuclear_magneton
Qe_electron_charge = 1.6021766208E-19  # C
factor_Dip2FC = 8 * pi / 3
gH = +5.585694702  # g_factor for nuclus H
kB = kB_boltzmann_constant
a0 = a0_bohr_radius
h = h_plank_constant  # J.s
Mu_e = mu_e_bohr_magneton  # J/T https://en.wikipedia.org/wiki/Bohr_magneton
Mu_n = mu_n_nuclear_magneton  # J/T https://en.wikipedia.org/wiki/Nuclear_magneton
mu0 = mu_0_vacuum_permeability


def AfcMHz2Rho(mhz, gn, S=1 / 2):
    f3 = AfcFactor_Rho2MHz(gn)
    rho = (mhz * 2 * S) / f3
    return rho


def AfcFactor_Rho2MHz(gn):
    f = mu_0_by_4pi * Mu_n / (a0 * a0 * a0)
    # GammaE=28024953.64  #Gamma_e/2*Pi
    GammaE = ge * Mu_e / h
    f2 = f * GammaE * 1e-6
    f3 = 8 * pi / 3 * f2 * gn
    return f3


def AfcRho2ppm(S, T, T0, rho):
    f = AfcFactorRho2ppm()
    y = f * rho * (S + 1) / (T - T0)
    return y


def AfcFactorRho2ppm():
    f = mu0 * Mu_e * Mu_e * ge * ge / (a0 * a0 * a0) / (9 * kB)
    f = f * 1e6
    return f


def Mhz2ppm(mhz, S, gn, T=330, T0=-34):
    return AfcRho2ppm(S=S, rho=AfcMHz2Rho(mhz=mhz, gn=gn, S=S), T=T, T0=T0)


def QISHz(Cq_MHz, eta, I, m, n, v0_MHz):
    ### Cq, v0: MHz
    ### Please add this QIS to Delta_iso
    Cq = Cq_MHz * 1e6
    v0 = v0_MHz * 1e6
    y = pow(3. * Cq / (2. * I * (2. * I - 1)), 2) * 56. / (5040. * v0) * (3. + eta * eta) * (
            m * (I * (I + 1.) - 3. * m * m) - n * (I * (I + 1.) - 3. * n * n))
    return y


def QISppm(Cq_MHz, eta, I, m, n, v0_MHz):
    ### Cq, v0: MHz
    y = QISHz(Cq_MHz=Cq_MHz, eta=eta, I=I, m=m, n=n, v0_MHz=v0_MHz)
    # y=y/(v0_MHz*1e6)*1e6
    y = y / v0_MHz
    return -y


if __name__ == '__main__':
    from vasptool import OUTCAR
    from vasptool import POSCAR
    import numpy
    import os

    # Constants
    gn_d = {'Li': 0.8219, 'O': 0.757, 'Mn': 1}
    S_d = {'Li': 1.5, 'O': 1.5, 'Mn': 1.5}
    I = {'Li': 1, 'O': 2.5, 'Mn': 1}
    m = {'Li': 1, 'O': 0.5, 'Mn': 1}
    n = {'Li': 0, 'O': -0.5, 'Mn': 1}
    v0 = {'Li': 29.47, 'O': 67.552, 'Mn': 1}
    T = {'Li': 323, 'O': 340, 'Mn': 330}
    N = 4
    ligt = numpy.mat([[1.93144358e+00, 1.00220000e-04, -5.94090000e-04],
                      [-7.63500000e-05, 1.93384854e+00, -5.98200000e-05],
                      [1.95329000e-03, -6.91010000e-04, 1.92834891e+00]], dtype='float64')


    def get_gtensor() -> numpy.mat:
        if os.path.exists('gtensor.csv'):
            temp = numpy.mat(numpy.loadtxt('gtensor.csv', dtype='float64', delimiter=','))
            return temp / 1e6 + 2 * numpy.identity(3)
        else:
            return ligt


    def Li2CO3_exp(ind):
        if ind <= 12:
            return 0  # Li
        else:
            return 163.35  # O


    def Li2CO3_cal(ind):
        if ind >= 13:
            return 198.1917
        elif ind <= 8:
            return -82.3329
        else:
            return 0


    def Li2MnO3_exp(ind):
        if ind >= 21:
            return 1859
        elif ind <= 4:
            return 734
        elif 5 <= ind <= 6:
            return 1461
        elif 7 <= ind <= 8:
            return 755
        else:
            return 2231


    def main(name):
        # Calculation
        outcar = OUTCAR()
        poscar = POSCAR()
        adp = outcar.get_Adp()
        afc = outcar.get_Afc()
        a1c = outcar.get_A1c()
        quad = outcar.get_quad()
        magnet = outcar.get_magnetization()
        gtensor = get_gtensor()
        g_iso = numpy.trace(gtensor) / 3 - ge
        cssum, csfc, csdp, csfc_t, csfc_exp, cs_plus_1c, qis = [], [], [], [], [], [], []

        for i in range(len(adp)):  # Calculation
            ele = poscar.get_element(ind=i + 1)
            # S = float(input('S for atom %s%s: ' % (str(i+1), ele)))
            csfc.append(N * Mhz2ppm(mhz=afc[i + 1], S=S_d[ele], gn=gn_d[ele], T=T[ele]))  # ge
            qis.append(QISppm(Cq_MHz=quad[i + 1]['cq'], eta=quad[i + 1]['eta'], I=I[ele], m=m[ele], n=n[ele],
                              v0_MHz=v0[ele]))
            csdp.append(N * Mhz2ppm(mhz=numpy.trace((adp[i + 1] * gtensor) * gtensor) / (3 * ge), S=S_d[ele],
                                    gn=gn_d[ele]))  # A_dp

            csfc_t.append(csfc[-1] + g_iso * csfc[-1] / ge)
            cssum.append(csfc[-1] + csdp[-1] + outcar.get_CSA_valence()[i + 1] + g_iso * csfc[-1] / ge + qis[-1])

            csfc_exp.append((Li2MnO3_exp(i + 1) - Li2CO3_exp(i + 1)) - (outcar.get_CSA_valence()[i + 1]
                                                                        - Li2CO3_cal(i + 1)) - csdp[-1] - qis[-1])

            cs_plus_1c.append(N * Mhz2ppm(S=S_d[ele], mhz=a1c[i + 1] + afc[i + 1], gn=gn_d[ele]))

        # Write file
        with open('../cs.csv', 'a') as f:
            f.write(
                f'{name}\nindex,element,magnetization (x),CSA,Afc(MHz),CQ(MHz),eta,Afc(ppm),Adp(ppm),Sum,Afc_tot(ppm),'
                f'Afc_exp,Atot+A1c(fc)\n')
        for i in range(len(adp)):
            try:
                t = f'{(i + 1)},{poscar.get_element(ind=i + 1)},{magnet[i + 1]},{outcar.get_CSA_valence()[i + 1]},' \
                    f'{afc[i + 1]},{quad[i + 1]["cq"]},{quad[i + 1]["eta"]},{csfc[i]},{csdp[i]},{cssum[i]},' \
                    f'{csfc_t[i]},{csfc_exp[i]},{cs_plus_1c[i]}\n'
            except Exception as err:
                if err.args[0] != 'magnetization (x) not found in OUTCAR.':
                    raise
                else:
                    t = f'{(i + 1)},{poscar.get_element(ind=i + 1)},{"N.A."},{outcar.get_CSA_valence()[i + 1]},' \
                        f'{afc[i + 1]},{quad[i + 1]["cq"]},{quad[i + 1]["eta"]},{csfc[i]},{csdp[i]},{cssum[i]},' \
                        f'{csfc_t[i]},{csfc_exp[i]},{cs_plus_1c[i]}\n'
            with open('../cs.csv', 'a') as f:
                f.write(t)


    for d in os.listdir(os.getcwd()):
        if os.path.isdir(d) and 'OUTCAR' in os.listdir(d):
            os.chdir(d)
            main(d)
            os.chdir('..')
