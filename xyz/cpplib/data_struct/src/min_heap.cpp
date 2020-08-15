//
// Created by cugxy on 2020/8/15.
//

#include "min_heap.h"

using cugxy::MinHeap;

template<class E>
void MinHeap<E>::siftDown(int nStart, int m)
{

}

template<class E>
void MinHeap<E>::siftUp(int nStart)
{

}

template<class E>
MinHeap<E>::MinHeap(int size)
: m_pHeap(nullptr)
, m_nCount(0)
, m_nMaxSize(size)
{

}

template<class E>
MinHeap<E>::MinHeap(E *arr, int size)
: m_pHeap(arr)
, m_nCount(0)
, m_nMaxSize(size)
{

}

template<class E>
MinHeap<E>::~MinHeap() {

}

template<class E>
bool MinHeap<E>::RemoveMin(E &x) {
    return false;
}

template<class E>
bool cugxy::MinHeap<E>::insert(E &x) {
    return false;
}


