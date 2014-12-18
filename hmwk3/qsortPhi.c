#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>

#define BILLION 1000000000L


int cmpfunc (const void * a, const void * b)
{
  return ( *(int*)a - *(int*)b );
}

int main()
{
  int n=100000;
  int i;
  int values[n];

  for (i=0; i<n; i++){
    values[i] = rand();
  }


  double start = omp_get_wtime();
  qsort(values, n, sizeof(int), cmpfunc);
  double end = omp_get_wtime();
  double diff = end-start;
  printf("elapsed process CPU time = %f seconds\n", diff);
  
  return(0);
}
