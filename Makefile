# LinuxForHealth core Makefile

FROZEN_REQUIREMENTS = frozen-requirements.txt
VIRTUAL_ENVIRONMENT_DIR = venv

# executes tests for a LinuxForHealth core component
# arguments:
# $1 - the component name (aligns with top level directory)
define execute_tests
	cd $(1) && \
	source $(VIRTUAL_ENVIRONMENT_DIR)/bin/activate && \
	python3 -m pytest
endef

# removes the components virtual environment
# arguments:
# $1 - the component name (aligns with top level directory)
define clean_venv
	rm -rf $(1)/$(FROZEN_REQUIREMENTS) $(1)/$(VIRTUAL_ENVIRONMENT_DIR)
endef


# builds the component's virtual environment
# existing virtual environments and "frozen" requirements are reused if available
# arguments:
# $1 - the component name (aligns with top level directory)
# $2 - the setup.cfg build "extra" group to include. Example: "all" or "dev"
define build_component_venv
	if [ ! -d "./$(1)/$(VIRTUAL_ENVIRONMENT_DIR)" ]; then \
		python3 -m venv $(1)/$(VIRTUAL_ENVIRONMENT_DIR); \
		$(1)/$(VIRTUAL_ENVIRONMENT_DIR)/bin/python3 -m pip install --upgrade pip setuptools; \
	fi

	if [ -f "./$(1)/$(FROZEN_REQUIREMENTS)" ]; then \
		$(1)/$(VIRTUAL_ENVIRONMENT_DIR)/bin/python3 -m pip install -r "./$(1)/$(FROZEN_REQUIREMENTS)"; \
	fi

	cd $(1) && $(VIRTUAL_ENVIRONMENT_DIR)/bin/python3 -m pip install -e ".[$(2)]";

	if [ ! -f "./$(1)/$(FROZEN_REQUIREMENTS)" ]; then \
		$(1)/$(VIRTUAL_ENVIRONMENT_DIR)/bin/python3 -m pip freeze > $(1)/$(FROZEN_REQUIREMENTS); \
	fi
endef

all: connect-venv

clean-connect-venv:
	$(call clean_venv,connect)

connect-venv:
	$(call build_component_venv,connect,all)

activate-connect-venv:
	$(call activate_venv,connect)

connect-dev-venv:
	$(call build_component_venv,connect,dev)

connect-test:
	$(call execute_tests,connect)


.PHONY: clean-connect-venv, connect-venv, connect-dev-venv, connect-test