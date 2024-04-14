#include<stdio.h>
#include<pthread.h>
void *hello(void* arg) {
  printf("%s\n", (char*)arg);
  return NULL;
}

int main() {
  pthread_t tid;
  pthread_create(&tid, NULL, hello,(void*) "hello world");
  pthread_join(tid, NULL);
  return 0;
}
