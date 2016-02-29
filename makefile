#for opencv project
PROJECT_TOP_DIR=$(shell pwd)
PROJECT_BIN_DIR=$(PROJECT_TOP_DIR)
PROJECT_SRC_DIR=$(PROJECT_TOP_DIR)
PROJECT_INC_DIR=$(PROJECT_TOP_DIR)
PROJECT_LIB_DIR=$(PROJECT_TOP_DIR)
PROJECT_OBJ_DIR=$(PROJECT_BIN_DIR)
#MKDIR := mkdir -p $(PROJECT_TOP_DIR)/bin

CC := g++
#TARGET is the name of the exec file
TARGETS = elf
CFLAGS := -g -I$(PROJECT_INC_DIR)
#LDFLAG is the path where libfiles locates
LDFLAG := -L$(PROJECT_LIB_DIR)
#use pkg-config to generate gcc parametres
CFLAGS := $(shell pkg-config --libs --cflags opencv) 

ifeq "$(origin src)" "undefined"
	src :=$(wildcard $(PROJECT_SRC_DIR)/*.cpp)
endif
dir := $(notdir $(src))
PROJECT_OBJ := $(patsubst %.cpp,%.o,$(dir) )
PROJECT_ALL_OBJS := $(addprefix $(PROJECT_OBJ_DIR)/, $(PROJECT_OBJ))

all:$(PROJECT_SRC_DIR) $(PROJECT_ALL_OBJS)
	$(CC) $(CFLAGS) $(PROJECT_ALL_OBJS) -o $(PROJECT_BIN_DIR)/$(TARGETS) $(LDFLAG)
	exec $(TARGETS)

$(PROJECT_OBJ_DIR)/%.o : $(PROJECT_SRC_DIR)/%.cpp
	#$(MKDIR) $(PROJECT_OBJ_DIR)
	$(CC) -c $(CFLAGS) $< -o $@

.PHONY: clean
clean:
#	rm -fr $(PROJECT_OBJ_DIR)
	rm -fr $(TARGETS)
	rm -fr $(wildcard $(PROJECT_OBJ_DIR)/*.o)

