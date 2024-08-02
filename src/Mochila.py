import gurobipy as gp
from gurobipy import GRB
import sys

def read_backpack_file(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip().split()
        n = int(first_line[0])
        m = int(first_line[1])
        
        capacities_line = file.readline().strip().split()
        capacities = [int(capacity) for capacity in capacities_line]
        
        items = []
        for _ in range(n):
            item_line = file.readline().strip().split()
            benefit = int(item_line[0])
            weight = int(item_line[1])
            items.append((benefit, weight))

    return n, m, capacities, items


if __name__ == "__main__":
    filename = sys.argv[1]
    n,m,capacities,items = read_backpack_file(filename)
    itens_bp={}
    print(n, m, capacities, items)
    model = gp.Model("multiple_backpack")
    # Cria variáveis de decisão para cada par (i, j)
    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")
    # Maximiza a soma do valor colocado em cada mochila
    model.setObjective(gp.quicksum(items[i][0]*x[i, j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)

    # Restrições do peso de cada mochila
    for j,capacity in enumerate(capacities):
        model.addConstr(gp.quicksum(items[i][1]*x[i, j] for i in range(n)) <= capacity, f"backpack_{j}_constraint")

    # Restrições de um item estar somente em uma mochila
    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(m)) <= 1, f"item_{i}_constraint")

    # Otimiza o modelo
    model.optimize()
    for i in range(n):
        for j in range(m):
            #print(f"x[{i},{j}] = {x[i, j].X}")
            if (x[i,j].X) >= 1:
                if j not in itens_bp:
                    itens_bp[j]=[]
                itens_bp[j].append(i)

    print("\n\n---------------------------------------------------\n \t \t Solução Ótima\n ---------------------------------------------------")
    print(f"Valor da função Objetivo: {model.Objval}")
    for i in range(m):
        print(f"Itens na mochila {i}: {itens_bp[i]}")



