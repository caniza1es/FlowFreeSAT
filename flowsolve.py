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
        'O' : 3,
        'P' : 4
    }
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] in ['R','G','B','O','P']:
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
    if solution == "UNSAT":
        print(solution)
        return None
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
Nc = 5
Nd = 4
X = list(range(Nx))
Y = list(range(Ny))
C = list(range(Nc))
D = list(range(Nd))

NColores = {
	'R' : 0,
	'G' : 1,
	'B' : 2,
	'O' : 3,
        'P' : 4
}

Colores = {
    0 : 'R',
    1 : 'G',
    2 : 'B',
    3 : 'O',
    4 : 'P'
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

def regla_1():#asigna colores
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


def regla_2():
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys():
                O_d = []
                for d in direcciones_posibles.keys():
                    pq = [Logica.Ytoria([OenCasilla.P([x,y,c,d[0]]),OenCasilla.P([x,y,c,d[1]])]) for c in C]
                    npq = [Logica.Ytoria([OenCasilla.P([x,y,c,u[0]]),OenCasilla.P([x,y,c,u[1]])]) for c in C for u in direcciones_posibles.keys() if u!=d]
                    pq = "("+Logica.Otoria(pq)+"Y-"+Logica.Otoria(npq)+")"
                    O_d.append(pq)
                Y_xy.append(Logica.Otoria(O_d))
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

def regla_3():#asignaterminales
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
                ovc = [OenCasilla.P([ov[0],ov[1],c,vectort(T,(ov[0],ov[1]))])for c in C]
                ovtotal.append(Logica.Otoria(ovc))
            formula = "("+vtp+"Y-"+Logica.Otoria(ovtotal)+")"
            O_par_t.append(formula)
        Y_pos_t.append(Logica.Otoria(O_par_t))
    return Logica.Ytoria(Y_pos_t)

def vec(x, y, direccion):
    if 2 in direccion:
        if 3 in direccion:
            return (x-1, y)
        


#direccion 2-3
def regla_4():#asignaleft-right
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys() and (x!=0 and x!=Nx-1):
                O_c = []
                for c in C:
                    formula = "("+OenCasilla.P([x,y,c,2])+"Y"+OenCasilla.P([x,y,c,3])+")"
                    vecinos = []
                    if((x+1,y) in pos_t.keys()):
                        if ((x-1,y) in pos_t.keys()):
                            continue
                        else:
                            vecinos.append( OenCasilla.P([x - 1, y, pos_t[(x + 1, y)], 3]) )
                    elif ((x-1,y) in pos_t.keys()):
                        vecinos.append( OenCasilla.P([x + 1, y, pos_t[(x-1, y)], 2]) )
                    else:
                        vecinos.append( "("+OenCasilla.P([x + 1, y, c ,2]) + "Y" + OenCasilla.P([x - 1,y,c,3])+")")
                    opuestos_a = ["-"+OenCasilla.P([x,y+1,o,0]) for o in C if y+1 in Y]
                    opuestos_b = ["-"+OenCasilla.P([x,y-1,o,1]) for o in C if y-1 in Y]
                    total_op = Logica.Ytoria(vecinos + opuestos_a + opuestos_b)
                    formula_total = "("+formula+">"+total_op+")"
                    O_c.append(formula_total)
                if len(O_c) != 0:
                    Y_xy.append(Logica.Ytoria(O_c))
    return Logica.Ytoria(Y_xy)

def regla_5(): # Asignar top-right
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys() and (y!=0 and x!=Nx-1):
                O_c = []
                for c in C:
                    formula = "(" + OenCasilla.P([x, y, c, 0]) + "Y" + OenCasilla.P([x, y, c, 3]) + ")"
                    vecinos = []
                    if((x + 1, y) in pos_t.keys()):
                        if ((x, y - 1) in pos_t.keys()):
                            continue
                        else:
                            vecinos.append( OenCasilla.P([x, y - 1, pos_t[(x + 1, y)], 1]) )
                    elif ((x, y - 1) in pos_t.keys()):
                        vecinos.append( OenCasilla.P([x + 1, y, pos_t[(x, y - 1)], 2]) )
                    else:
                        vecinos.append( "(" + OenCasilla.P([x + 1, y, c , 2]) + "Y" + OenCasilla.P([x ,y - 1, c, 1]) + ")")
                    opuestos_a = ["-" + OenCasilla.P([x, y + 1, o, 0]) for o in C if y + 1 in Y]
                    opuestos_b = ["-" + OenCasilla.P([x - 1, y, o, 3]) for o in C if x - 1 in X]
                    total_op = Logica.Ytoria(vecinos + opuestos_a + opuestos_b)
                    formula_total = "(" + formula + ">" + total_op + ")"
                    O_c.append(formula_total)
                if len(O_c) != 0:
                    Y_xy.append(Logica.Ytoria(O_c))
    return Logica.Ytoria(Y_xy)

def regla_6(): # Asignar top-left
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys() and (y!=0 and x!=0):
                O_c = []
                for c in C:
                    formula = "(" + OenCasilla.P([x, y, c, 0]) + "Y" + OenCasilla.P([x, y, c, 2]) + ")"
                    vecinos = []
                    if((x - 1, y) in pos_t.keys()):
                        if ((x, y - 1) in pos_t.keys()):
                            continue
                        else:
                            vecinos.append( OenCasilla.P([x, y - 1, pos_t[(x - 1, y)], 1]) )
                    elif ((x, y - 1) in pos_t.keys()):
                        vecinos.append( OenCasilla.P([x - 1, y, pos_t[(x, y - 1)], 3]) )
                    else:
                        vecinos.append( "(" + OenCasilla.P([x - 1, y, c , 3]) + "Y" + OenCasilla.P([x ,y - 1, c, 1]) + ")")
                    opuestos_a = ["-" + OenCasilla.P([x, y + 1, o, 0]) for o in C if y + 1 in Y]
                    opuestos_b = ["-" + OenCasilla.P([x + 1, y, o, 2]) for o in C if x + 1 in X]
                    total_op = Logica.Ytoria(vecinos + opuestos_a + opuestos_b)
                    formula_total = "(" + formula + ">" + total_op + ")"
                    O_c.append(formula_total)
                if len(O_c) != 0:
                    Y_xy.append(Logica.Ytoria(O_c))
    return Logica.Ytoria(Y_xy)                   

def regla_7(): # Asignar top-bottom
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys() and (y!=0 and y!=Ny-1):
                O_c = []
                for c in C:
                    formula = "(" + OenCasilla.P([x, y, c, 0]) + "Y" + OenCasilla.P([x, y, c, 1]) + ")"
                    vecinos = []
                    if((x, y + 1) in pos_t.keys()):
                        if ((x, y - 1) in pos_t.keys()): # bottom es Terminal y top es Terminal
                            continue
                        else: # bottom es Terminal y top no es Terminal
                            vecinos.append( OenCasilla.P([x, y - 1, pos_t[(x, y + 1)], 1]) )
                    elif ((x, y - 1) in pos_t.keys()): # bottom no es Terminal y top es Terminal
                        vecinos.append( OenCasilla.P([x, y + 1, pos_t[(x, y - 1)], 0]) )
                    else: # ni bottom ni top son Terminal
                        vecinos.append( "(" + OenCasilla.P([x, y + 1, c , 0]) + "Y" + OenCasilla.P([x ,y - 1, c, 1]) + ")")
                    opuestos_a = ["-" + OenCasilla.P([x - 1, y, o, 3]) for o in C if x - 1 in X]
                    opuestos_b = ["-" + OenCasilla.P([x + 1, y, o, 2]) for o in C if x + 1 in X]
                    total_op = Logica.Ytoria(vecinos + opuestos_a + opuestos_b)
                    formula_total = "(" + formula + ">" + total_op + ")"
                    O_c.append(formula_total)
                if len(O_c) != 0:
                    Y_xy.append(Logica.Ytoria(O_c))
    return Logica.Ytoria(Y_xy)

def regla_8(): # Asignar left-bottom
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys() and (x!=0 and y!=Ny-1):
                O_c = []
                for c in C:
                    formula = "(" + OenCasilla.P([x, y, c, 2]) + "Y" + OenCasilla.P([x, y, c, 1]) + ")"
                    vecinos = []
                    if((x, y + 1) in pos_t.keys()):
                        if ((x - 1, y) in pos_t.keys()): # bottom es Terminal y left es Terminal
                            continue
                        else: # bottom es Terminal y left no es Terminal
                            vecinos.append( OenCasilla.P([x - 1, y, pos_t[(x, y + 1)], 3]) )
                    elif ((x - 1, y) in pos_t.keys()): # bottom no es Terminal y left es Terminal
                        vecinos.append( OenCasilla.P([x, y + 1, pos_t[(x - 1, y)], 0]) )
                    else: # ni bottom ni left son Terminal
                        vecinos.append( "(" + OenCasilla.P([x, y + 1, c , 0]) + "Y" + OenCasilla.P([x - 1, y, c, 3]) + ")")
                    opuestos_a = ["-" + OenCasilla.P([y - 1, y, o, 1]) for o in C if y - 1 in X]
                    opuestos_b = ["-" + OenCasilla.P([x + 1, y, o, 2]) for o in C if x + 1 in X]
                    total_op = Logica.Ytoria(vecinos + opuestos_a + opuestos_b)
                    formula_total = "(" + formula + ">" + total_op + ")"
                    O_c.append(formula_total)
                if len(O_c) != 0:
                    Y_xy.append(Logica.Ytoria(O_c))
    return Logica.Ytoria(Y_xy)

def regla_9(): # Asignar right-bottom
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys() and (x!=Nx-1 and y!=Ny-1):
                O_c = []
                for c in C:
                    formula = "(" + OenCasilla.P([x, y, c, 3]) + "Y" + OenCasilla.P([x, y, c, 1]) + ")"
                    vecinos = []
                    if((x, y + 1) in pos_t.keys()):
                        if ((x + 1, y) in pos_t.keys()): # bottom es Terminal y right es Terminal
                            continue
                        else: # bottom es Terminal y right no es Terminal
                            vecinos.append( OenCasilla.P([x + 1, y, pos_t[(x, y + 1)], 2]) )
                    elif ((x + 1, y) in pos_t.keys()): # bottom no es Terminal y right es Terminal
                        vecinos.append( OenCasilla.P([x, y + 1, pos_t[(x + 1, y)], 0]) )
                    else: # ni bottom ni right son Terminal
                        vecinos.append( "(" + OenCasilla.P([x, y + 1, c , 0]) + "Y" + OenCasilla.P([x + 1, y, c, 2]) + ")")
                    opuestos_a = ["-" + OenCasilla.P([x, y - 1, o, 1]) for o in C if y - 1 in X]
                    opuestos_b = ["-" + OenCasilla.P([x - 1, y, o, 3]) for o in C if x - 1 in X]
                    total_op = Logica.Ytoria(vecinos + opuestos_a + opuestos_b)
                    formula_total = "(" + formula + ">" + total_op + ")"
                    O_c.append(formula_total)
                if len(O_c) != 0:
                    Y_xy.append(Logica.Ytoria(O_c))
    return Logica.Ytoria(Y_xy)

def regla_10():
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t.keys():
                if x == 0:
                    f = "-"+Logica.Otoria([OenCasilla.P([x,y,c,2]) for c in C])
                    Y_xy.append(f)
                elif x==Nx-1:
                    f = "-"+Logica.Otoria([OenCasilla.P([x,y,c,3]) for c in C])
                    Y_xy.append(f)
                if y == 0:
                    f = "-"+Logica.Otoria([OenCasilla.P([x,y,c,0]) for c in C])
                    Y_xy.append(f)
                elif y == Ny-1:
                    f = "-"+Logica.Otoria([OenCasilla.P([x,y,c,1]) for c in C])
                    Y_xy.append(f)
    return Logica.Ytoria(Y_xy)

def coors(x,y):
    return -200+(x*100),200-(y*100)

def visualizar(I):
    import turtle
    FlowWindow = turtle.Screen()
    FlowWindow.setup(500,500)
    FlowWindow.title("FlowFree")
    FlowWindow.tracer(0)
    for T in range(Nc):
            FlowWindow.addshape('img/{0}.gif'.format(T))
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

def flowSAT():
        SAT = []
        SAT.append(regla_1())
        SAT.append(regla_2())
        SAT.append(regla_3())
        SAT.append(regla_4())
        SAT.append(regla_5())
        SAT.append(regla_6())
        a = regla_7()
        if len(a) != 0:
            SAT.append(regla_7())
        SAT.append(regla_8())
        SAT.append(regla_9())
        SAT.append(regla_10())
        #for i in SAT:
        #    print(SAT.index(i))
        #    a = Logica.tseitin(i)
        return Logica.Ytoria(SAT)


M = resolver(flowSAT())
M = resolver(flowSAT())
if M:
    visualizar(M)
