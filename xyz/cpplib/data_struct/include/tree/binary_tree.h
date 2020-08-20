//
// Created by cugxy on 2020/8/20.
//

#ifndef CPPLIB_BINARY_TREE_H
#define CPPLIB_BINARY_TREE_H

#include "export_datastruct.h"

namespace cugxy
{
    template <class E>
    struct BinaryNode {
        E               val;
        BinaryNode<E>  *pLeft;
        BinaryNode<E>  *pRight;
    };

    template <class E>
    class BinaryTree {
    protected:
        BinaryNode<E> * m_pRoot;

        void displayNode(BinaryNode<E> *pNode);
        int deepNode(BinaryNode<E> *pNode);
        bool isFullNode(BinaryNode<E> *pNode);

    public:
        BinaryTree(BinaryNode<E> * pRoot);
        virtual ~BinaryTree();

        void display();

        int deep();

        bool isFull();
    };

    template class DATA_STRUCT_LIBRARY_EXPORT BinaryNode<int>;
    template class DATA_STRUCT_LIBRARY_EXPORT BinaryTree<int>;
}

#endif //CPPLIB_BINARY_TREE_H
