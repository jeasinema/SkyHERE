CXXFLAGS := $(shell pkg-config --cflags --libs opencv)

all: main cv_chase

main: main.cpp
	g++ $< -o $@ $(CXXFLAGS)

SOURCES := $(shell find catchtest/*.cpp)
SOURCES += $(shell find catchtest/*.h)
cv_chase: $(SOURCES)
	g++ -o $@ $(SOURCES) $(CXXFLAGS)

clean:
	rm main cv_chase
