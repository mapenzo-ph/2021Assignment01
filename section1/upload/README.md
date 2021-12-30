### Compilation

The files have been tested using both OpenMPI and Intel libraries. The results shown in the report are obtained using OpenMPI 4.1.1. 

To compile the source files:
- load the relevant module using  `module load openmpi-4.1.1`
- `cd` in the source directory
- `make`

By default matrix3Dsum.c is compiled so that it uses virtual topology for message passing. Since it does not provide any benefit in this specific case, it can be deactivated compiling with `-D NO_VIRTUAL_TOPOLOGY` . This can be done via the command `make sum3Dnvt` .

### Running the programs

To run the programs use

- `mpirun -np nproc ring nreps` 
- `mpirun -np nproc sum3Dmatrix size1 size2 size3 ndims dim_1 dim_2 ... dim_ndims` 

Input example for both programs are provided in `input_examples`. 
