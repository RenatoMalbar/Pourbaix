import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

#VARIAVEIS ENTRADA
Conc_Fe3 = 1 #em M -> alterar para ppm
Conc_Fe2 = 1 #em M -> alterar para ppm

pH = 7 #pH do sistema
potencial = 0 #potencial redox do sistema

class equilibrio:
    def __init__(self, func, dependencia, limite_inf, limite_sup) -> None:
        self.func = func
        self.depend = dependencia
        self.limites = [limite_inf, limite_sup]


#*********** ÁGUA ******************
def h2o_o2(ph):
    return 1000*(1.223-0.0591*ph)

def h2o_h2(ph):
    return 1000*(-0.0591*ph)

#******************* FERRO ***************
#***** ferro (s) ******************

#Equilíbrio Fe(II) + 2e -> Fe(s)
def fe2_fe(atividade_fe, atividade_fe2, ph):
    return -440+(59.2/2)*np.log10(atividade_fe2)

#Equilíbrio Fe3O4 + 8H+ + 8e -> 3Fe(s) + 3H2O 
def fe3o4_fe(atividade_fe3o4, atividade_fe, ph):
    return 1000*(-0.085-0.0591*ph) 

#Equilíbrio 2Fe2O3 + 2H+ + 2e -> 2Fe3O4 + H2O
def fe2o2_fe3o4(atividade_fe3, atividade_fe2, ph):
    return 1000*(0.221-0.0591*ph)

#Equilíbrio  Fe3O4 + 8H+ + 2e -> 3Fe(II) + 4H2O
def fe2_fe3o4(atividade_fe3, atividade_fe2, ph):
    return 1000*(0.980 - 0.2364*ph - 0.0886*np.log10(atividade_fe2))

#Equilíbrio Fe2o3 + 6H+ + 2e -> 2Fe(II) + 3H2O
def fe2o3_fe2(atividade_fe3, atividade_fe2, ph):
    return(1000*(0.728 - 0.1773*ph - 0.0591*np.log10(atividade_fe2)))

#Equilíbrio 2Fe(III) + 3H2O -> Fe2O3 + 6H+
def fe3_fe2O3(atividade_fe3, atividade_fe2, E):
    return (-1.43+(2*(-np.log10(atividade_fe3))))/6

#Equilíbrio Fe(II) + H2O -> FeO + 2H+
def fe2_feO(atividade_fe3, atividade_fe2, E):
    return ((np.log10(atividade_fe2)-13.29)/(-2))

#Equilíbrio Fe(II) + 2H2O -> Fe(OH)2 + 2H+
def fe2_feoh(atividade_fe3, atividade_fe2, E):
    return (14-np.log10(((4.87*10**(-17))/atividade_fe2)**(1/2)))

#Equilíbrio Fe(III) + 1e -> Fe(II)
def fe3_fe2(atividade_fe3, atividade_fe2, ph):
    return (1000*(0.771 + 0.0591*np.log10(atividade_fe3/atividade_fe2)))

#encontrar inters de duas funções
def find_root_ph(x, func1, func2, atividade_red, atividade_oxi):
    return func1(atividade_red, atividade_oxi, x) - func2(atividade_red, atividade_oxi, x)

#lista de valores de pH
lista_ph = np.arange(-2.0, 16.5, 0.5)
lista_potencial = 1000*np.arange(-2.0, 2, 0.01)

#calculos
lista_atividades = [0, -2, -4, -6] #atividades testadas (10)^lista_atividades[i]

#ÁGUA
e_h20_o2 = []
e_h20_h2 = []
for ativ in lista_atividades:
    e_h20_o2.append([h2o_o2(ph) for ph in lista_ph])
    e_h20_h2.append([h2o_h2(ph) for ph in lista_ph])

#FERRO
#ferro 0
root = optimize.root(find_root_ph, 0, (fe2_fe, fe3o4_fe, 1, Conc_Fe2))
fe_intersec=(float(root.x))

#ferro 2
root = optimize.root(find_root_ph, 0, (fe2_fe3o4, fe2o2_fe3o4, 1, Conc_Fe2))
fe2_intersec=(float(root.x))
root = optimize.root(find_root_ph, 0, (fe2_fe3o4, fe3o4_fe, 1, Conc_Fe2))
fe2_intersec2=(float(root.x))
root = optimize.root(find_root_ph, 0, (fe2o3_fe2, fe2o2_fe3o4, 1, Conc_Fe2))
fe2_intersec3=(float(root.x))
root = optimize.root(find_root_ph, 0, (fe3_fe2O3, fe3_fe2, 1, Conc_Fe2))
fe3_intersec1=(float(root.x))

#traçar curvas
plt.figure(figsize=(9,7))
#Equilíbrio Fe(II) + 2e -> Fe(s)
plt.plot(np.arange(-2, fe_intersec, 0.0001), [fe2_fe(1,Conc_Fe2,ph) for ph in np.arange(-2, fe_intersec, 0.0001)], 'k-', linewidth=0.65)
#Equilíbrio Fe3O4 + 8H+ + 8e -> 3Fe(s) + 3H2O 
plt.plot(np.arange((fe_intersec), 16, 0.0001), fe3o4_fe(1,1, np.arange((fe_intersec), 16, 0.0001)), 'k-', linewidth=1.3)
#Equilíbrio 2Fe2O3 + 2H+ + 2e -> 2Fe3O4 + H2O
plt.plot(np.arange((fe2_intersec), 16, 0.0001), fe2o2_fe3o4(1,1, np.arange((fe2_intersec), 16, 0.0001)), 'k-', linewidth=1.3)
#Equilíbrio  Fe3O4 + 8H+ + 2e -> 3Fe(II) + 4H2O
lim = np.arange(fe2_intersec, fe2_intersec2, 0.0001)
plt.plot(lim, [fe2_fe3o4(1,Conc_Fe2,ph) for ph in lim], 'k-', linewidth=0.65 )
#Equilíbrio Fe2o3 + 6H+ + 2e -> 2Fe2 + 3H2O
lim = (fe3_fe2O3(Conc_Fe3,Conc_Fe2,1), fe2_intersec3)
plt.plot(lim, [fe2o3_fe2(1,Conc_Fe2,ph) for ph in lim], 'k-', linewidth=0.65)
#Equilíbrio 2Fe(III) + 3H2O -> Fe2O3 + 6H+
lim = (fe2o3_fe2(Conc_Fe3,Conc_Fe2,fe3_fe2O3(Conc_Fe3,Conc_Fe2,1)), 2000)
plt.plot([fe3_fe2O3(Conc_Fe3,Conc_Fe2,pot) for pot in lim], lim, 'k-', linewidth=0.65)
#Equilíbrio Fe(III) + 1e -> Fe(II)
lim = (-2, fe3_fe2O3(Conc_Fe3, Conc_Fe2, potencial))
plt.plot(lim, [fe3_fe2(Conc_Fe3,Conc_Fe2,ph) for ph in lim], 'k--', linewidth=0.65)

#ÁGUA
for i in range(0,len(lista_atividades)): 
    plt.plot(lista_ph, e_h20_o2[i], 'g:', alpha = 0.3, linewidth=0.75)
    plt.plot(lista_ph, e_h20_h2[i], 'g:', alpha = 0.3, linewidth=0.75)

plt.xlim(-2, 16)
plt.ylim(-2000, 2000)
plt.xlabel('pH')
plt.ylabel('E [mV]')


#Condições do sistema
plt.plot(pH, potencial, 'r.', markersize = 20)
plt.plot(pH, potencial, 'w.', markersize = 17)
plt.plot(pH, potencial, 'r.', markersize = 10)

#nomes das espécies
plt.annotate('Fe(s)', xy=(6, -1000),
                color='k', size='medium')

plt.annotate(' Magnetita (Fe3O4)', xy=(12, -750),
                color='k', size='small')

plt.annotate('Fe2O3', xy=(7, 250),
                color='k', size='small')

plt.annotate('Fe 2+', xy=(0, 100),
                color='k', size='small')

plt.annotate('Fe 3+', xy=(-1.5, 1300),
                color='k', size='small')

plt.tight_layout()
plt.show()