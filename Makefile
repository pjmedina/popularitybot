.PHONY: all
all: webapp worker

.PHONY: delete
delete: delete-webapp delete-worker

.PHONY: webapp
webapp:
	$(MAKE) -C webapp all

.PHONY: worker
worker:
	$(MAKE) -C worker all

.PHONY: delete-webapp
delete-webapp:
	$(MAKE) -C webapp delete

.PHONY: delete-worker
delete-worker:
	$(MAKE) -C worker delete
