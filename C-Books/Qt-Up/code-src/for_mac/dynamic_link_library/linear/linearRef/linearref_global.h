#ifndef LINEARREF_GLOBAL_H
#define LINEARREF_GLOBAL_H

#include <QtCore/qglobal.h>

#if defined(LINEARREF_LIBRARY)
#  define LINEARREFSHARED_EXPORT Q_DECL_EXPORT
#else
#  define LINEARREFSHARED_EXPORT Q_DECL_IMPORT
#endif

#endif // LINEARREF_GLOBAL_H
