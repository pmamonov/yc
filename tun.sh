#!/bin/sh
while true; do
	date
	ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=1	\
		-N -R 2222:localhost:22				\
		-o "StrictHostKeyChecking no"			\
		$(python yc.py)
	sleep 60
done
