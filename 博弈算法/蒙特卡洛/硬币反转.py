import random
import matplotlib.pyplot as plt

def coin_flip():
    return random.randint(0,1)

list1=[]
def monte_carlp(n):
    results=0
    for i in range(1,n):
        flip_result=coin_flip()
        results=results+flip_result
        prob_value=results/i
        list1.append(prob_value)

    return results/n
answer=monte_carlp(5000)

plt.axhline(y=0.5,color='r',linestyle='-')
plt.xlabel('Iterations')
plt.ylabel('Probability')
plt.plot(list1)
plt.show()

print('结果是：',answer)

