//
// Created by cugxy on 2020/8/15.
//

#ifndef CPPLIB_MIN_HEAP_H
#define CPPLIB_MIN_HEAP_H

namespace cugxy
{
    const int knDefaultTSize = 50;

    /**
    * \brief 最小堆
    * \author	xy
    */
    template<class E>
    class MinHeap {
    protected:
        E	*m_pHeap;	    /**< 数组存储方式 */
        int	m_nCount;	    /**< 元素个数 */
        int	m_nMaxSize;	    /**< 最大 */

        void siftDown(int nStart, int m);

        void siftUp(int nStart);

    public:
        explicit MinHeap(int size = knDefaultTSize);

        explicit MinHeap(E arr[], int size);

        virtual ~MinHeap();

        bool RemoveMin(E& x);

        bool insert(E & x);

        bool IsEmpty() const { return true; };

        bool IsFull() const { return true; };

        void makeEmpty() { };
    };


};
#endif //CPPLIB_MIN_HEAP_H
