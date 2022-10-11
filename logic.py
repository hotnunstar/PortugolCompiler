# logic.py
# Authors: Joel Figueiras (20809) & Nuno Araújo (20078)

from my_lib import run_batch

print("Escolha a opção pretendida:")
print("[1] Executar algoritmo")
print("[2] Gerar código C")
op = input()

while op != '1' and op != '2':
    print(f"Unknown option {op}, try again!")
    op = input()
run_batch("portu.gol", op)



