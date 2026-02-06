
# Python Program to find the Nth fibonacci number using Matrix Exponentiation

def multiply(A, B):
    C = [[0, 0], [0, 0]]
    C[0][0] = A[0][0] * B[0][0] + A[0][1] * B[1][0]
    C[0][1] = A[0][0] * B[0][1] + A[0][1] * B[1][1]
    C[1][0] = A[1][0] * B[0][0] + A[1][1] * B[1][0]
    C[1][1] = A[1][0] * B[0][1] + A[1][1] * B[1][1]
    A[0][0] = C[0][0]
    A[0][1] = C[0][1]
    A[1][0] = C[1][0]
    A[1][1] = C[1][1]

def power(M, expo):
    ans = [[1, 0], [0, 1]]
    while expo:
        if expo & 1:
            multiply(ans, M)
        multiply(M, M)
        expo >>= 1
    return ans


def nthFibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    M = [[1, 1], [1, 0]]
    res = power(M, n - 1)
    return res[0][0]

class FibonacciCalculator:
    def number(self, n):
        if n < 0:
            raise ValueError('n must be non-negative')
        return nthFibonacci(n)

    def sequence(self, n):
        if n < 0:
            raise ValueError('n must be non-negative')
        return [nthFibonacci(i) for i in range(n)]
