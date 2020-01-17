#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>

#include <unistd.h>
#include <math.h>
#include <sys/stat.h>
#include <sys/statvfs.h>

#include <string>
#include <sstream>
#include <fstream>
#include <mutex>
#include <thread>

#include <GLES3/gl3.h>
#include <EGL/egl.h>
#include <EGL/eglext.h>

#include "nanovg.h"
#define NANOVG_GLES3_IMPLEMENTATION
#include "nanovg_gl.h"
#include "nanovg_gl_utils.h"

#include "common/framebuffer.h"
#include "common/touch.h"
#include "common/utilpp.h"


namespace {


struct UpdatedConfirm {
  int count_down = 333;

  TouchState touch;

  int fb_w, fb_h;
  EGLDisplay display;
  EGLSurface surface;

  FramebufferState *fb = NULL;
  NVGcontext *vg = NULL;
  int font_regular;
  int font_bold;

  std::thread update_thread_handle;

  std::mutex lock;

  // i hate state machines give me coroutines already
  enum UpdateState {
    CONFIRMATION,
    ERROR,
  };
  UpdateState state;

  int count_num;
  std::string cancel_text;

  std::string error_text;

  // button
  int b_x, b_w, b_y, b_h;
  int balt_x;

  UpdatedConfirm() {
    touch_init(&touch);

    fb = framebuffer_init("updated_confirm", 0x00001000, false, &fb_w, &fb_h);
    assert(fb);

    vg = nvgCreateGLES3(NVG_ANTIALIAS | NVG_STENCIL_STROKES | NVG_DEBUG);
    assert(vg);

    font_regular = nvgCreateFont(vg, "miui_regular", "/system/fonts/Miui-Regular.ttf");
    assert(font_regular >= 0);

    font_bold = nvgCreateFont(vg, "miui_bold", "/system/fonts/Miui-Bold.ttf");
    assert(font_bold >= 0);


    b_w = 640;
    balt_x = 200;
    b_x = fb_w-b_w-200;
    b_y = 720;
    b_h = 220;

    state = CONFIRMATION;

  }


  void set_error(std::string text) {
    std::lock_guard<std::mutex> guard(lock);
    error_text = text;
    state = ERROR;
  }

  void set_confirmation() {
    std::lock_guard<std::mutex> guard(lock);
    state = CONFIRMATION;
  }

  void run_stages() {
    // //clean and rebuild
    // printf("git reset --hard\n");
    // system("git -C /data/openpilot reset --hard @{u}");


    // //clean and rebuild
    // printf("git clean -xdf\n");
    // system("git -C /data/openpilot clean -xdf ");

    exit(0);
  }

  void draw_ack_screen(const char *title, const char *message, const char *button, const char *altbutton) {
    nvgFillColor(vg, nvgRGBA(255,255,255,255));
    nvgTextAlign(vg, NVG_ALIGN_CENTER | NVG_ALIGN_BASELINE);

    nvgFontFace(vg, "miui_bold");
    nvgFontSize(vg, 120.0f);
    nvgTextBox(vg, 110, 220, fb_w-240, title, NULL);

    nvgTextAlign(vg, NVG_ALIGN_LEFT | NVG_ALIGN_BASELINE | NVG_ALIGN_RIGHT);
    nvgFontFace(vg, "miui_regular");
    nvgFontSize(vg, 86.0f);
    nvgTextBox(vg, 130, 380, fb_w-260, message, NULL);

    // draw button
    if (button) {
      nvgBeginPath(vg);
      nvgFillColor(vg, nvgRGBA(8, 8, 8, 255));
      nvgRoundedRect(vg, b_x, b_y, b_w, b_h, 20);
      nvgFill(vg);

      nvgFillColor(vg, nvgRGBA(255, 255, 255, 255));
      nvgFontFace(vg, "miui_regular");
      nvgTextAlign(vg, NVG_ALIGN_CENTER | NVG_ALIGN_MIDDLE);
      nvgText(vg, b_x+b_w/2, b_y+b_h/2, button, NULL);

      nvgBeginPath(vg);
      nvgStrokeColor(vg, nvgRGBA(255, 255, 255, 50));
      nvgStrokeWidth(vg, 5);
      nvgRoundedRect(vg, b_x, b_y, b_w, b_h, 20);
      nvgStroke(vg);
    }

    // draw button
    if (altbutton) {
      nvgBeginPath(vg);
      nvgFillColor(vg, nvgRGBA(8, 8, 8, 255));
      nvgRoundedRect(vg, balt_x, b_y, b_w, b_h, 20);
      nvgFill(vg);

      nvgFillColor(vg, nvgRGBA(255, 255, 255, 255));
      nvgFontFace(vg, "miui_regular");
      nvgTextAlign(vg, NVG_ALIGN_CENTER | NVG_ALIGN_MIDDLE);
      nvgText(vg, balt_x+b_w/2, b_y+b_h/2, altbutton, NULL);

      nvgBeginPath(vg);
      nvgStrokeColor(vg, nvgRGBA(255, 255, 255, 50));
      nvgStrokeWidth(vg, 5);
      nvgRoundedRect(vg, balt_x, b_y, b_w, b_h, 20);
      nvgStroke(vg);
    }
  }


  void ui_draw() {
    std::lock_guard<std::mutex> guard(lock);

    nvgBeginFrame(vg, fb_w, fb_h, 1.0f);

    switch (state) {
    case CONFIRMATION:
      count_num = (int)ceil(count_down*30 /1000) + 1;
      cancel_text = "暂时跳过 [" + std::to_string(count_num) + "]";
      draw_ack_screen("Openpilot 版本更新",
                      "当前 openpilot 分支代码有更新，更新内容已下载完毕，\r本次更新可能需要几分钟的编译时间。\r",
                      "编译升级",
                      cancel_text.data());
      break;
    case ERROR:
      draw_ack_screen("There was an error", (error_text).c_str(), NULL, "Reboot");
      break;
    }

    nvgEndFrame(vg);
  }

  void ui_update() {
    std::lock_guard<std::mutex> guard(lock);

    switch (state) {
    case ERROR:
    case CONFIRMATION: {
      int touch_x = -1, touch_y = -1;
      int res = touch_poll(&touch, &touch_x, &touch_y, 0);
      if (res == 1) {
        if (touch_x >= b_x && touch_x < b_x+b_w && touch_y >= b_y && touch_y < b_y+b_h) {
          if (state == CONFIRMATION) {
            update_thread_handle = std::thread(&UpdatedConfirm::run_stages, this);
          }
        }
        if (touch_x >= balt_x && touch_x < balt_x+b_w && touch_y >= b_y && touch_y < b_y+b_h) {
          count_down = 0;
        }
      }
    }
    default:
      break;
    }
  }


  void go() {
    while (count_down > 1) {
      ui_update();

      glClearColor(0.08, 0.08, 0.08, 1.0);
      glClear(GL_STENCIL_BUFFER_BIT | GL_COLOR_BUFFER_BIT);

      // background
      nvgBeginPath(vg);
      NVGpaint bg = nvgLinearGradient(vg, fb_w, 0, fb_w, fb_h,
        nvgRGBA(0, 0, 0, 0), nvgRGBA(0, 0, 0, 255));
      nvgFillPaint(vg, bg);
      nvgRect(vg, 0, 0, fb_w, fb_h);
      nvgFill(vg);

      glEnable(GL_BLEND);
      glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

      ui_draw();

      glDisable(GL_BLEND);

      framebuffer_swap(fb);
      
      assert(glGetError() == GL_NO_ERROR);

      // no simple way to do 30fps vsync with surfaceflinger...
      usleep(30000);
      // countdown 3s to continue
      count_down--;
    }

    if (update_thread_handle.joinable()) {
      update_thread_handle.join();
    }

    exit(1);
  }


};

}
int main(int argc, char *argv[]) {
  UpdatedConfirm updatedConfirm;
  updatedConfirm.go();

  return 0;
}
