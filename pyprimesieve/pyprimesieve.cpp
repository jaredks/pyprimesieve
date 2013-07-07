/*
  pyprimesieve: Many primes, very fast. Uses primesieve.
  Copyright: (c) 2013, Jared Suttles. All rights reserved.
  License: BSD, see LICENSE for details.
*/
#include <Python.h>
#include "../primesieve/src/PrimeSieve.h"
#include "../primesieve/src/PrimeSieveCallback.h"

class PrimePyList : public PrimeSieveCallback<uint64_t> {
public:
    PrimePyList(size_t pi, size_t* i) : list(PyList_New(pi)), pi(pi), i(i) {}
    void callback(uint64_t prime){
        if (*i < pi)
            PyList_SET_ITEM(list, (*i)++, PyInt_FromSize_t(prime));
        else {
            PyObject* pyprime = PyInt_FromSize_t(prime);
            PyList_Append(list, pyprime);
            Py_DECREF(pyprime);
        }
    }
    PyObject* list;
    size_t*   i;
    size_t    pi;
};

static PyObject* pyprimes_primes(PyObject* self, PyObject* args){
    Py_ssize_t start = 0, n = 0; size_t pi;
    if (!PyArg_ParseTuple(args, "n|n", &start, &n)) return NULL;
    if (PyTuple_Size(args) == 1){
        n = start;
        start = 0;
    }
    if (start > n) return PyList_New(0);
    if (start < 2) start = 2;
    if (n < 3) return PyErr_Occurred() ? NULL : PyList_New(0);
    else if (n == 3){
        PyObject* just_two = PyList_New(1);
        PyList_SET_ITEM(just_two, 0, PyInt_FromLong(2));
        return just_two;
    }
    else if (n < 6)  pi = 2;
    else if (n < 8)  pi = 3;
    else if (n < 12) pi = 4;
    else if (n < 14) pi = 5;
    else if (n < 18) pi = 6;
    else             pi = n/(log(n)-1);
    size_t i = 0;
    PrimePyList primes(pi, &i);
    PrimeSieve ps;
    ps.generatePrimes(start, n-1, &primes);
    i--;
    while (i < --pi) PyObject_CallMethod(primes.list, (char*)"__delitem__", (char*)"(n)", pi);
    return primes.list;
}

static PyObject* pyprimes_factorize(PyObject* self, PyObject* args){
    Py_ssize_t n = 0;
    if (!PyArg_ParseTuple(args, "n", &n)) return NULL;
    PyObject* prime_factorization = PyList_New(0);
    if (n < 2) return prime_factorization;
    size_t i = 0;
    while (!(n & 1)){
        n /= 2;
        i++;
    }
    if (i > 0){
        PyObject* tuple = PyTuple_Pack(2, PyInt_FromLong(2), PyInt_FromSsize_t(i));
        PyList_Append(prime_factorization, tuple);
        Py_DECREF(tuple);
    }
    size_t p = 3;
    while (p*p <= n){
        i = 0;
        while (n % p ==0){
            n /= p;
            i++;
        }
        if (i > 0){
            PyObject* tuple = PyTuple_Pack(2, PyInt_FromSsize_t(p), PyInt_FromSsize_t(i));
            PyList_Append(prime_factorization, tuple);
            Py_DECREF(tuple);
        }
        p += 2;
    }
    if (n > 1){
        PyObject* tuple = PyTuple_Pack(2, PyInt_FromSsize_t(n), PyInt_FromLong(1));
        PyList_Append(prime_factorization, tuple);
        Py_DECREF(tuple);
    }
    return prime_factorization;
}

static PyMethodDef module_methods[] = {
    {"primes", pyprimes_primes, METH_VARARGS, "List of prime numbers up to the given number."},
    {"factorize", pyprimes_factorize, METH_VARARGS, "List of tuples for the prime factorization of the given number."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_pyprimesieve(){
    Py_InitModule("_pyprimesieve", module_methods);
}
