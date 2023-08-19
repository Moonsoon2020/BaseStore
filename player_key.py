from dbbase import ControlBD

con = ControlBD()
print(1, 2, 3)
for ke in con.get_user():
    print(ke)
    a = int(input())
    if a == 2:
        ke.ok = True
    if a == 3:
        ke.ok = False
    con.commit()