# LinuxForHealth HealthOS build file

# target modules default to "all" modules
# to specify one or more modules execute the following in the shell
# export TARGET_MODULE=core support
# (multiple modules are separated by spaces)
# make <target>

ifdef TARGET_MODULES
	TARGET_MODULES := $(TARGET_MODULES)
else
	TARGET_MODULES := core plugins sdk support
endif

# removes python bytecode and untracked dependencies for a module
define clean_module
	cd $(1) && pyclean . && poetry install --remove-untracked && cd ../;
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

wheels: clean
	$(foreach module,$(TARGET_MODULES), $(call install_dependencies_omit_dev,$(module)))
	$(foreach module,$(TARGET_MODULES), $(call build_wheel,$(module)))

clean:
	$(foreach module,$(TARGET_MODULES), $(call clean_module,$(module)))

dev_env: clean
	$(foreach module,$(TARGET_MODULES), $(call install_dependencies_omit_dev,$(module)))

.PHONY: clean dev_env wheels