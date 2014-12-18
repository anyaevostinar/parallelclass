#ifdef _POMP
#  undef _POMP
#endif
#define _POMP 200110

#include "sort1.c.opari.inc"
#line 1 "sort1.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void count_sort(int a[], int n) {
  int i, j,k, count;
  printf("got to check 1");
  int *temp = malloc(n*sizeof(int));
  for(i=0; i<n;i++){
    temp[i]=0;
  }
  printf("check 2");
  printf("check 3");
POMP_Parallel_fork(&omp_rd_78);
#line 16 "sort1.c"
# pragma omp parallel     num_threads(1) default(none) private(i,j,count) shared(a, n, temp)
{ POMP_Parallel_begin(&omp_rd_78);
POMP_For_enter(&omp_rd_78);
#line 16 "sort1.c"
# pragma omp          for                                                                    nowait
    for (i=0; i<n; i++) {
      printf("check 4");
      count = 0;
      for (j = 0; j < n; j++) {
	if (a[j] < a[i]) {
	  count++;
	} else if (a[j] == a[i] && j < i) {
	  count++;
	}
      }
      temp[count] = a[i];
    }
POMP_Barrier_enter(&omp_rd_78);
#pragma omp barrier
POMP_Barrier_exit(&omp_rd_78);
POMP_For_exit(&omp_rd_78);
POMP_Parallel_end(&omp_rd_78); }
POMP_Parallel_join(&omp_rd_78);
#line 29 "sort1.c"
  memcpy(a, temp, n*sizeof(int));
  free(temp);
}
int main() {
  printf("check 0");
  int list_to_sort[5] = {1000, 2, 3, 7, 50};
  count_sort(list_to_sort, 5);
  printf("%d", list_to_sort[0]);
  printf("%d", list_to_sort[1]);
  printf("%d\n", list_to_sort[2]);

}
