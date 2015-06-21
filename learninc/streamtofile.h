#include <stdio.h>
#include <string.h>

typedef struct nvpairtag {
  char* name;
  char* type;
  void* data;
  int databytecount;
}nvpair;

void constructStream(int size, char* outfilename);
void deconstructStream();
void queue(void* toqueue, int bytecount, FILE* fp);
