#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "streamtofile.h"

#ifndef _BITSTREAM_
#define _BITSTREAM_
	#include "bitstream.h"
#endif

void queue(void* toqueue, int bytecount, FILE* fp)
{
  fwrite(toqueue, sizeof(unsigned char), bytecount, fp);
}

int getsizeof(nvpair apair)
{
  int ret = sizeof(int);
  ret += (strlen(apair.name) * sizeof(char));
  ret += apair.databytecount;
  return ret;
}


void writeValue(nvpair apair, FILE* fp)
{
  int slen = strlen(apair.name);

  void* v = &slen;

  queue(v, sizeof(int), fp);

  v = apair.name;

  queue(v, sizeof(char) * slen, fp);

  v = &apair.databytecount;

  queue(v, sizeof(int), fp);

  queue(apair.data, apair.databytecount, fp);
}

void writeState(nvpair state[], int arrlen, FILE* fp)
{
  queue(&arrlen, sizeof(int), fp);
  int i = 0; 
  for(i = 0; i < arrlen; i++)
  {
    writeValue(state[i], fp);
  }
}
