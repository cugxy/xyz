//
// Created by cugxy on 2020/8/15.
//

#ifndef CPPLIB_PRIORITY_QUEUE_H
#define CPPLIB_PRIORITY_QUEUE_H

#include "export_datastruct.h"

namespace cugxy
{
    const int knDefaultPQSize = 50;

/**
* \brief 优先队列 小的优先
* \author	xy
*/
    template<class E>
    class PQueue {
    protected:
        E * m_pElements;    /**< 数组存储方式 */
        int m_nCount;       /**< 元素个数 */
        int m_nMaxSize;     /**< 最大容量 */

    protected:
        /**
        * \brief 调整 将新加的元素调整到合适的位置，之前的所有元素已经排序好，所以最坏时间复杂度为 O(n)所有的都要向后移动一次
        * return
        */
        void adjust();

    public:
        explicit PQueue(int size = knDefaultPQSize);

        virtual ~PQueue();

        bool Insert(const E& x);

        bool RemoveMin(E& x);

        bool GetFront(E& x) const
        {
            if (m_nCount == 0) return false;
            x = m_pElements[0];
            return true;
        }

        void MakeEmpty() { m_nCount = 0; }

        bool IsEmpty() const
        {
            return 0 == m_nCount;
        }

        bool IsFull() const
        {
            return m_nCount == m_nMaxSize;
        }

        int GetSize() const { return m_nCount; }
    };


    template class DATA_STRUCT_LIBRARY_EXPORT PQueue<int>;
};
#endif //CPPLIB_PRIORITY_QUEUE_H
