def arrayChallenge(arr):
    n = len(arr)
    result = [0] * n

    for i in range(n):
        counter = 0
        for j in range(i):
            if arr[j] > arr[i]:
                counter -= abs(arr[j] - arr[i])
            else:
                counter += abs(arr[j] - arr[i])
        result[i] = counter

    return result
arr = [4,1,2,2,3]
print(arrayChallenge(arr))  # Output: [0, 2, 0]