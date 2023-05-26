import time

def init(chess_len):
    len = chess_len
    record = [[[0, 0, 0, 0] for x in range(chess_len)] for y in range(chess_len)]
    count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]
    pos_score = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(chess_len)] for y in range(chess_len)]
    for i in record:
        print(i)
    print('--------------------------------')
    print(count)
    print('--------------------------------')
    for j in pos_score:
        print(j)

CHESS_TYPE_NUM=8









