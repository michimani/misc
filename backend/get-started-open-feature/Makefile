init:
	cd infra && make init && make apply
	cd client && make init

clean:
	cd infra && make clean
	cd client && uv clean

evaluate-feature:
	@cd client \
	&& make run ARGS="$(ARGS)"