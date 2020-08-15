//
// Created by cugxy on 2020/8/15.
//

#include "p_queue.h"

using cugxy::PQueue;


template<class E>
PQueue<E>::PQueue(int size)
        : m_pElements(nullptr)
        , m_nCount(0)
        , m_nMaxSize(-1)
{
    m_nMaxSize = size;
    m_pElements = new E[m_nMaxSize];
}

template<class E>
PQueue<E>::~PQueue()
{
    if (m_pElements != nullptr)
    {
        delete m_pElements;
        m_pElements = nullptr;
    }
}

template<class E>
void PQueue<E>::adjust()
{
    E tmp = m_pElements[m_nCount - 1];
    int j = 0;
    for (j = m_nCount - 2; j >= 0; --j)
    {
    if (m_pElements[j] < tmp)    break;
    m_pElements[j + 1] = m_pElements[j];
    }
    m_pElements[j + 1] = tmp;
}

template<class E>
bool PQueue<E>::Insert(const E &x)
{
    if (m_nCount == m_nMaxSize) return false;
    m_pElements[m_nCount++] = x;
    adjust();
    return true;
}

template<class E>
bool PQueue<E>::RemoveMin(E& x)
{
    if (m_nCount == 0) return false;
    x = m_pElements[0];
    for (int i = 1; i < m_nCount; ++i)
    {
        m_pElements[i - 1] = m_pElements[i];
    }
    --m_nCount;
    return true;
}



