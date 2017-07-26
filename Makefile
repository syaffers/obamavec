clean:
	if [ -f "obama_vec.bin" ]; then\
		rm obama_vec.bin;\
	fi
	if [ -f "corpus.txt" ]; then\
		rm corpus.txt;\
	fi
	if [ -f "scrape.log" ]; then\
		rm scrape.log;\
	fi
	if [ -f "processed/speech0.txt" ]; then\
		rm processed/*.txt;\
	fi
	if [ -f "raw2/speech0.txt" ]; then\
		rm raw2/*.txt;\
	fi

scrape:
	node scrape_speeches.js >> scrape.log

corpus:
	sh clean_raw_files.sh
	cat processed/*.txt > corpus.txt
