#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "streamtofile.h"

int getValue(nvpair* readpair, FILE* fpinput)
{

  int x = 0;
  int sizeread;
  sizeread = fread(&x, 1, sizeof(int), fpinput);
  if(sizeread == 0)
  {
    return -1;
  }
  
  (*readpair).name = malloc(sizeof(char) * (x));

  sizeread = fread((*readpair).name, x, sizeof(char), fpinput);

  sizeread = fread(&x, 1, sizeof(int), fpinput);

  (*readpair).type = malloc(sizeof(char) * x);

  printf("\n");
  printf((*readpair).name);
  printf("\n");
  printf((*readpair).type);
  printf("\n");

  sizeread = fread((*readpair).type, x, sizeof(char), fpinput);

  (*readpair).databytecount = 4;

  sizeread = fread(&(*readpair).databytecount, 1, sizeof(int), fpinput);

  (*readpair).data = malloc((*readpair).databytecount);

  sizeread = fread((*readpair).data, (*readpair).databytecount, sizeof(unsigned char), fpinput);

  return 1;
}

int getpairset(nvpair** apairset, int* pairsetcount, FILE* afile, char** name)
{
  int sizeread;
  int namelen = 0;
  sizeread = fread(&namelen, 1, sizeof(int), afile);

  *name = malloc(sizeof(char) * namelen);

  sizeread = fread(*name, namelen, sizeof(char), afile);

  sizeread = fread(pairsetcount, 1, sizeof(int), afile);
  if(sizeread == 0){return -1;}

  *apairset = malloc(sizeof(nvpair)* (*pairsetcount));
 
  int i;
  int res;
  printf("C:%d", *pairsetcount);
  for(i = 0; i < *pairsetcount; i++)
  {
    printf("?:%d", i);
    res = getValue(((*apairset) + i), afile);
    if(res == -1)
    {
      printf("x");
      free(*apairset);
      return -1;
    }
  }  
  return 1;
}

void freepairset(nvpair* apairset, int pairsetcount, char* name){
  int i;
  for(i = 0; i < pairsetcount; i++){
    free((*(apairset+i)).name);
    free((*(apairset+i)).data);
  }
  free(apairset);
  free(name);
}

float diff(void* done, int donec, void* dtwo, int dtwoc){
  int max = fmax(donec, dtwoc);
  int min = fmin(donec, dtwoc);
  if(max == 0){return 0.0f;}
  float inc = 1/((float)max);
  float v = (max - min)*inc;

  int i;
  for(i = 0; i < min; i++){
    unsigned char cone = *(unsigned char*)(done+i);
    unsigned char ctwo = *(unsigned char*)(dtwo+i);
    if(cone != ctwo){
      v += inc;
    }
  }
  if(v < inc){
    return 0;
  }
  return v;
}

void comparepairsets(nvpair* one, int onec, nvpair* two, int twoc, FILE* fp)
{
  int diffcount = 0;
  int oneonlycount = 0;
  int twoonlycount = 0;

  int usedtwoscount = 0;

  int i , j;
  for(i = 0; i < onec; i++){
    int found = 0;
    for(j = 0; j < twoc; j++){
      int rc = strcmp((*(one+i)).name, (*(two+j)).name);
      if(rc == 0){
        float diffval = diff(
          (*(one+i)).data, 
          (*(one+i)).databytecount,
          (*(two+j)).data,
          (*(two+j)).databytecount);
        if(diffval > 0){
          diffcount++;
        }
        usedtwoscount++;
        found = 1;
        break;
      }
    }
    if(!found){oneonlycount++;}
  }
  twoonlycount = twoc - usedtwoscount;
 
  fprintf(fp, "%d,%d,%d\n",diffcount,oneonlycount,twoonlycount);
}

void parseppfile(char* inputfile, char* outputfile)
{
  FILE* finput;
  FILE* foutput;
  
  printf("?");
  fflush(stdout);
  finput = fopen(inputfile, "r");
  foutput = fopen(outputfile, "w");

  int res = 1;

  char* name;
  nvpair* apair;
  int paircount;

  char* prevname;
  nvpair* previouspair;
  int prevpaircount;

  res = getpairset(&previouspair, &prevpaircount, finput, &prevname);
  if(res == -1){
    printf("first set empty");
    return;
  }
  fflush(stdout);
  while(1)
  {
    printf("1:%d\n", prevpaircount);
    fflush(stdout);
    res = getpairset(&apair, &paircount, finput, &name);
    printf("2:%d\n", paircount);
    fflush(stdout);
    if(res == -1){break;}
    printf("2.5:\n");
    comparepairsets(previouspair, prevpaircount, apair, paircount, foutput);

    printf("3\n");
    fflush(stdout);
    freepairset(previouspair, prevpaircount, prevname);

    printf("4\n");
    fflush(stdout);
    previouspair = apair;
    prevpaircount = paircount;
    prevname = name;
 
  }
  freepairset(previouspair, prevpaircount, prevname);

  fclose(finput);
  fclose(foutput);
}
