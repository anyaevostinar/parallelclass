#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include <math.h>

void count_sort(int a[], int n) {
  int i, j,k, count;
  int *temp = malloc(n*sizeof(int));
# pragma omp parallel num_threads(2)
  {
# pragma omp for
    int *temp_private = malloc(n*sizeof(int));
    for (i=0; i<n; i++) {
      count = 0;
      for (j = 0; j < n; j++) {
	if (a[j] < a[i]) {
	  count++;
	} else if (a[j] == a[i] && j < i) {
	  count++;
	}
      }
      temp_private[count] = a[i];
    }
#   pragma omp critical
    {
      for(k=0; k<n; ++k){
	temp[k] += temp_private[k];
	printf("%d\n", temp_private[0]);
      }
    }
  }
  memcpy(a, temp, n*sizeof(int));
  free(temp);
}
int main() {
  int list_to_sort[5] = {1000, 2, 3, 7, 50};
  count_sort(list_to_sort, 5);
  printf("%d", list_to_sort[0]);
  printf("%d", list_to_sort[1]);
  printf("%d\n", list_to_sort[2]);

}
