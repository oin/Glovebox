/*
 GloveBox. An experimental improvised music environment.
 Copyright (C) 2012 Jonathan Aceituno
 http://glovebox.oin.name
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "gl_texture.h"
#include <algorithm>

#define GLTHEINTERNALFORMAT GL_RGB8
#define GLTHEFORMAT GL_RGB
#define GLTHETYPE GL_UNSIGNED_BYTE

GlTexture::GlTexture(unsigned int w, unsigned int h) : width(w), height(h), data(0), texid_(0) {
	data = new unsigned char[width*height*3];
	
	glGenTextures(1, &texid_);
	
	glEnable(GL_TEXTURE_2D);
	
	glBindTexture(GL_TEXTURE_2D, texid_);
	
	glTexImage2D(GL_TEXTURE_2D, 0, GLTHEINTERNALFORMAT, width, height, 0, GLTHEFORMAT, GLTHETYPE, data);
	
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, /*GL_CLAMP_TO_EDGE*/GL_REPEAT);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, /*GL_CLAMP_TO_EDGE*/GL_REPEAT);
	
	// glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
	glDisable(GL_TEXTURE_2D);
}

GlTexture::~GlTexture() {
	delete[] data;
	glDeleteTextures(1, &texid_);
}

void GlTexture::Load(unsigned char* data) {
	// std::copy(d, d + width*height*3, data);
	
	GLint prevAlignment;
	glGetIntegerv(GL_UNPACK_ALIGNMENT, &prevAlignment);
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
	
	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D, texid_);
	glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GLTHEFORMAT, GLTHETYPE, data);
	glDisable(GL_TEXTURE_2D);
	
	glPixelStorei(GL_UNPACK_ALIGNMENT, prevAlignment);
}

void GlTexture::Draw(float w, float h) {
	glActiveTexture(GL_TEXTURE0);
	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D, texid_);
	
	GLfloat tex_coords[] = {
		0.0f,0.0f,
		1.0f,0.0f,
		1.0f,-1.0f,
		0.0f,-1.0f
	};
	GLfloat verts[] = {
		0.0f,0.0f,
		w,0.0f,
		w,h,
		0.0f,h
	};
	glEnableClientState( GL_TEXTURE_COORD_ARRAY );
	glTexCoordPointer(2, GL_FLOAT, 0, tex_coords );
	glEnableClientState(GL_VERTEX_ARRAY);		
	glVertexPointer(2, GL_FLOAT, 0, verts );
	glDrawArrays( GL_TRIANGLE_FAN, 0, 4 );
	glDisableClientState( GL_TEXTURE_COORD_ARRAY );
	
	glDisable(GL_TEXTURE_2D);
}