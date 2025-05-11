from basic import request1_2

for tryid in range(233, 253):
    print(tryid) if len((result := request1_2(tryid))) == 1 else print(tryid, result)
