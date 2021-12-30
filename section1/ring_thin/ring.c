#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);

    const int nreps = 10000;    // number of repetitions

    // init rank and size
    int rank, nprocs;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Status status;

    // create ring with wirtual topology
    MPI_Comm ring_comm;
    int dims[1];
    dims[0] = nprocs;
    int period[1];
    period[0] = 1;

    MPI_Cart_create(MPI_COMM_WORLD, 1, dims, period, 1, &ring_comm);

    // get coordinates to send/rec
    int source, pneigh, nneigh;
    MPI_Cart_shift(ring_comm, 0, 1, &source, &pneigh);
    MPI_Cart_shift(ring_comm, 0, -1, &source, &nneigh);

    // declare buffers and tags
    int NPTAG = nprocs * 10;

    int psendbuf, precvbuf; // cw buffers
    int psendtag, precvtag; // cw tags

    int nsendbuf, nrecvbuf; // ccw buffers
    int nsendtag, nrecvtag; // ccw tags

    double elapsed;  // time measurements
    MPI_Barrier(ring_comm);
    elapsed = MPI_Wtime();
   
    for (size_t k=0; k<nreps; ++k) {
    
        precvbuf = 0;   // reinitialize c variables
        psendtag = rank * 10;
        precvtag = nneigh * 10;

        nrecvbuf = 0;   // reinitialize cc variables
        nsendtag = rank*10;
        nrecvtag = pneigh*10;

        // if (rank==0) {
        //     printf("Rep %d\n", k);
        // }

        for  (size_t i=0; i<nprocs; ++i) {  // main loop

            // send/recv clockwise
            psendbuf = precvbuf + rank;
            MPI_Sendrecv(&psendbuf, 1, MPI_INT, pneigh, psendtag, &precvbuf, 1, MPI_INT, nneigh, \
                            precvtag, ring_comm, &status);

            // printf("Proc %d sent to proc %d with tag %d and received from %d with tag %d \n",\
            //         rank, pneigh, psendtag, nneigh, precvtag);

            psendtag = precvtag;
            precvtag = (precvtag+NPTAG-10)%NPTAG;

            // send/recv counterclockwise
            nsendbuf = nrecvbuf - rank;
            MPI_Sendrecv(&nsendbuf, 1, MPI_INT, nneigh, nsendtag, &nrecvbuf, 1, MPI_INT, pneigh, \
                            nrecvtag, ring_comm, &status);

            nsendtag = nrecvtag;
            nrecvtag = (nrecvtag+10)%NPTAG;

            // printf("Proc %d sent to proc %d with tag %d and received from %d with tag %d \n",\
            //         rank, nneigh, nsendtag, pneigh, nrecvtag);
        }

    }

    MPI_Barrier(ring_comm);
    elapsed = MPI_Wtime() - elapsed;

    // if (nsendtag != psendtag){
    //     printf("Final tags are not the same!");
    //     return 44;
    // }

    printf("I am processor %d and my final messages are %d,%d with tag %d\n", rank, precvbuf, nrecvbuf, psendtag);

    if (rank == 0) {
        printf("\nAverage elapsed time: %lf\n", elapsed/nreps);
    }

    MPI_Finalize();
    return 0;
}