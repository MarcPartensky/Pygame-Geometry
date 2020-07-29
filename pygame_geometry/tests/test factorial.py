def factorial(n):
    v=1
    for i in range(1,n+1):
        #v*=i
        v=v*i
    return v


def factorial(n):
    if n=1:
        return 1
    else:
        return n*factorial(n-1)


factorial = lambda n*factorial(n-1) if n>1 else 1


print(factorial(5))
