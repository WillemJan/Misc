#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyleft 2013 Willem Jan Faber (http://www.fe2.nl)
'''

import array
import cairo
import pygame

# Global settings
from config import PI

def RectangleRound(x1 = 0, y1 = 0, x2 = 260, y2 = 30, r = 12,color = (.7,.7,.7,1)):
	data = array.array('b', chr(0) * (x2 - x1) *  (y2 - y1) * 4)
	stride = (x2 - x1) * 4
	surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32, (x2 - x1), (y2 - y1), stride)
	ctx = cairo.Context(surface)
	ctx.set_source_rgb(color[0], color[1], color[2])
	ctx.move_to(x1 + r, y1)
	ctx.line_to(x1 + r, y1)
	ctx.arc(x2 - r, y1 + r, r, PI + (PI / 2), 2 * PI)
	ctx.line_to(x2, y1 + r)
	ctx.arc(x2 - r, y2 - r, r, 2 * PI, 2 * PI + (PI / 2))
	ctx.line_to(x1 + r + r, y2)
	ctx.arc(x1 + r, y2 - r, r, 2 * PI + (PI / 2), 3 * PI)
	ctx.line_to(x1, y1 + r)
	ctx.arc(x1 + r, y1 + r, r, 3 * PI, PI + PI / 2)
	pat=cairo.LinearGradient (0.0, 0.0, 0.0, 0.6)
	ctx.fill()
	img=pygame.image.frombuffer(data.tostring(), ((x2 - x1), (y2 - y1)), "RGBA")
	return (img)
