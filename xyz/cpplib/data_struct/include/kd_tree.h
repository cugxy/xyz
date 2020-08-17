//
// Created by cugxy on 2020/8/11.
//

#ifndef CPPLIB_KD_TREE_H
#define CPPLIB_KD_TREE_H

#include <vector>
#include <ostream>
#include <iostream>
#include "export_datastruct.h"

using std::vector;
using std::ostream;
using std::cout;
using std::endl;

namespace cugxy{

    template<class E>
    struct KDNode {
        KDNode *    pParent;
        KDNode *    pLeft;
        KDNode *    pRight;
        int         nAxis;
        vector<E>   val;

        KDNode(vector<E> data, int ax)
        {
            val = data;
            nAxis = ax;
            pParent = nullptr;
            pLeft = nullptr;
            pRight = nullptr;
        }
    };

    template<class E>
    class KDTree {
    protected:
        int                 m_nDimension;
        int                 m_nCurDim;
        vector<vector<E> >  m_Data;
        KDNode<E> *         m_pRoot;

    private:
        void createTree();

        bool compare(const vector<E> &a, const vector<E> &b);

        int disVector(const vector<E> &a, const vector<E> &b);

        KDNode<E> * createTreeNode(int left, int right, int dim);

        void printTreeNode(KDNode<E> *r);

        void queryNode(const vector<E> &d, int &minDis, KDNode<E> * &nearNode, KDNode<E> *tmpNode);

    public:
        explicit KDTree(vector<vector<E> > data, int dim);

        virtual ~KDTree();

        void printTree();

        KDNode<E>* query(const vector<E> &d);
    };

    ostream & operator<<(ostream & os, vector<int> vi)
    {
        os << "(";
        for (int i = 0; i < vi.size(); i++)
            cout << vi[i] << ",";
        os << ")";
        return os;
    }

    template class DATASTRUCT_LIBRARY_EXPORT KDNode<int>;
    template class DATASTRUCT_LIBRARY_EXPORT KDTree<int>;

};

#endif //CPPLIB_KD_TREE_H
