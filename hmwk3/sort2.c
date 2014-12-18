#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>

void count_sort(int a[], int n) {
  int f,i, j,k, count;
  int *temp = malloc(n*sizeof(int));
  for(i=0; i<n;i++){
    temp[i]=0;
  }
    for (i=0; i<n; i++) {
      count = 0;
#     pragma omp parallel for num_threads(1) default(none) private(j) shared(i,count,a, n, temp)
      for (j = 0; j < n; j++) {
	if (a[j] < a[i]) {
	  count++;
	} else if (a[j] == a[i] && j < i) {
	  count++;
	}
      }
      temp[count] = a[i];
    }

# pragma omp parallel for num_threads(1) default(none) private(f) shared(a, n, temp)
    for (f=0; f<n; f++){
      a[f]=temp[f];
    }

  free(temp);
}
int main() {
  int n=100000;
  int i;
  int list_to_sort[n];
  for (i=0; i<n; i++){
    list_to_sort[i] = rand();
  }
  double start = omp_get_wtime();
  count_sort(list_to_sort, n);
  double end = omp_get_wtime();
  double diff = end-start;
  printf("elapsed process CPU time = %f seconds\n", diff);
  //  printf("%d ", list_to_sort[0]);
  //printf("%d ", list_to_sort[1]);

}
