CXXFLAGS := $(shell pkg-config --cflags --libs opencv)
CXX := g++

all: main cv_chase

.PHONY:main
main: main.cpp
	$(CXX) $< -o $@ $(CXXFLAGS)

SOURCES := $(shell find catchtest/*.cpp)
SOURCES += $(shell find catchtest/*.h)


.PHONY:cv_chase
cv_chase: ./catchtest/cv_chase.cpp
	$(CXX) $(SOURCES)  $(CXXFLAGS) -c
	$(CXX) $(CXXFLAGS) $(patsubst %.o, %.cpp, $(wildcard catchtest/*.cpp))  -o $@ 
	rm *.o

.PHONY:clean 
clean:
	rm main cv_chase 
