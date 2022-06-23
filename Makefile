FROZEN_REQUIREMENTS = frozen-requirements.txt
VIRTUAL_ENVIRONMENT_DIR = venv

# removes the components virtual environment
# arguments:
# $1 - the component name (aligns with top level directory)
define clean_venv
	rm -rf $(1)/$(FROZEN_REQUIREMENTS) $(1)/$(VIRTUAL_ENVIRONMENT_DIR)
endef


# builds the component's virtual environment
# arguments:
# $1 - the component name (aligns with top level directory)
define build_component_venv
	cd $(1) && \
	python3 -m venv $(VIRTUAL_ENVIRONMENT_DIR) && \
	source $(VIRTUAL_ENVIRONMENT_DIR)/bin/activate && \
	python3 -m pip install --upgrade pip setuptools && \
	python3 -m pip install -e ".[$(2)]" && \
	python3 -m pip freeze > frozen-requirements.txt
endef

all: connect-venv

clean-connect-venv:
	$(call clean_venv,connect)

connect-venv: clean-connect-venv
	$(call build_component_venv,connect,all)

connect-dev-venv: clean-connect-venv
	$(call build_component_venv,connect,dev)


.PHONY: clean-connect-venv, connect-venv, connect-dev-venv