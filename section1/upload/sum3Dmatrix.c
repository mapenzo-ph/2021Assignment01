#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

void init_rand_matrix(double *matrix, const int layers, const int rows, const int cols) {
    /**
     * @brief Populate matrix block
     * Initialize matrix with random doubles
     * taken in interval [0,100]
    */

    int layer_size = rows * cols;
    double *layer_start;
    double *row_start;
    double inv_rmax = 100/(double)RAND_MAX;
   
    // init
    for (size_t k=0; k<layers; ++k){
        layer_start = matrix + k*layer_size;
        for (size_t i=0; i<rows; ++i){  // initialize matrix
            row_start = layer_start + i*cols;
            for (size_t j=0; j<cols; ++j){
                *(row_start+j) = rand()*inv_rmax;
            }
        }
    }
}




void print_matrix(double *matrix, const int layers, const int rows, const int cols) {
    /**
     * @brief Prints matrix in formatted way
    */

    int layer_size = rows*cols;   
    double *layer_start;
    double *row_start;

    for (size_t k=0; k<layers; ++k){    // loop on layers
        layer_start = matrix + k*layer_size;
        printf("* --- Layer: %zu -----\n\n", k);
        for (size_t i=0; i<rows; ++i){  // loop on rows and cols of a layer
            row_start = layer_start + i*cols;
            printf("\t|");
            for (size_t j=0; j<cols; ++j){
                printf(" %-8g ", *(row_start+j));
            }
            printf("|\n");
        }
        printf("\n");
    }
    printf("\n");
}




/*----- MAIN --------------------------------------------*/
int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);

    int rank, nproc; // get rank and size
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    MPI_Comm vtopo;

#ifdef NO_VIRTUAL_TOPOLOGY
    // if (rank == 0)
    // { // check program branch
    //     printf("Using MPI_COMM_WORLD\n");
    // }
    vtopo = MPI_COMM_WORLD;
#else
    // if (rank == 0)
    // { // check for program branch
    //     printf("Using virtual topology\n");
    // }

    // creating virtual topology
    const int ndims = 3;
    int dims[ndims];
    int qperiods[ndims];
    const int qreorder = 1;

    for (size_t k = 0; k < ndims; ++k)
    {
        dims[k] = atoi(argv[4+k]);  // get from argv
        qperiods[k] = 0;
    }

    // MPI_Dims_create(nproc, ndims, dims); // creating virtual topology
    MPI_Cart_create(MPI_COMM_WORLD, ndims, dims, qperiods, qreorder, &vtopo);
#endif

    // generate random matrices
    int layers, rows, cols, nelems, buff_size, nsend;
    double *first, *second, *result;
    double tstart, cstart, ttime, ctime;

    layers = atoi(argv[1]);
    rows = atoi(argv[2]);
    cols = atoi(argv[3]);
    nelems = layers*rows*cols;
    buff_size = nelems / nproc;
    nsend = buff_size * nproc;

    if (rank == 0) {    // allocate matrices in root process
        srand(time(NULL)); // init rng

        first = (double*)malloc(nelems*sizeof(double));
        init_rand_matrix(first, layers, rows, cols);
        // print_matrix(first, layers, rows, cols);

        second = (double*)malloc(nelems*sizeof(double));
        init_rand_matrix(second, layers, rows, cols);
        // print_matrix(second, layers, rows, cols);

        result = (double*)malloc(nelems*sizeof(double));

        printf("Total number of elements: %d\n", nelems);
        printf("Elements per process: %d\n", buff_size);
        printf("Remaining elements given to root process: %d\n", nelems-nsend);
    }

    MPI_Barrier(vtopo);  // synchronization    

    // define buffers for scatter/gather
    double *recv_1 = (double*)malloc(buff_size*sizeof(double));
    double *recv_2 = (double*)malloc(buff_size*sizeof(double));
    double *partial = (double*)malloc(buff_size*sizeof(double));

    tstart = MPI_Wtime(); // start total timer

    MPI_Scatter(first, buff_size, MPI_DOUBLE, recv_1, buff_size, MPI_DOUBLE, 0, vtopo);
    MPI_Scatter(second, buff_size, MPI_DOUBLE, recv_2, buff_size, MPI_DOUBLE, 0, vtopo);

    cstart = MPI_Wtime(); // start comp timer 

    for(size_t i=0; i<buff_size; ++i) { // performing parallel sum
        partial[i] = recv_1[i] + recv_2[i];
    }

    ctime = MPI_Wtime() - cstart; // stop comp timer

    MPI_Gather(partial, buff_size, MPI_DOUBLE, result, buff_size, MPI_DOUBLE, 0, vtopo);

    if (rank == 0) {    // sum remaining elements in root process   
        if (nsend != nelems) {
            for (size_t i=nsend; i<nelems; ++i) {
                result[i] = first[i] + second[i];
            }
        }
    }
    
    ttime = MPI_Wtime() - tstart; // stop total timer

    if (rank == 0) {    // finalize program
        printf("Total time: %lf\n", ttime);
        printf("Communication time: %lf\n", ttime-ctime);

        // print_matrix(result, layers, rows, cols);   // print to check

        free(first);    // free memory
        free(second);
        free(result);
    }

    MPI_Finalize();
    return 0;
}