#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pwm.h"



#include <stdio.h>
#include <stdlib.h>

#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/clocks.h"
#include "ws2812.pio.h"
#include "char_data.h"

static uint     ledgpio = 25;   //  GPIO number of LED on board
static uint     wrap = 500;     //  TOP register value

static uint16_t levelFromCount(int i);



#define IS_RGBW false
#define NUM_PIXELS 8*32*1
#define NUM_PIXELS 8*32*3
#define WS2812_PIN 15

static inline void put_pixel(uint32_t pixel_grb) {
    pio_sm_put_blocking(pio0, 0, pixel_grb << 8u);
}

static inline uint32_t urgb_u32(uint8_t r, uint8_t g, uint8_t b) {
    return
            ((uint32_t) (r) << 8) |
            ((uint32_t) (g) << 16) |
            (uint32_t) (b);
}

void pattern_snakes(uint len, uint t) {
    for (uint i = 0; i < len; ++i) {
        uint x = (i + (t >> 1)) % 64;
        if (x < 10)
            put_pixel(urgb_u32(0xff, 0, 0));
        else if (x >= 15 && x < 25)
            put_pixel(urgb_u32(0, 0xff, 0));
        else if (x >= 30 && x < 40)
            put_pixel(urgb_u32(0, 0, 0xff));
        else
            put_pixel(0);
    }
}

void pattern_random(uint len, uint t) {
    if (t % 8)
        return;
    for (int i = 0; i < len; ++i)
        put_pixel(rand());
}

void pattern_red(uint len, uint t) {
    if (t % 8)
        return;
    for (int i = 0; i < len; ++i)
        put_pixel(urgb_u32(0xff, 0, 0));
}

void pattern_green(uint len, uint t) {
    if (t % 8)
        return;
    for (int i = 0; i < len; ++i)
        put_pixel(urgb_u32(0x00, 0xff, 0));
}
void pattern_blue(uint len, uint t) {
    if (t % 8)
        return;
    for (int i = 0; i < len; ++i)
        put_pixel(urgb_u32(0x00, 0x0, 0xff));
}

void pattern_sparkle(uint len, uint t) {
    if (t % 8)
        return;
    for (int i = 0; i < len; ++i)
        put_pixel(rand() % 16 ? 0 : 0xffffffff);
}

void pattern_greys(uint len, uint t) {
    int max = 100; // let's not draw too much current!
    t %= max;
    for (int i = 0; i < len; ++i) {
        put_pixel(t * 0x10101);
        if (++t >= max) t = 0;
    }
}

typedef void (*pattern)(uint len, uint t);
const struct {
    pattern pat;
    const char *name;
} pattern_table[] = {
	/*
        {pattern_red,  "red!"},
        {pattern_green,  "green!"},
        {pattern_blue,  "blue!"},
	*/
        {pattern_snakes,  "Snakes!"},
        {pattern_random,  "Random data"},
        {pattern_sparkle, "Sparkles"},
        {pattern_greys,   "Greys"},
};

/* PWM stuff
    gpio_set_function(ledgpio, GPIO_FUNC_PWM);
    uint    slice = pwm_gpio_to_slice_num(ledgpio);
    uint    chan = pwm_gpio_to_channel(ledgpio);
    pwm_set_wrap(slice, wrap);
    pwm_set_chan_level(slice, chan, 0);
    pwm_set_clkdiv(slice, 10.0);
    pwm_set_enabled(slice, true);
    uint64_t    usleep100 = 1000;    //  sleep time for one stage in the period

    while (true) {
        int c = getchar_timeout_us(0);  //  check for input from USB
        if ((c != PICO_ERROR_TIMEOUT) && ('0' <= c)) {
            usleep100 = (uint64_t)((c - '0') * 100);
            printf("sleep time is set to %dusec\n", (int)usleep100);
        }
        int i;
        for (i = 0 ; i < wrap ; i ++) {
            pwm_set_chan_level(slice, chan, levelFromCount(i));
            sleep_us(usleep100);
        }
        for (i = wrap ; 0 < i ; i --) {
            pwm_set_chan_level(slice, chan, levelFromCount(i));
            sleep_us(usleep100);
        }
   }

static uint16_t levelFromCount(int i)
{
    return (uint16_t)(i * i / wrap);
}

   */


uint32_t screen_buf[NUM_PIXELS] = { 0 };

int draw_char(char c, int offset_x, int offset_y, uint32_t color) {
        int char_index = 0;
	for (int ci = 0; ci < count_of(char_data); ci++) {
		if (char_data[ci].sym == c) {
			char_index = ci;
		}
	}

	for (int x = 0; x < 6; x++) {
	   for (int y = 0; y < 8; y++) {
		   uint32_t val = color * char_data[char_index].data[x + y * 6];
		   int scr_x = x + offset_x;
		   int scr_y = y + offset_y;
		   if (scr_x >= 0 && scr_x <= NUM_PIXELS/8 && scr_y >= 0 && scr_y < 8) {
		     int scr_offs = 8*scr_x + 8*(scr_x%2) - scr_x%2 + scr_y * (1-((scr_x%2)*2));
		     if (scr_offs >= 0 && scr_offs < NUM_PIXELS) {
		        screen_buf[scr_offs] = val; // urgb_u32(x*8, y*8, 0);
		     }
		   }
	   }
	}
}

int draw_str(char *s, int offset_x, int offset_y, uint32_t color) {
	int extra_offset_x = 0;
	while(*s)  {
		draw_char(*s, offset_x + extra_offset_x, offset_y, color);
		extra_offset_x += 6;
		s++;
	}
}
void clear_buf() {
		for (int i = 0; i < NUM_PIXELS; ++i) {
			screen_buf[i] = 0;
		}
}

void scroll_buf() {
		for(int dst_x=0; dst_x<(NUM_PIXELS/8); dst_x++) {
			for(int scr_y=0; scr_y<8; scr_y++) {
				int scr_x = dst_x+1;
				int scr_offs = 8*scr_x + 8*(scr_x%2) - scr_x%2 + scr_y * (1-((scr_x%2)*2));
				int dst_offs = 8*dst_x + 8*(dst_x%2) - dst_x%2 + scr_y * (1-((dst_x%2)*2));
				screen_buf[dst_offs] = scr_offs >= NUM_PIXELS ? urgb_u32(0, 0, 0) : screen_buf[scr_offs];
			}
		}
}
void draw_buf() {
		for (int i = 0; i < NUM_PIXELS; ++i) {
			put_pixel(screen_buf[i]);
		}
}

int scroll_str_offs(char *s, uint32_t color, int offset_y) {
	int max_offset_x = NUM_PIXELS/8;
	int min_offset_x = NUM_PIXELS/8-strlen(s)*6;
	int curr_offset_x = max_offset_x;
	while(curr_offset_x >= min_offset_x) {
		scroll_buf();
		draw_str(s, curr_offset_x, offset_y, color);
		draw_buf();
		sleep_us(6500);
		curr_offset_x--;
	}
}

int scroll_str(char *s, uint32_t color) {
	scroll_str_offs(s, color, 0);
}


int main() {
    stdio_init_all();
    printf("WS2812 Smoke Test, using pin %d", WS2812_PIN);

    // todo get free sm
    PIO pio = pio0;
    int sm = 0;
    uint offset = pio_add_program(pio, &ws2812_program);

    ws2812_program_init(pio, sm, offset, WS2812_PIN, 1100000, IS_RGBW);

    while (1) {
	scroll_str("#", urgb_u32(0x00, 0x70, 0x00));
	scroll_str("LETS", urgb_u32(0x00, 0x00, 0x7f));
	scroll_str("RIDE", urgb_u32(0x00, 0x70, 0x00));
	scroll_str("TOGETHER  ", urgb_u32(0x00, 0x00, 0x7f));
	scroll_str_offs("a", urgb_u32(0x00, 0x00, 0x20), +2);
	scroll_str_offs("a", urgb_u32(0x00, 0x10, 0x00), -3);
	scroll_str("a", urgb_u32(0x20, 0x0, 0x00));
	scroll_str("y", urgb_u32(0x20, 0x0, 0x30));
	scroll_str_offs("y", urgb_u32(0x00, 0x20, 0x30), +1);
	scroll_str_offs("y", urgb_u32(0x00, 0x60, 0x00), -1);
	scroll_str_offs("y", urgb_u32(0x30, 0x40, 0x00), +2);
	scroll_str_offs("y ", urgb_u32(0x30, 0x00, 0x30), -2);
	scroll_str("HTTPS://", urgb_u32(0x10, 0x10, 0x00));
	scroll_str("CRITICALMASS.BRUSSELS", urgb_u32(0x40, 0x40, 0x00));
	scroll_str("/  ", urgb_u32(0x10, 0x10, 0x00));
    }

    return 0;
}
