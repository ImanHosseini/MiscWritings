
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdio.h>
#include <math.h>
#include <curand.h>
#include <curand_kernel.h>


cudaError_t addWithCuda(int *c, const int *a, const int *b, unsigned int size);

__global__ void addKernel(int *c, const int *a, const int *b)
{
    int i = threadIdx.x;
    c[i] = a[i] + b[i];
}

#define EXPCNT 100000
#define N 5
#define DENOM 623360743125120
#define KNS 256
#define WARP 32


__global__ void setup_kernel(curandState* state) {

    int idx = threadIdx.x + blockDim.x * blockIdx.x;
    curand_init(idx, idx, 0, &state[idx]);
}

__device__ void swap(int* arr,int i, int j) {
    int tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
}

__device__ int analysis(int* arr) {
    int stack[5][5] = { 0 };
    int maxi[5] = { -1,-1,-1,-1,-1 };
    for (int i = 0; i < 5; i++) {
        for (int idx = i * 5; idx < i * 5 + 5; idx++) {
            stack[arr[idx] / 5][i] += 1;
        }
    }
  
    int mi = -1;
    for (int i = 0; i < 5; i++) {
        int twoz = 0;
        bool broke = false;
        for (int j = 0; j < 5; j++) {
            int v = stack[i][j];
            if (v > 2) {
                if (maxi[j] == -1) {
                    maxi[j] = 1;
                    broke = true;
                    break;
                }
                else {
                    return 0;
                }
            }
            else {
                if (v == 2) {
                    //printf("TWO\n");
                    if (twoz == 1) {
                        return 0;
                    }
                    else {
                        mi = j;
                        twoz += 1;
                    }
                }
            }
        }
        if (!broke) {
            if (twoz == 1) {
                if (maxi[mi] == -1) {
                    maxi[mi] = 1;
                }
                else {
                    return 0;
                }
            }
            else {
                return 0;
            }
            
        }
    }
    return 1;
}

__global__ void expKernel(long long *acc, curandState* my_curandstate) {
    int idx = threadIdx.x + blockDim.x * blockIdx.x;

    for (int i = 0; i < EXPCNT; i++) {
        int conf[25] = { 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 };
        for (int js = 0; js < 25; js++) {
            float myrandf = curand_uniform(&(my_curandstate[idx]));
            int myrand = ceilf(myrandf * 24);
            //printf("%d\n", myrand);
            swap(conf, js, myrand);
        }
        int a = analysis(conf);
        // printf("%d\n", a);
        acc[idx] += a;
    }
    
    /*printf("idx:%d: %d\n", idx,myrand);*/
}

int main()
{
    const int arraySize = 5;
    const int a[arraySize] = { 1, 2, 3, 4, 5 };
    const int b[arraySize] = { 10, 20, 30, 40, 50 };
    int c[arraySize] = { 0 };
    long long acc[KNS*WARP] = { 0 };
    long long* acc_d;
    cudaMalloc(&acc_d, sizeof(long long) * KNS * WARP);
    cudaMemcpy(acc_d, acc, sizeof(long long) * KNS * WARP, cudaMemcpyHostToDevice);

    curandState* d_state;
    cudaMalloc(&d_state, sizeof(curandState)*KNS);
   
    setup_kernel << <WARP, KNS >> > (d_state);
    expKernel <<< WARP, KNS >>> (acc_d,d_state);
    cudaDeviceSynchronize();
    cudaMemcpy(acc, acc_d, sizeof(long long) * KNS * WARP, cudaMemcpyDeviceToHost);
    long long summ = 0;
    for (auto i = 0; i < KNS * WARP; i++) {
        // printf("%ld | ", acc[i]);
        summ += acc[i];
    }
    printf("%ld : %ld\n", summ, WARP*KNS*EXPCNT);
    // cudaDeviceReset must be called before exiting in order for profiling and
    // tracing tools such as Nsight and Visual Profiler to show complete traces.
    auto cudaStatus = cudaDeviceReset();
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaDeviceReset failed!");
        return 1;
    }

    return 0;
}


