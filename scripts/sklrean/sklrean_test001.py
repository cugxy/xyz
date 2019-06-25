#!usr/bin/env python  
# -*- coding:utf-8 _*-

from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC
from IPython import embed


def bc():
    data = pd.read_table(r'testSet.txt', header=None, delim_whitespace=True)
    X_train = np.array(data.loc[:][[0, 1]])
    y_train = np.array(data[2])
    y_train = np.where(y_train == 1, 1, -1)
    x_min = X_train[:, 0].min()
    x_max = X_train[:, 0].max()
    y_min = X_train[:, 1].min()
    y_max = X_train[:, 1].max()
    plt.figure(figsize=(15, 15))
    for fig_num, kernel in enumerate(('linear', 'poly', 'rbf')):
        svm_ = SVC(kernel=kernel)
        svm_.fit(X_train, y_train)
        plt.subplot(222 + fig_num)
        plt.scatter(x = X_train[y_train == 1, 0], y = X_train[y_train == 1, 1],
                    s = 30, marker = 'o', color = 'yellow', zorder = 10)
        plt.scatter(x = X_train[y_train == -1, 0], y = X_train[y_train == -1, 1],
                    s = 30, marker = 'x', color = 'blue', zorder = 10)
        plt.scatter(x = [x[0] for x in svm_.support_vectors_], y = [x[1] for x in svm_.support_vectors_], s = 80, facecolors='none', zorder = 10)
        print(len(svm_.support_vectors_))
        plt.title(kernel)
        plt.xlabel('support vectors ' + str(len(svm_.support_vectors_)))
        plt.xticks([])
        plt.yticks([])
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
        Z = svm_.decision_function(np.c_[XX.ravel(), YY.ravel()])
        Z = Z.reshape(XX.shape)
        plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
        plt.contour(XX, YY, Z, colors=['black', 'k', 'white'], linestyles=['--', '-', '--'], levels=[-.5, 0, .5])

    # plot data
    plt.subplot(221)
    plt.title('data')
    plt.scatter(x=X_train[y_train == 1, 0], y=X_train[y_train == 1, 1],
                s=30, marker='o', color='red', zorder=10)
    plt.scatter(x=X_train[y_train == -1, 0], y=X_train[y_train == -1, 1],
                s=30, marker='x', color='blue', zorder=10)
    plt.xticks([])
    plt.yticks([])
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.savefig(str(kernel) + '.jpg')
    plt.show()


if __name__ == '__main__':
    if 1:
        bc()
    pass
