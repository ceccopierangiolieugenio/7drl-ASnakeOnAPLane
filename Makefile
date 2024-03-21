testWeb:
	rm -rf tmp/*

	mkdir -p tmp/bin
	cp index.html -p tmp
	cp -a crap/*  tmp

	find 7drl/   -name "*.py" | sort | sed 's,7drl.,,' | xargs tar cvzf tmp/bin/7drl.tgz -C 7drl
	find TermTk/ -name "*.py" | sort | xargs tar cvzf tmp/bin/TermTk.tgz

	cd tmp; zip -r ../7drl.zip *; cd ..

	python3 -m http.server --directory tmp

