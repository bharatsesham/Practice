import sys


def lcs(string_1, string_2):
    seq = ''
    len_string_1 = len(string_1)
    len_string_2 = len(string_2)
    opt = [[0]*(len_string_2 + 1) for _ in range(len_string_1 + 1)]
    pi = [[0]*(len_string_2 + 1) for _ in range(len_string_1 + 1)]

    for i in range(1, len_string_1 + 1):
        for j in range(1, len_string_2 + 1):
            if string_1[i - 1] == string_2[j - 1]:
                opt[i][j] = opt[i-1][j-1]+1
                pi[i][j] = 'DU'
            elif opt[i-1][j] <= opt[i][j-1]:
                opt[i][j] = opt[i][j-1]
                pi[i][j] = 'L'
            else:
                opt[i][j] = opt[i-1][j]
                pi[i][j] = 'U'

    i = len_string_1
    j = len_string_2
    while i > 0 and j > 0:
        if pi[i][j] == 'DU':
            seq += (string_1[i - 1])
            i -= 1
            j -= 1
        elif pi[i][j] == 'L':
            j -= 1
        else:
            i -= 1

    return seq[::-1], opt[len_string_1][len_string_2]


if __name__ == '__main__':
    input_1 = sys.stdin.readline().rstrip()
    input_2 = sys.stdin.readline().rstrip()
    lcs = lcs(input_1, input_2)
    print(lcs[1])
    print(lcs[0])
