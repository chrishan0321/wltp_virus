import random


def make_lotto():
    lotto = []
    # lotto = [ 23, 1, 10 ]
    count = 0
    while count < 6:
        num = random.randint(1, 45)
        # num = 23
        if lotto.count(num) == 0:
            lotto.append(num)
            count += 1
        else:
            continue
    return lotto


print("-------로또 번호 생성기-------")
lotto = make_lotto()
print(lotto)
print("----------------------------")