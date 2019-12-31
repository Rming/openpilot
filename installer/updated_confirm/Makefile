CC = clang
CXX = clang++

PHONELIBS = ../../phonelibs

WARN_FLAGS = -Werror=implicit-function-declaration \
             -Werror=incompatible-pointer-types \
             -Werror=int-conversion \
             -Werror=return-type \
             -Werror=format-extra-args

CFLAGS = -std=gnu11 -g -fPIC -O2 $(WARN_FLAGS)
CXXFLAGS = -std=c++11 -g -fPIC -O2 $(WARN_FLAGS)


BORINGSSL_FLAGS = -I$(PHONELIBS)/boringssl/include
BORINGSSL_LIBS = $(PHONELIBS)/boringssl/lib/libssl_static.a \
                 $(PHONELIBS)/boringssl/lib/libcrypto_static.a \

NANOVG_FLAGS = -I$(PHONELIBS)/nanovg

OPENGL_LIBS = -lGLESv3

FRAMEBUFFER_LIBS = -lutils -lgui -lEGL

.PHONY: all
all: updated_confirm

OBJS = ../../selfdrive/common/touch.o \
       ../../selfdrive/common/framebuffer.o \
       $(PHONELIBS)/nanovg/nanovg.o

DEPS := $(OBJS:.o=.d)

updated_confirm: updated_confirm.o $(OBJS)
	@echo "[ LINK ] $@"
	$(CXX) $(CPPFLAGS) -fPIC -o 'updated_confirm' $^ \
    $(FRAMEBUFFER_LIBS) \
    $(BORINGSSL_LIBS) \
    -L/system/vendor/lib64 \
    $(OPENGL_LIBS) \
    -lcutils -lm -llog
	strip updated_confirm


%.o: %.c
	mkdir -p $(@D)
	@echo "[ CC ] $@"
	$(CC) $(CPPFLAGS) $(CFLAGS) \
          -I../.. \
          -I$(PHONELIBS)/android_frameworks_native/include \
          -I$(PHONELIBS)/android_system_core/include \
          -I$(PHONELIBS)/android_hardware_libhardware/include \
          $(NANOVG_FLAGS) \
          -c -o '$@' '$<'

%.o: %.cc
	mkdir -p $(@D)
	@echo "[ CXX ] $@"
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) \
           -I../../selfdrive \
           -I../../ \
           -I$(PHONELIBS)/android_frameworks_native/include \
           -I$(PHONELIBS)/android_system_core/include \
           -I$(PHONELIBS)/android_hardware_libhardware/include \
           $(NANOVG_FLAGS) \
           $(BORINGSSL_FLAGS) \
           -c -o '$@' '$<'


.PHONY: clean
clean:
	rm -f $(OBJS) $(DEPS)

-include $(DEPS)
