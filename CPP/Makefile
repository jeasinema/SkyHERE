CXXFLAGS := $(shell pkg-config --cflags --libs opencv)
CXX := g++

all: main cv_chase vector

.PHONY:main
main: main.cpp
	$(CXX) $< $(CXXFLAGS) -o $@

SRC := $(shell find catchtest/*.cpp)
INC := ./catchtest


.PHONY:cv_chase
cv_chase: ./cv_chase.cpp
	$(CXX) $(SRC) -I $(INC) $(CXXFLAGS) -c
	$(CXX) $< $(patsubst %cpp, %o, $(notdir $(wildcard ./catchtest/*.cpp))) -I $(INC) $(CXXFLAGS) -o $@
	rm *.o

vector: ./vector.cpp
	$(CXX) $(SRC) -I $(INC) $(CXXFLAGS) -c
	$(CXX) $< $(patsubst %cpp, %o, $(notdir $(wildcard ./catchtest/*.cpp))) -I $(INC) $(CXXFLAGS) -o $@
	rm *.o

.PHONY:clean
clean:
	rm main cv_chase vector
