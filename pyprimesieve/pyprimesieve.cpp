/*
  pyprimesieve: Many primes, very fast. Uses primesieve.
  Copyright: (c) 2013, Jared Suttles. All rights reserved.
  License: BSD, see LICENSE for details.
*/
#include <Python.h>
#include "../primesieve/src/PrimeSieve.h"
#include "../primesieve/src/PrimeSieveCallback.h"
#include "../primesieve/src/ParallelPrimeSieve.h"

const char* DOCSTRING =
"pyprimesieve: Many primes, very fast. Uses primesieve.\n"
"- - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n"
"primes(n): List of prime numbers up to `n`.\n\n"
"primes(start, n): List of prime numbers from `start` up to `n`.\n\n"
"primes_sum(n [, threads]): The summation of prime numbers up to `n`. If `threads` is given, that many threads will\n"
"be created. If not, the optimal number of threads will be determined.\n\n"
"primes_sum(start, n [, threads]): The summation of prime numbers from `start` up to `n`. If `threads` is given,\n"
"that many threads will be created. If not, the optimal number of threads will be determined.\n\n"
"primes_nth(n): The nth prime number.\n\n"
"factorize(n): List of tuples in the form of (*prime*, *power*) for the prime factorization of `n`.\n\n\n"
"Copyright: (c) 2013, Jared Suttles. All rights reserved.\n"
"License: BSD, see LICENSE for details.\n";


class PrimePyList : public PrimeSieveCallback<uint64_t> {
public:
    PrimePyList(size_t pi, size_t* i) : list(PyList_New(pi)), pi(pi), i(i) {}
    void callback(uint64_t prime){
        if (*i < pi){
            PyList_SET_ITEM(list, (*i)++, PyInt_FromSize_t(prime));
        } else {
            PyObject* pyprime = PyInt_FromSize_t(prime);
            PyList_Append(list, pyprime);
            Py_DECREF(pyprime);
        }
    }
    PyObject* list;
    size_t*   i;
    size_t    pi;
};

static PyObject* primes(PyObject* self, PyObject* args){
    Py_ssize_t start = 0, n = 0; size_t pi;
    if (!PyArg_ParseTuple(args, "n|n:primes", &start, &n)) return NULL;
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

static PyObject* factorize(PyObject* self, PyObject* args){
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
        PyObject* tuple = PyTuple_Pack(2, PyInt_FromLong(2), PyInt_FromSize_t(i));
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
            PyObject* tuple = PyTuple_Pack(2, PyInt_FromSize_t(p), PyInt_FromSize_t(i));
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

size_t sum = 0;

void summation(uint64_t prime){
    sum += prime;
}

static PyObject* primes_sum(PyObject* self, PyObject* args){
    PyEval_InitThreads();
    Py_ssize_t start = 0, n = 0; sum = 0;
    if (!PyArg_ParseTuple(args, "n|n:primes_sum", &start, &n)) return NULL;
    if (PyTuple_Size(args) == 1){
        n = start;
        start = 0;
    }
    if (n < 3 || start > n) return PyErr_Occurred() ? NULL : PyInt_FromLong(0);
    if (start < 2) start = 2;
    Py_BEGIN_ALLOW_THREADS  //----
    ParallelPrimeSieve pps;
    pps.setNumThreads(ParallelPrimeSieve::getMaxThreads());  // calls OpenMP's omp_get_max_threads
    pps.generatePrimes(start, n-1, summation);
    Py_END_ALLOW_THREADS    //----
    return PyInt_FromSize_t(sum);
}

class StopPrimeGeneration : public std::exception {};

class NthPrime : public PrimeSieveCallback<uint64_t> {
public:
    NthPrime(Py_ssize_t n) : n(n), i(0) {}
    void callback(uint64_t p){
        if (++i == n){
            prime = PyInt_FromSize_t(p);
            throw StopPrimeGeneration();
        }
    }
    PyObject* prime;
private:
    Py_ssize_t n;
    Py_ssize_t i;
};

static PyObject* primes_nth(PyObject* self, PyObject* args){
    Py_ssize_t n = 0;
    if (!PyArg_ParseTuple(args, "n:primes_nth", &n)) return NULL;
    if (n < 1){
        PyErr_SetString(PyExc_ValueError, "a positive integer is required");
        return NULL;
    }
    switch (n){
        case 1: return PyInt_FromLong(2);
        case 2: return PyInt_FromLong(3);
        case 3: return PyInt_FromLong(5);
        case 4: return PyInt_FromLong(7);
        case 5: return PyInt_FromLong(11);
    }
    NthPrime nthprime(n);
    PrimeSieve ps;
    try {
        ps.generatePrimes(0, n*log(n*log(n)), &nthprime);
    }
    catch (StopPrimeGeneration&) {}
    return nthprime.prime;
}

static PyMethodDef module_methods[] = {
    {"primes",     primes,     METH_VARARGS, "List of prime numbers up to the given number."},
    {"factorize",  factorize,  METH_VARARGS, "List of tuples for the prime factorization of the given number."},
    {"primes_sum", primes_sum, METH_VARARGS, "Summation of prime numbers up to the given number."},
    {"primes_nth", primes_nth, METH_VARARGS, "The Nth prime number."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initpyprimesieve(){
    Py_InitModule3("pyprimesieve", module_methods, DOCSTRING);
}
