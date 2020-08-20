//
// Created by cugxy on 2020/8/20.
//

#ifndef CPPLIB_BINARY_SEARCH_TREE_H
#define CPPLIB_BINARY_SEARCH_TREE_H

namespace cugxy
{
    template <class E>
    struct BSNode {
        E           val;
        BSNode<E>  *pLeft;
        BSNode<E>  *pRight;
        BSNode<E>  *pParent;
    };

    template <class E>
    class BSTree {
    protected:
        BSNode<E> *pRoot;

    public:
        
    };

}

#endif //CPPLIB_BINARY_SEARCH_TREE_H
