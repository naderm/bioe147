/* Copyright (c) 2013, Nader Morshed
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef int bool;
#define TRUE 1
#define FALSE 0
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

size_t m;
int frag_size;

/* Flip the elements of lst in place between the left and right indices and
   negate their values
*/
void flip(int *lst, int left, int right) {
  while (left < right) {
	int tmp = -lst[left];
	lst[left] = -lst[right - 1];
	lst[right - 1] = tmp;
	left++;
	right--;
  }
}

/* Returns a random integer, a <= int <= b */
int randint(int a, int b) {
  return a + rand() / (RAND_MAX / ((b - a) + 1) + 1);
}

/* Randomly pick a segment within lst to flip in place. This segment may have a
   length of zero, in which case, nothing happens.
*/
void rand_flip(int *lst) {
  int left, right;
  left = randint(0, m);

  if (frag_size == 0)
	right = randint(0, m);
  else
	right = randint(MAX(0, left - frag_size), MIN(m, left + frag_size));

  if (left > right) {
	int tmp = left;
	left = right;
	right = left;
  }

  flip(lst, left, right);
}

/* Shuffles and randomly negates the values of lst in place.
 */
void shuffle_and_flip(int *lst) {
  for (size_t i = 0; i < m; i++) {
	size_t j = i + rand() / (RAND_MAX / (m - i) + 1);
	int tmp = lst[i];
	lst[i] = lst[j];
	lst[j] = tmp;

	if (rand() % 2 == 1)
	  lst[i] = -lst[i];
  }
}

/* Compile on linux with: gcc -std=c99 -O2 flipper.c -o flipper */
int main(int argc, char **argv) {
  size_t particle_count;
  int *particles, *start;

  if (argc != 4) {
	printf("Usage: flipper [m] [distance] [particles]\n");
	printf("    m: Number of edges in graph\n");
	printf("    distance: Max number of fragments that can be flipped by\n");
	printf("              a recombinase. If 0, no limit to fragment size.\n");
	printf("    particles: Number of samples to run (Ideally > 2^m * m!)\n");
	printf("\n");
	printf("Remember, this program uses 4 * particles * m bytes of memory\n");
	printf("\n");
	exit(1);
  }

  m = atoi(argv[1]);
  frag_size = atoi(argv[2]);
  particle_count = atoi(argv[3]);

  srand(time(NULL));

  particles = malloc(particle_count * m * sizeof(int));
  start = malloc(m * sizeof(int));

  if (particles == NULL || start == NULL) {
	fprintf(stderr, "Error: Unable to allocate memory for particles!\n");
	exit(1);
  }

  for (size_t j = 0; j < m; j++)
	start[j] = j + 1;

  shuffle_and_flip(start);

  /* Copy the starting particle over every sample */
  for (size_t i = 0; i < particle_count; i++)
	memcpy(particles + i * m, start, m * sizeof(int));

  free(start);

  /* Repeatedly sample the problem space */
  for (size_t iter = 1; iter < 100; iter++) {
	size_t count = 0;

	printf("Iteration %u ... ", iter);

	for (size_t i = 0; i < particle_count; i++) {
	  bool correct = TRUE;
	  int *particle = particles + i * m;

	  /* Randomly flip the particle in place */
	  rand_flip(particle);

	  for (size_t j = 0; j < m; j++) {
		if (particle[j] != j + 1) {
		  correct = FALSE;
		  break;
		}
	  }

	  if (correct)
		count++;
	}

	/* Count the number of particles in the correct configuration */
	printf("Ratio: %f %%\n", ((float) count) / particle_count * 100);
  }

  free(particles);

  return 0;
}
