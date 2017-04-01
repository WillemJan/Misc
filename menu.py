#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright © 2013 Willem Jan Faber (http://www.fe2.nl) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
* Neither the name of “Fe2“ nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
