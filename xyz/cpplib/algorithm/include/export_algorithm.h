//
// Created by cugxy on 2020/8/15.
//

#ifndef CPPLIB_EXPORT_ALGORITHM_H
#define CPPLIB_EXPORT_ALGORITHM_H

#if defined(ALGORITHM_LIBRARY)
#define ALGORITHM_LIBRARY_EXPORT __declspec(dllexport)
#else
#define ALGORITHM_LIBRARY_EXPORT __declspec(dllimport)
# endif

#endif //CPPLIB_EXPORT_ALGORITHM_H
