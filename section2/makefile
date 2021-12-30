.PHONY:	default all all_plots plot table clean 

default:	thin gpu

thin:	
	./scripts/make_csv data_thin

gpu:
	./scripts/make_csv data_gpu

clean_csv:	
	./scripts/clean_csv
	
all_plots:	clean_csv plots_by_level plots_by_framework plot

plots_by_level:
	if [ ! -d results/plots_by_level ];then mkdir results/plots_by_level;fi
	python3 scripts/plots_by_level/plot_thin_node.py
	python3 scripts/plots_by_level/plot_thin_socket.py
	python3 scripts/plots_by_level/plot_thin_core.py
	python3 scripts/plots_by_level/plot_gpu_node.py
	python3 scripts/plots_by_level/plot_gpu_socket.py
	python3 scripts/plots_by_level/plot_gpu_core.py

plots_by_framework:
	if [ ! -d results/plots_by_framework ];then mkdir results/plots_by_framework;fi
	python3 scripts/plots_by_framework/plot_thin_intel.py
	python3 scripts/plots_by_framework/plot_thin_ucx.py
	python3 scripts/plots_by_framework/plot_thin_tcp.py
	python3 scripts/plots_by_framework/plot_thin_vader.py
	python3 scripts/plots_by_framework/plot_gpu_intel.py
	python3 scripts/plots_by_framework/plot_gpu_ucx.py
	python3 scripts/plots_by_framework/plot_gpu_tcp.py
	python3 scripts/plots_by_framework/plot_gpu_vader.py

plot:
	python3 scripts/make_plot.py
	

table:
	./scripts/make_table
	python3 scripts/make_table.py
	rm -f results/tmp_table.csv

clean:
	rm -rf clean
