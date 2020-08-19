//
// Created by cugxy on 2020/8/11.
//

#include "kd_tree.h"
#include <climits>
#include <algorithm>
#include <numeric>
#include <cmath>

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
KDTree<E>::~KDTree() = default;


template<class E>
int KDTree<E>::calSplitDim(int left, int right)
{
    if (left == right)
        return 0;
    double maxStd = 0.0;
    int rsDim = 0;
    for (int i = 0; i < m_nDimension; ++i)
    {
        vector<E> tmpLst;
        for (auto it = m_Data.begin() + left; it != m_Data.begin() + right + 1; ++it)
        {
            auto tmpData = *it;
            tmpLst.push_back(tmpData[i]);
        }
        E sum = std::accumulate(std::begin(tmpLst), std::end(tmpLst), 0.0);
        E mean = sum / tmpLst.size();
        E accum;
        std::for_each(std::begin(tmpLst), std::end(tmpLst), [&](const E d){
            accum += ((d - mean) * (d - mean));
        });
        double stdev = std::sqrt(accum / (tmpLst.size()));
        if (stdev > maxStd)
        {
            maxStd = stdev;
            rsDim = i;
        }
    }
    return rsDim;
}

template<class E>
void KDTree<E>::createTree() {
    m_pRoot = createTreeNode(0, m_Data.size() - 1);
}

template<class E>
KDNode<E> *KDTree<E>::createTreeNode(int left, int right) {
    if (right < left)
        return nullptr;
    int nCurDim = calSplitDim(left, right);
    sort(m_Data.begin() + left,
         m_Data.begin() + right + 1,
         [&](const vector<int> &a, const vector<int> &b) {return a[nCurDim] < b[nCurDim]; }
    );
    int mid = (left + right + 1) / 2;
    auto *r = new KDNode<E>(m_Data[mid], nCurDim);
    r->pLeft = createTreeNode(left, mid - 1);
    if (r->pLeft != nullptr)
        r->pLeft->pParent = r;
    r->pRight = createTreeNode(mid + 1, right);
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





