//
// Created by cugxy on 2020/8/16.
//
#include "tree/kd_tree.h"
#include <vector>
#include <iostream>

using std::vector;
using std::cout;
using std::endl;
using cugxy::KDNode;
using cugxy::KDTree;

int main(int argc, char **argv)
{
//    6 2
//    2 3
//    5 4
//    9 6
//    4 7
//    8 1
//    7 2
    vector<vector<int> > data;
    data.push_back(vector<int>{2,3});
    data.push_back(vector<int>{6,2});
    data.push_back(vector<int>{5,4});
    data.push_back(vector<int>{9,6});
    data.push_back(vector<int>{4,7});
    data.push_back(vector<int>{8,1});
    data.push_back(vector<int>{7,2});
    auto * pTree = new KDTree<int>(data, data[0].size());
    pTree->printTree();
    cout << endl;
    vector<int> vi{3,4};
    KDNode<int> * r = pTree->query(vi);
    // cout << r->val << endl;
    for (auto it = r->val.begin(); it != r->val.end(); ++it)
    {
        cout << *it << ' ';
    }
    cout << endl;
}