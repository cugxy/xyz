//
// Created by cugxy on 2020/8/15.
//

#ifndef CPPLIB_EXPORT_DATASTRUCT_H
#define CPPLIB_EXPORT_DATASTRUCT_H

#if defined(DATA_STRUCT_LIBRARY)
#define DATA_STRUCT_LIBRARY_EXPORT __declspec(dllexport)
#else
#define DATA_STRUCT_LIBRARY_EXPORT __declspec(dllimport)
# endif

#endif //CPPLIB_EXPORT_DATASTRUCT_H
