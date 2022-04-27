import FlowRead
start = True

def read():
	try:
		MAP_INPUT = FlowRead.FlowRead(input("     >mapa: "))
		FlowRead.FlowPrint(MAP_INPUT)
	except:
		print("archivo no encontrado")
def solve():
	import FlowSolve
	terminales = []
	T = FlowRead.FlowRead(input("     >mapa: "))
	for y in range(len(T)):
		for x in range(len(T[y])):
			if T[y][x] == 'R':
				terminales.append((x,y,0,0))
			elif T[y][x] == 'G':
				terminales.append((x,y,1,0))
			elif T[y][x] == 'B':
				terminales.append((x,y,2,0))
			elif T[y][x] == 'O':
				terminales.append((x,y,3,0))
			else:
				continue
	formula = FlowSolve.asignarReglas(terminales)
	FlowRead.FlowPrint(formula)

def switch(case):
	if case == 'a':
		read()
	elif case == 'b':
		solve()
	elif case == 'c':
		start = False
		exit()
	else:
		print("opcion no valida")

def main():
	while start:
		print("")
		print("a.mostrar flow free")
		print("b.solucionar flow free")
		print("c.salir")
		print("")
		switch(input("   >"))

if __name__ == "__main__":
	main()


	

   
