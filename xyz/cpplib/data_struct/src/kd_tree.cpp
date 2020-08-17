//
// Created by cugxy on 2020/8/11.
//

#include "kd_tree.h"
#include <climits>
#include <algorithm>

using std::sort;
using std::min;
using cugxy::KDNode;
using cugxy::KDTree;


template<class E>
KDTree<E>::KDTree(vector<vector<E>> data, int dim)
{
    m_nDimension = dim;
    m_Data = data;
    createTree();
}

template<class E>
KDTree<E>::~KDTree() {

}

template<class E>
void KDTree<E>::createTree() {
    m_pRoot = createTreeNode(0, m_Data.size()-1, 0);
}

template<class E>
bool KDTree<E>::compare(const vector<E> &a, const vector<E> &b) {
    return a[m_nCurDim] < b[m_nCurDim];
}

template<class E>
KDNode<E> *KDTree<E>::createTreeNode(int left, int right, int dim) {
    if (right < left)
        return nullptr;
    m_nCurDim = dim;
    // sort(m_Data.begin() + left, m_Data.begin() + right+1, this->compare);
    //@todo: 按照 m_nCCurDim 进行排序

    int mid = (left + right+1) / 2;
    auto *r = new KDNode<E>(m_Data[mid], dim);
    r->pLeft = createTreeNode(left, mid - 1, (dim + 1) % m_nDimension);
    if (r->pLeft != nullptr)
        r->pLeft->pParent = r;
    r->pRight = createTreeNode(mid + 1, right, (dim + 1) % m_nDimension);
    if (r->pRight != nullptr)
        r->pRight->pParent = r;
    return r;
}

template<class E>
void KDTree<E>::printTreeNode(KDNode<E> *r) {
    if (r == nullptr)
        return;
    printTreeNode(r->pLeft);
    cout << r->val << "\t";
    printTreeNode(r->pRight);
}

template<class E>
void KDTree<E>::queryNode(const vector<E> &d, int &minDis, KDNode<E> *&nearNode, KDNode<E> *tmpNode) {
    if (tmpNode == nullptr)
        return;
    cout << "now node: " << tmpNode->val << endl;
    if (disVector(tmpNode->val, d) < minDis)
    {
        minDis = disVector(tmpNode->val, d);
        nearNode = tmpNode;
    }
    if (abs(tmpNode->val[tmpNode->nAxis] - d[tmpNode->nAxis]) < minDis)
    {
        queryNode(d, minDis, nearNode, tmpNode->pLeft);
        queryNode(d, minDis, nearNode, tmpNode->pRight);
    } else
    {
        if (tmpNode->val[tmpNode->nAxis] > d[tmpNode->nAxis])
            queryNode(d, minDis, nearNode, tmpNode->pLeft);
        else
            queryNode(d, minDis, nearNode, tmpNode->pRight);
    }
}

template<class E>
void KDTree<E>::printTree() {
    printTreeNode(m_pRoot);
}


template<class E>
KDNode<E> *KDTree<E>::query(const vector<E> &d) {
    int dim = 0, minDis = INT_MAX;
    KDNode<E> * r = m_pRoot;
    KDNode<E> * pTmp;
    while (r != nullptr)
    {
        pTmp = r;
        if (d[dim] < r->val[dim])
            r = r->pLeft;
        else
            r = r->pRight;
        dim = (dim + 1) % m_nDimension;
    }
    minDis = min(disVector(d, pTmp->val), minDis);
    KDNode<E> * nearNode = pTmp;
    cout << endl<<"nearest node: " << pTmp->val << endl;

    while (pTmp->pParent != nullptr)
    {
        pTmp = pTmp->pParent;
        if (disVector(pTmp->val, d) < minDis)
        {
            nearNode = pTmp;
            minDis = disVector(pTmp->val, d);
        }
        cout << "now parent node: " << pTmp->val << endl;
        KDNode<E> * son;
        // 判断当前轴与点的距离，如果小于minDis，则进行到另一半进行查找
        if (abs(pTmp->val[pTmp->nAxis] - d[pTmp->nAxis]) < minDis)
        {
            if (pTmp->val[pTmp->nAxis] > d[pTmp->nAxis])
                son = pTmp->pRight;
            else
                son = pTmp->pLeft;
            queryNode(d, minDis, nearNode, son);
        }
    }
    return nearNode;
}

template<class E>
int KDTree<E>::disVector(const vector<E> &a, const vector<E> &b) {
    int sum = 0;
    for (int i = 0; i < a.size(); ++i)
        sum += (a[i] - b[i])*(a[i] - b[i]);
    return sum;
}




