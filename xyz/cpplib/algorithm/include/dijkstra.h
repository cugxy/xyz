//
// Created by cugxy on 2020/8/18.
//

#ifndef CPPLIB_DIJKSTRA_H
#define CPPLIB_DIJKSTRA_H

#include <iostream>
#include <climits>
#include <cfloat>
#include <algorithm>
#include "export_algorithm.h"

using std::cout;
using std::endl;

namespace cugxy {
    template<class E>
    int minDistance(E *dist, bool *sptSet, int nCount) {
        E min = DBL_MAX;
        int minIndex = 0;
        for (int v = 0; v < nCount; ++v) {
            if (!sptSet[v] && dist[v] <= min)
                min = dist[v], minIndex = v;
        }
        return minIndex;
    }

    template<class E>
    void printSolution(E *dist, int nCount)
    {
        cout << "Vertex   Distance from Source\n";
        for (int i = 0; i < nCount; ++i)
            cout << i <<" tt " << dist[i] << endl;
    }

    template <class E>
    void dijkstra(E **graph, int src, int nCount)
    {
        E dist[nCount];
        bool sptSet[nCount];
        for (int i = 0; i < nCount; i++)
            dist[i] = DBL_MAX, sptSet[i] = false;
        dist[src] = 0.0;
        for (int count = 0; count < nCount - 1; ++count)
        {
            int u = minDistance<E>(dist, sptSet, nCount);
            sptSet[u] = true;
            for (int v = 0; v < nCount; ++v)
            {
                if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX && dist[u] + graph[u][v] < dist[v])
                    dist[v] = dist[u] + graph[u][v];
            }
        }
        printSolution<E>(dist, nCount);
    }

    template ALGORITHM_LIBRARY_EXPORT int minDistance(int *dist, bool *sptSet, int nCount);
    template ALGORITHM_LIBRARY_EXPORT void printSolution(int *dist, int nCount);
    template ALGORITHM_LIBRARY_EXPORT void dijkstra(int **graph, int src, int nCount);

    template ALGORITHM_LIBRARY_EXPORT int minDistance(float *dist, bool *sptSet, int nCount);
    template ALGORITHM_LIBRARY_EXPORT void printSolution(float *dist, int nCount);
    template ALGORITHM_LIBRARY_EXPORT void dijkstra(float **graph, int src, int nCount);

    template ALGORITHM_LIBRARY_EXPORT int minDistance(double *dist, bool *sptSet, int nCount);
    template ALGORITHM_LIBRARY_EXPORT void printSolution(double *dist, int nCount);
    template ALGORITHM_LIBRARY_EXPORT void dijkstra(double **graph, int src, int nCount);
};

#endif //CPPLIB_DIJKSTRA_H
