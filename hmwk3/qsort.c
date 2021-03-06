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
  int n=60000;
  int i;
  int values[n];
  struct timespec start, end;
  uint64_t diff;

  for (i=0; i<n; i++){
    values[i] = rand();
  }


  clock_gettime(CLOCK_MONOTONIC, &start);
  qsort(values, n, sizeof(int), cmpfunc);
  clock_gettime(CLOCK_MONOTONIC, &end);
  diff = BILLION * (end.tv_sec - start.tv_sec) + end.tv_nsec - start.tv_nsec;
  printf("elapsed process CPU time = %llu nanoseconds\n", (long long unsigned int) diff);
  
  return(0);
}
