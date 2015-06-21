#include <stdio.h>

int main(int argc, char** argv){
  printf(argv[0]);
  printf("\n");
  fflush(stdout);
  printf(argv[1]);
  printf("\n");
  fflush(stdout);
  parseppfile(argv[1], argv[2]);
}
