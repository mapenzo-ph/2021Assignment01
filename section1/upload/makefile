CC = mpicc

SRC = ring.c sum3Dmatrix.c
NAMES = $(basename $(SRC))

.PHONY:	default all sum3Dnvt clean

default:	all

all:	$(NAMES)

%:	%.c
	$(CC) $(CFLAGS) $< -o $@ 

sum3Dnvt:	sum3Dmatrix.c
	$(CC) -D NO_VIRTUAL_TOPOLOGY $< -o sum3Dvt

clean:	
	rm -rf $(NAMES) sum3Dnvt
