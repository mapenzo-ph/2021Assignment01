THIN = jacobi_data_thin/results
GPU = jacobi_data_gpu/results
.PHONY:	default csv network_csv table plot data

csv:
	./scripts/make_csv $(THIN) $(GPU)

network_csv:
	./scripts/make_network_csv

table:
	python3 scripts/make_table.py

plot:	
	python3 scripts/make_plot.py

data:
	./scripts/make_clean_csv $(THIN) $(GPU)