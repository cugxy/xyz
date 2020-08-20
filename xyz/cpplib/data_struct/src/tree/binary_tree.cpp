//
// Created by cugxy on 2020/8/20.
//

#include "tree/binary_tree.h"
#include <iostream>
#include <algorithm>

using std::cout;
using std::endl;
using std::max;

using cugxy::BinaryNode;
using cugxy::BinaryTree;

template<class E>
BinaryTree<E>::BinaryTree(BinaryNode<E> *pRoot): m_pRoot(pRoot)
{

}

template<class E>
BinaryTree<E>::~BinaryTree()
{

}

template<class E>
void BinaryTree<E>::displayNode(BinaryNode<E> *pNode) {
    if (pNode != nullptr)
    {
        displayNode(pNode->pLeft);
        cout << pNode->val << endl;
        displayNode(pNode->pRight);
    }
}

template<class E>
int BinaryTree<E>::deepNode(BinaryNode<E> *pNode) {
    return (pNode == nullptr) ? 0 : (1 + max(deepNode(pNode->pRight), deepNode(pNode->pLeft)));
}

template<class E>
bool BinaryTree<E>::isFullNode(BinaryNode<E> *pNode) {
    if (pNode == nullptr)
        return true;
    if (pNode->pLeft != nullptr && pNode->pRight != nullptr)
        return isFullNode(pNode->pLeft) && isFullNode(pNode->pRight);
    else
        return pNode->pLeft == nullptr && pNode->pRight == nullptr;
}

template<class E>
void BinaryTree<E>::display() {
    displayNode(m_pRoot);
}

template<class E>
int BinaryTree<E>::deep() {
    return deepNode(m_pRoot);
}

template<class E>
bool BinaryTree<E>::isFull() {
    return isFullNode(m_pRoot);
}
