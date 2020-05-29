import sys


def count_inversion(input_list):
    if len(input_list) <= 1:
        return input_list, 0
    else:
        mid = int(len(input_list) / 2)
        left, a = count_inversion(input_list[:mid])
        right, b = count_inversion(input_list[mid:])
        result, c = merge_and_count(left, right)
        return result, (a + b + c)


def merge_and_count(left, right):
    result = []
    count = 0
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            count += len(left)-i
            j += 1
        else:
            i += 1

    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while left[i:] or right[j:]:
        if left[i:]:
            result.append(left[i])
            i += 1
        if right[j:]:
            result.append(right[j])
            j += 1
    return result, count


if __name__ == '__main__':
    data = sys.stdin.readlines()
    input_text = []
    for line in data:
        input_text.append(int(line.rstrip("\n")))
    input_text.pop(0)
    count = count_inversion(input_text)[1]
    print(count)
