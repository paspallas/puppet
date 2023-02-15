RM  := rm -rf
RC  := pyrcc5
PY 	:= python

.PHONY:
run:
	@$(PY) src/main.py

.PHONY:
app:
	@pyinstaller --clean app.spec

.PHONY:
clean:
	@$(RM) __pycache__ *.ini

.PHONY:
distclean: clean
	@$(RM) dist build

.PHONY:
res:
	@$(RC) -no-compress src/app/resources/resources.qrc -o src/app/resources/resources.py 
