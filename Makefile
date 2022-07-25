# LinuxForHealth HealthOS build file

# target modules default to "all" modules
# to specify one or more modules execute the following in the shell
# export TARGET_MODULE=core support
# (multiple modules are separated by spaces)
# make <target>

ifdef TARGET_MODULES
	TARGET_MODULES := $(TARGET_MODULES)
else
	TARGET_MODULES := core
endif

# executes tests for each module
define test_module
	cd $(1) && poetry run pytest && cd ../;
endef

# format code
define format_module
	cd $(1) && poetry run black ./src ./tests && poetry run isort . && cd ../;
endef

# removes python bytecode and the virtual environment
define clean_module
	-cd $(1) && pyclean . && poetry env remove 3.10 > /dev/null && cd ../;
endef

# install all dependencies, including "dev" dependencies
define install_dev_dependencies
	cd $(1) && poetry install && cd ../;
endef

# installs dependencies, omitting "dev" dependencies
define install_dependencies_omit_dev
	cd $(1) && poetry install --no-dev && cd ../;
endef

# build wheel distributions
define build_wheel
	cd $(1) && poetry build -f wheel && cd ../;
endef

# removes wheels
define remove_wheel
	cd $(1) && rm -rf dist/ && cd ../;
endef

wheels:
	$(foreach module,$(TARGET_MODULES), $(call install_dependencies_omit_dev,$(module)))
	$(foreach module,$(TARGET_MODULES), $(call build_wheel,$(module)))
.PHONY: wheels

test:
	$(foreach module,$(TARGET_MODULES), $(call test_module, $(module)))
.PHONY: test

format:
	$(foreach module,$(TARGET_MODULES), $(call format_module,$(module)))
.PHONY: format

dev-env: clean
	$(foreach module,$(TARGET_MODULES), $(call install_dev_dependencies,$(module)))
.PHONY: dev-env

clean:
	$(foreach module,$(TARGET_MODULES), $(call clean_module,$(module)))
	$(foreach module,$(TARGET_MODULES), $(call remove_wheel,$(module)))
.PHONY: clean
