.PHONY: run test eval stop

# The project lives in track_2b/ (the template's track directory); these
# targets forward to its Makefile, so `make run` works from either root.
run test eval stop:
	$(MAKE) -C track_2b $@
