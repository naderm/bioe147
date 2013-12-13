
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef int bool;
#define TRUE 1
#define FALSE 0

size_t M = 7;

void flip(int *lst, int left, int right) {
  while (left < right) {
	int tmp = -lst[left];
	lst[left] = -lst[right - 1];
	lst[right - 1] = tmp;
	left++;
	right--;
  }
}

void rand_flip(int *lst) {
  int left, right;
  left = rand() / (RAND_MAX / (M + 1) + 1);
  right = rand() % (M + 1);

  if (left > right) {
	int tmp = left;
	left = right;
	right = left;
  }

  flip(lst, left, right);
}

void shuffle_and_flip(int *lst) {
  for (size_t i = 0; i < M; i++) {
	size_t j = i + rand() / (RAND_MAX / (M - i) + 1);
	int tmp = lst[i];
	lst[i] = lst[j];
	lst[j] = tmp;

	if (rand() % 2 == 1)
	  lst[i] = -lst[i];
  }
}


int main() {
  size_t particle_count = 10000000;
  int *particles, *start;

  srand(time(NULL));

  particles = malloc(particle_count * M * sizeof(int));
  start = malloc(M * sizeof(int));

  for (size_t j = 0; j < M; j++) {
	start[j] = j + 1;
  }
  shuffle_and_flip(start);

  for (size_t i = 0; i < particle_count; i++) {
	memcpy(particles + i * M, start, M * sizeof(int));
	/* for (size_t j = 0; j < M; j++) { */
	/*   particles[i * M + j] = j + 1; */
	/* } */
	/* shuffle_and_flip(particles + i * M); */
  }

  free(start);

  for (size_t iter = 1; iter < 100; iter++) {
	size_t count = 0;

	printf("Iteration %u ... ", iter);

	for (size_t i = 0; i < particle_count; i++) {
	  bool correct = TRUE;

	  rand_flip(particles + i * M);

	  for (size_t j = 0; j < M; j++) {
		if (particles[i * M + j] != j + 1) {
		  correct = FALSE;
		  break;
		}
	  }

	  if (correct)
		count++;
	}

	printf("Ratio: %f %%\n", ((float) count) / particle_count * 100);
  }

  free(particles);

  return 0;
}
