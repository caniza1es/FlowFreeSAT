import Logica

def FlowRead(MAP_FILE):
	MAP_FILE = open(MAP_FILE,"r")
	MAP_MATRIX = [j.strip() for j in MAP_FILE]
	MAP_FILE.close()
	return MAP_MATRIX

def defineMap(matriz):
    dic = {}
    dic_a = {
        'R' : 0,
        'G' : 1,
        'B' : 2,
        'O' : 3
    }
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] in ['R','G','B','O']:
                dic[(x,y)] = dic_a[matriz[y][x]]
    return dic

def topico(tsei,intdict):
    M = []
    for claus in tsei:
        cl = []
        for kkk in claus:
            kkk = intdict[kkk]
            cl.append(kkk)
        M.append(cl)
    return M

def resolver(formula):
    S = Logica.tseitin(formula)
    pycosatset = S
    count = 1
    intdict = {}
    dictint = {}
    for cl in S:
        for kk in cl:
            if "-" not in kk:
                if kk not in intdict.keys():
                    intdict[kk] = count
                    dictint[count] = kk
                    count+=1
            else:
                if kk[1] not in intdict.keys():
                    intdict[kk[1]] = count
                    dictint[count] = kk[1]
                    count+=1
                intdict[kk] = -1 * intdict[kk[1]]
    pycosatset = topico(pycosatset,intdict)
    import pycosat
    solution = pycosat.solve(pycosatset)
    II = {}
    for innt in solution:
        num = -1*innt if innt < 0 else innt
        boole = True if innt > 0 else False
        II[dictint[num]] = boole
    lis = []
    for k in II:
        if (ord(k) >= OenCasilla.rango[0]) and (ord(k) <= OenCasilla.rango[1]) and II[k]:
            lis.append(k)
    return lis



mapa = FlowRead(input("mapa: "))

Nx = len(mapa[0])
Ny = len(mapa)
Nc = 4
Nd = 4
X = list(range(Nx))
Y = list(range(Ny))
C = list(range(Nc))
D = list(range(Nd))

NColores = {
	'R' : 0,
	'G' : 1,
	'B' : 2,
	'O' : 3
}

Colores = {
    0 : 'R',
    1 : 'G',
    2 : 'B',
    3 : 'O' 
}

Direcciones = {
	0 : 't',
	1 : 'b',
	2 : 'l',
	3 : 'r',
}


direcciones_posibles = {
    (0,1) : 'tb',
    (0,2) : 'tl',
    (0,3) : 'tr',
    (1,2) : 'bl',
    (1,3) : 'br',
    (2,3) : 'lr'
}

OenCasilla = Logica.Descriptor([Nx,Ny,Nc,Nd])
pos_t = defineMap(mapa)


def regla_1():
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys():
                O_d = []
                for d in direcciones_posibles.keys():
                    pq = [Logica.Ytoria([OenCasilla.P([x,y,c,d[0]]),OenCasilla.P([x,y,c,d[1]])]) for c in C] 
                    pq = Logica.Otoria(pq)
                    O_d.append(pq)
                Y_xy.append(Logica.Otoria(O_d))
    return Logica.Ytoria(Y_xy)


def regla_2():
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t:
                O_c = []
                for c in C:
                    nq = [OenCasilla.P([x,y,nc,d]) for nc in C if nc != c for d in D]
                    q = [OenCasilla.P([x,y,c,d]) for d in D]
                    formula = "("+Logica.Otoria(q)+"Y-"+Logica.Otoria(nq)+")"
                    O_c.append(formula)
                Y_xy.append(Logica.Otoria(O_c))
    return Logica.Ytoria(Y_xy)

def vectort(T,vecino_escogido):
    if vecino_escogido[0] == T[0] + 1:
        return 2
    elif vecino_escogido[0] == T[0] - 1:
        return 3
    elif vecino_escogido[1] == T[1] + 1:
        return 0
    elif vecino_escogido[1] == T[1] - 1:
        return 1

def regla_3():
    Y_pos_t = []
    for T in pos_t.keys():
        vecinos = [(x,y) for x in X for y in Y if ((x,y) not in pos_t.keys()) and (((x+1==T[0] or x-1==T[0])and y==T[1]) or ((y+1==T[1] or y-1==T[1])and x==T[0]))]
        if len(vecinos) == 1:
            Y_pos_t.append(OenCasilla.P([vecinos[0][0],vecinos[0][1],pos_t[T],vectort(T,vecinos[0])]))
            continue
        O_par_t = []
        for vecino_escogido in vecinos:
            otros_vecinos = [i for i in vecinos if i!=vecino_escogido]
            vtp = OenCasilla.P([vecino_escogido[0],vecino_escogido[1],pos_t[T],vectort(T,vecino_escogido)])
            ovtotal = []
            for ov in otros_vecinos:
                ovc = [OenCasilla.P([ov[0],ov[1],pos_t[T],dd]) for dd in D]
                ovtotal.append(Logica.Otoria(ovc))
            formula = "("+vtp+"Y-"+Logica.Otoria(ovtotal)+")"
            O_par_t.append(formula)
        Y_pos_t.append(Logica.Otoria(O_par_t))
    return Logica.Ytoria(Y_pos_t)

def coors(x,y):
    return -200+(x*100),200-(y*100)

def visualizar(I):
    import turtle
    FlowWindow = turtle.Screen()
    FlowWindow.setup(500,500)
    FlowWindow.title("FlowFree")
    FlowWindow.tracer(0)
    FlowWindow.addshape('img/0.gif')
    FlowWindow.addshape('img/1.gif')
    FlowWindow.addshape('img/2.gif')
    FlowWindow.addshape('img/3.gif')
    for d in D:
        for c in C:
            FlowWindow.addshape('img/{0}{1}.gif'.format(d,c))
    cell = turtle.Turtle()
    cell.pu()
    cell.ht()
    for t in pos_t.keys():
        cell.setpos(coors(t[0],t[1]))
        cell.shape('img/{}.gif'.format(pos_t[t]))
        cell.stamp()
    for valor in I:
        corx,cory,color,dirr = OenCasilla.inv(valor)
        cell.setpos(coors(corx,cory))
        cell.shape('img/{0}{1}.gif'.format(dirr,color))
        cell.stamp()
    FlowWindow.exitonclick()


M = resolver(Logica.Ytoria([regla_1(),regla_2(),regla_3()]))
visualizar(M)
