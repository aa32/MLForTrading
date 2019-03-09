"""assess a betting strategy.

copyright 2018, georgia institute of technology (georgia tech)
atlanta, georgia 30332
all rights reserved

template code for cs 4646/7646

georgia tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  this copyright statement should not be removed
or edited.

we do grant permission to share solutions privately with non-students such
as potential employers. however, sharing with other current or future
students of cs 7646 is prohibited and subject to being investigated as a
gt honor code violation.

-----do not edit anything above this line---

student name: Anshuta Awasthi
gt user id: aawasthi32
gt id: 903379179
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np



def author():
    return 'aawasthi32'  # replace tb34 with your georgia tech username.


def gtid():
    return 903379179    # replace with your gt id number

def get_spin_result(win_prob):
    # type: (object) -> object
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result

def strategy(winning,win_prob):
    episode_winnings = 0
    i = 1
    while (episode_winnings < 80 and i <= 1000):
        bet_amount = 1
        won = False

        while not won:
            won = get_spin_result(win_prob)
            if won:
                episode_winnings = episode_winnings + bet_amount

            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2

            winning[i] = episode_winnings
            i = i + 1
    winning[i:] = 80
    return winning



def strategy2(winning,win_prob):
    episode_winnings = 0
    i = 1
    roll = 256
    flag = True
    while (episode_winnings < 80 and flag and i < 1000):
        bet_amount = 1
        won = False

        while not won:
            won = get_spin_result(win_prob)

            if(roll < bet_amount):
                bet_amount = roll


            if won:
                episode_winnings = episode_winnings + bet_amount
                roll = 256 + episode_winnings


            elif (episode_winnings > -256):
                episode_winnings = episode_winnings - bet_amount
                roll = 256 + episode_winnings
                bet_amount = bet_amount * 2


            elif (episode_winnings == -256):
                flag = False
                break

            winning[i] = episode_winnings
            i = i + 1
    if flag:
        winning[i:] = 80
    else:
        winning[i:] = -256
    return winning


def fig1(win_prob):
    x = np.arange(301)
    y = np.zeros(len(x))
    plt.figure(1)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.title('Figure 1')
    y = np.arange(-256, 100)
    # plt.figure()
    plt.interactive(False)
    for j in range(0, 10):
        print('this is episode', format(j))
        winning = np.zeros((1000,), dtype=np.int)
        yall = strategy(winning, win_prob)
        y = yall[0:301]
        plt.plot(x, y)

    plt.savefig('Figure1.png')



def fig2(win_prob):
    plt.figure(2)
    plt.title('Figure 2')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    y = np.zeros(1000)
    x = np.arange(1000)
    yall = np.zeros((1000,1000))
    for i in range(0, 1000):
        winning = np.zeros((1000,), dtype=np.int)
        yall[i] = strategy(winning, win_prob)

    yall = np.transpose(yall)

    for j in range(0,1000):
        y[j] = np.mean(yall[j])
    plt.plot(x,y,label = 'Mean')


    for k in range(0, 1000):
        y[k] = np.mean(yall[k]) + np.std(yall[k])
    plt.plot(x,y ,label='Mean + Std')


    for l in range(0, 1000):
        y[l] = np.mean(yall[l]) - np.std(yall[l])
    plt.plot(x,y,label='Mean - Std')

    plt.legend()
    plt.savefig('Figure2.png')




def fig3(win_prob):
    plt.figure(3)
    plt.title('Figure 3')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    y = np.zeros(1000)
    x = np.arange(1000)
    yall = np.zeros((1000,1000))
    for i in range(0, 1000):
        winning = np.zeros((1000,), dtype=np.int)
        yall[i] = strategy(winning, win_prob)

    yall = np.transpose(yall)

    for j in range(0,1000):
        y[j] = np.median(yall[j])
    plt.plot(x,y,label = 'Median')


    for k in range(0, 1000):
        y[k] = np.median(yall[k]) + np.std(yall[k])
    plt.plot(x,y ,label = 'Median+Std')


    for l in range(0, 1000):
        y[l] = np.median(yall[l]) - np.std(yall[l])
    plt.plot(x,y ,label = 'Median-Std')

    plt.legend()
    plt.savefig('Figure3.png')



def fig4(win_prob):
    plt.figure(4)
    plt.title('Figure 4')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    y = np.zeros(1000)
    x = np.arange(1000)
    yall = np.zeros((1000,1000))
    for i in range(0, 1000):
        winning = np.zeros((1000,), dtype=np.int)
        yall[i] = strategy2(winning, win_prob)

    yall = np.transpose(yall)

    for j in range(0,1000):
        y[j] = np.mean(yall[j])
    plt.plot(x,y , label = 'Mean')


    for k in range(0, 1000):
        y[k] = np.mean(yall[k]) + np.std(yall[k])
    plt.plot(x,y , label = 'Mean+Std')


    for l in range(0, 1000):
        y[l] = np.mean(yall[l]) - np.std(yall[l])
    plt.plot(x,y,label = 'Mean-Std.')

    plt.legend()
    plt.savefig('Figure4.png')


def fig5(win_prob):
    plt.figure(5)
    plt.title('Figure 5')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    y = np.zeros(1000)
    x = np.arange(1000)
    yall = np.zeros((1000,1000))
    for i in range(0, 1000):
        winning = np.zeros((1000,), dtype=np.int)
        yall[i] = strategy2(winning, win_prob)

    yall = np.transpose(yall)

    for j in range(0,1000):
        y[j] = np.median(yall[j])
    plt.plot(x,y , label = 'Median')


    for k in range(0, 1000):
        y[k] = np.median(yall[k]) + np.std(yall[k])
    plt.plot(x,y, label = 'Median+Std.')


    for l in range(0, 1000):
        y[l] = np.median(yall[l]) - np.std(yall[l])
    plt.plot(x,y , label = 'Median-Std.')

    plt.legend()
    plt.savefig('Figure5.png')




def test_code():
    win_prob = 18.0 / 38.0 # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    fig1(win_prob)
    fig2(win_prob)
    fig3(win_prob)
    fig4(win_prob)
    fig5(win_prob)


    # print get_spin_result(win_prob)  # test the roulette spin


# add your code here to implement the experiments

if __name__ == "__main__":
    test_code()